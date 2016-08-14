from geomet import wkt
import json

xmin = -74.0039062396984
xmax = -73.9929199115749
ymin = 40.7056279334954
ymax = 40.713955821575

geojson = json.loads(open('./mapbox_vector_tile/15_9648_12320.json').read())

_geo = geojson['boundaries']['features'][0]['geometry']

from mapbox_vector_tile import encode_geoms_then_props

features = []


def normalize(val, dim):
    if dim == 'x':
        return int(round((val - xmin) / (xmax - xmin) * 4096))
    elif dim == 'y':
        return int(round((val - ymin) / (ymax - ymin) * 4096))

from datetime import datetime
start = datetime.now()


id = 1
props = {}

for k in geojson.keys():

    if k not in features:
        features.append({'name': k, 'features': []})

    for feature in geojson[k]['features']:

        g = feature['geometry']
        if g['type'] == 'Point':
            g['coordinates'][0] = normalize(g['coordinates'][0], 'x')
            g['coordinates'][1] = normalize(g['coordinates'][1], 'y')

            _wkt = wkt.dumps(feature['geometry'], decimals=0)

            item = [a for a in features if a['name'] == k][0]
            item['features'].append({
                'geometry': _wkt,
                'properties': {'id': id}
            })
        elif g['type'] in ('Polygon', 'MultiLineString'):
            for i, coord_set in enumerate(g['coordinates']):
                for j, coord_pair in enumerate(coord_set):
                    g['coordinates'][i][j][0] = normalize(g['coordinates'][i][j][0], 'x')
                    g['coordinates'][i][j][1] = normalize(g['coordinates'][i][j][1], 'y')

            _wkt = wkt.dumps(feature['geometry'], decimals=0)

            item = [a for a in features if a['name'] == k][0]
            item['features'].append({
                'geometry': _wkt,
                'properties': {'id': id}
            })

        elif g['type'] == 'LineString':
            for i, coord_pair in enumerate(g['coordinates']):
                g['coordinates'][i][0] = normalize(g['coordinates'][i][0], 'x')
                g['coordinates'][i][1] = normalize(g['coordinates'][i][1], 'y')

            _wkt = wkt.dumps(feature['geometry'], decimals=0)

            item = [a for a in features if a['name'] == k][0]
            item['features'].append({
                'geometry': _wkt,
                'properties': {'id': id}
            })

        elif g['type'] == 'MultiPolygon':
            for l, polygon in enumerate(g['coordinates']):
                for i, coord_set in enumerate(polygon):
                    for j, coord_pair in enumerate(coord_set):
                        g['coordinates'][l][i][j][0] = normalize(g['coordinates'][l][i][j][0], 'x')
                        g['coordinates'][l][i][j][1] = normalize(g['coordinates'][l][i][j][1], 'y')

            _wkt = wkt.dumps(feature['geometry'], decimals=0)

            item = [a for a in features if a['name'] == k][0]
            item['features'].append({
                'geometry': _wkt,
                'properties': {'id': id}
            })

        else:
            print g['type']

        props[id] = feature['properties']
        props[id]['id'] = id
        id += 1

# print max(props.keys())
print (datetime.now() - start).total_seconds()

# print features

# from datetime import datetime
start = datetime.now()
with open('./mapbox_vector_tile/15_9648_12320.mvt', 'w') as mvt:
    mvt.write(encode_geoms_then_props(features, props))
# print (datetime.now() - start).total_seconds()

for k in geojson.keys():
    print k, len(geojson[k]['features'])
