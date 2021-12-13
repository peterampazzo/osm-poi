# OpenStreetMap POIs

To install:

```
virtualenv env
source env/bin/activate
pip install -e ".[devel]"
```

Two profile are currently supported `query` and `filter`.
1. The first profile query all the nodes and ways from OSM within the polygons included in the file passed.
2. The second profile remove keys if they have been removed from the two main lists (`-nodes.json` and `-ways.json`) generated from the previous step.

To test the behaviour an example file is provided:
```
osm_poi query example/grid.json
```
