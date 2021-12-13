import logging
import sys
import argparse
from osm_poi.osm import download


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "profile",
        metavar="profile",
        type=str,
    )
    parser.add_argument(
        "filename",
        metavar="filename",
        type=str,
    )
    args = parser.parse_args()
    profile = args.profile

    if profile == "query":
        logging.info(f"Running process query loading file {args.filename}")
        download(args.filename)
    if profile == "clean":
        pass
