from . import encoder
from . import decoder


def decode(tile, y_coord_down=False):
    vector_tile = decoder.TileData()
    message = vector_tile.getMessage(tile, y_coord_down)
    return message


def encode(layers, quantize_bounds=None, y_coord_down=False, extents=4096,
           on_invalid_geometry=None, round_fn=None):
    vector_tile = encoder.VectorTile(extents, on_invalid_geometry,
                                     round_fn=round_fn)
    if (isinstance(layers, list)):
        for layer in layers:
            vector_tile.addFeatures(layer['features'], layer['name'],
                                    quantize_bounds, y_coord_down)
    else:
        vector_tile.addFeatures(layers['features'], layers['name'],
                                quantize_bounds, y_coord_down)

    return vector_tile.tile.SerializeToString()


def encode_geoms_then_props(layers, props, quantize_bounds=None, y_coord_down=False, extents=4096,
                            on_invalid_geometry=None, round_fn=None):
    from datetime import datetime
    geom_start = datetime.now()
    vector_tile = encoder.VectorTile(extents, on_invalid_geometry,
                                     round_fn=round_fn)
    if (isinstance(layers, list)):
        for layer in layers:
            vector_tile.addFeatures(layer['features'], layer['name'],
                                    quantize_bounds, y_coord_down)
    else:
        vector_tile.addFeatures(layers['features'], layers['name'],
                                quantize_bounds, y_coord_down)
    geom_end = datetime.now()
    vector_tile.add_props(props)
    props_end = datetime.now()
    print (geom_end - geom_start).total_seconds()
    print (props_end - geom_end).total_seconds()
    s = vector_tile.tile.SerializeToString()
    print (datetime.now() - props_end).total_seconds()
    return s
