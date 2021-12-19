import logging
import sys
import argparse
from pyhocon import ConfigFactory
from osm_poi.osm import download, remove_labels


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", type=str)
    parser.add_argument("filename", type=str)
    parser.add_argument("--label", type=str)
    args = parser.parse_args()
    profile = args.profile

    config = ConfigFactory.parse_file("app.conf")

    logging.basicConfig(
        level=logging.getLevelName(config["conf"]["logging_level"]),
        format="[%(asctime)s] - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )

    logging.getLogger("fiona").setLevel(
        logging.getLevelName(config["conf"]["logging_level_modules"])
    )

    if profile == "query":
        logging.info(f"Running process query loading file {args.filename}")
        download(
            path=args.filename,
            max_retry_count=config["overpy"]["max_retry_count"],
            retry_timeout=config["overpy"]["retry_timeout"],
            label=args.label,
        )
    if profile == "filter":
        logging.info(f"Running process filter loading file {args.filename}")
        remove_labels(args.filename)
