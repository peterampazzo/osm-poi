import os
import geopandas as gpd
from shapely.geometry import box
from typing import Dict, Any


def get_path(path: str) -> str:
    """
    Given a file path, return the directory path.

    Parameters
    ----------
    path : str
        File path

    Returns
    -------
    str
    """
    return os.path.dirname(path)


def get_filename(path: str) -> str:
    """
    Given a file path, return the filename without extension.

    Parameters
    ----------
    path : str
        File path

    Returns
    -------
    str
    """
    return os.path.basename(path).split(".")[0]


def load_file(filename: str) -> gpd.GeoDataFrame:
    # bbox = min Longitude , min Latitude , max Longitude , max Latitude

    data = gpd.read_file(filename)
    poly_geom = data.bounds  # bounds for individual geometries
    b = poly_geom.apply(lambda row: box(row.minx, row.miny, row.maxx, row.maxy), axis=1)
    data = gpd.GeoDataFrame(poly_geom, geometry=b)

    return data


def get_first_label(item: Dict[str, Any]) -> str:

    key = list(item.keys())[0]
    return f"{key}={item[key]}"
