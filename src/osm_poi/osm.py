import overpy
import json
from collections import Counter
from typing import Dict, Any, Tuple
import logging
from osm_poi.utils import get_filename, get_path, load_file, get_first_label


class OSM:
    def __init__(self, max_retry_count: int = 4, retry_timeout: int = 3):
        self.api = overpy.Overpass(
            max_retry_count=max_retry_count, retry_timeout=retry_timeout
        )

    def query(self, minx: int, miny: int, maxx: int, maxy: int) -> Tuple[list, list]:
        result = self.api.query(
            f"""
            (way
            ({minx},{miny},{maxx},{maxy});
            node
            ({minx},{miny},{maxx},{maxy});
            );
            out body;
            """
        )
        return result.nodes, result.ways


def remove_labels(path: str) -> None:
    """
    Remove unwanted labels from nodes and ways. Overwrite the existing files
    with only the desidered labels.

    Parameters
    ----------
    path : str
        Path to load with all the features

    Returns
    -------
    None
    """
    directory, filename = get_path(path), get_filename(path)
    data: Dict[str, Any] = {"features": [], "nodes": {}, "ways": {}}

    for key in data:
        with open(f"{directory}/{filename}-{key}.json") as f:
            data[key] = json.load(f)
            logging.info(f"Loaded file {directory}/{filename}-{key}.json")

    for polygon in data["features"]:
        for node in list(polygon["nodes"]):
            if node not in data["nodes"]:
                del polygon["nodes"][node]
        for way in list(polygon["ways"]):
            if way not in data["ways"]:
                del polygon["ways"][way]

    for key in data:
        with open(f"{directory}/{filename}-{key}.json", "w") as write_file:
            json.dump(data[key], write_file)
            logging.info(f"Dumped file {directory}/{filename}-{key}.json")

    logging.info(f"Completed.")


def download(
    path: str, max_retry_count: int, retry_timeout: int, label: str = None
) -> None:
    """
    Load file with GeoPandas, query OpenStreetMap both nodes and ways
    for each feature included and dump into three JSON files.

    Parameters
    ----------
    path : str
        Path to load with all the features
    path : str
        Path to load
    max_retry_count : int
        Max number of retries to query OSM
    retry_timeout : int
        Retry timeout to query OSM
    label : str, optional
        Name of the column which contains the polygon ID/Name

    Returns
    -------
    None
    """
    gdf = load_file(path)
    api = OSM(max_retry_count=max_retry_count, retry_timeout=retry_timeout)
    data: Dict[str, Any] = {"features": [], "nodes": {}, "ways": {}}

    if label is not None and label not in gdf.columns:
        logging.error(f"The label {label} is not a valid column.")
        return

    for index, row in gdf.iterrows():
        nodes, ways = api.query(row.miny, row.minx, row.maxy, row.maxx)

        nodes = [get_first_label(item.tags) for item in nodes if any(item.tags)]
        ways = [get_first_label(item.tags) for item in ways if any(item.tags)]

        data["nodes"].extend(nodes)
        data["ways"].extend(ways)

        polygon = {
            "id": row[label] if label else index,
            "nodes": Counter(nodes),
            "ways": Counter(ways),
        }

        data["features"].append(polygon)
        logging.debug(
            f"Queried polygon {index} with {len(nodes)} nodes types and {len(ways)} ways types."
        )

    data["nodes"] = Counter(data["nodes"])
    data["ways"] = Counter(data["ways"])

    directory, filename = get_path(path), get_filename(path)
    for key in data:
        with open(f"{directory}/{filename}-{key}.json", "w") as write_file:
            json.dump(data[key], write_file)
            logging.info(f"Dumped file {directory}/{filename}-{key}.json")

    logging.info("Completed.")
