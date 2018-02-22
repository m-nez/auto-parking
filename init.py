import bge
import parking
from vis import Vis

if __name__ == "__main__":
    a, l = parking.load_json_array(parking.SIMPLE)
    o = bge.logic.getCurrentController().owner
    o['vis'] = Vis(a, l)

