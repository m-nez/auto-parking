import numpy
import json

WALL = 0
CHANNEL = 1
FLOOR = 2
ENTRANCE = 3
EXIT = 4

EMPTY = -1

TYPE = 0
ID = 1

def load_json_array(filename):
    with open(filename) as f:
        j = json.load(f)
        parking = j["parking"]
        zl = len(parking)
        yl = len(parking[0])
        xl = len(parking[0][0])
        array = numpy.empty((zl, yl, xl, 2), dtype=numpy.int64)
        array[:,:,:,0] = parking
        array[:,:,:,1] = EMPTY
        
    return array, j["lifts"]

SIMPLE = "data/simple.json"
