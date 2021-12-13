import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))

devel = ["black", "mypy"]

setuptools.setup(
    name="OpenStreetMap POI",
    version="0.1.0",
    description="OverPy wrapper to query OpenStreetMap POIs",
    author="Pietro Rampazzo",
    author_email="pietro@rampazzo.co",
    url="https://github.com/peterampazzo/osm-poi",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=["geopandas", "overpy", "shapely"],
    extras_require={"devel": devel},
    entry_points={
        "console_scripts": [
            "osm_poi = osm_poi.main:main",
        ],
    },
)
