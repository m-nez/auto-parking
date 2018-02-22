import parking
import numpy

class Backend:
    def __init__(self, array, lifts, scenario=None):
        self._array = array
        self._lifts = lifts
        self._cars = {}
        self._scenario = scenario

        self._spawnpoints = numpy.vstack(numpy.where(array[:,:,:,0] == parking.ENTRANCE)).T

        self._id = 0

    def _get_new_id(self):
        self._id += 1
        return self._id

    def _spawn(self, sp):
        cid = self._get_new_id()
        self._array[sp][1] = cid
        self._cars[cid] = sp
        return cid

    def _move(self, lid, dest, pickup, lift_moves, car_moves):
        src = tuple(self._lifts[lid])
        dest = tuple(dest)
        self._lifts[lid] = dest
        lift_moves.append((lid, *dest))
        if pickup:
            cid = self._array[src][1]
            if cid != parking.EMPTY:
                car_moves.append((cid, *dest))
                self._array[dest][1] = self._array[src][1]
                self._array[src][1] = parking.EMPTY

    def _within_bounds(self, dest):
        for axis_size, d in zip(self._array.shape, dest):
            if 0 <= d < axis_size:
                continue
            else:
                return False
        return True
    
    def _valid_move(self, src, dest, pickup):
        dest = tuple(dest)
        src = tuple(src)
        if not self._within_bounds(dest):
            return False
        if self._array[dest][0] == parking.WALL:
            return False
        if dest[0] > src[0] and self._array[dest][0] != parking.CHANNEL:
            return False
        elif dest[0] < src[0] and self._array[src][0] != parking.CHANNEL:
            return False
        if self._array[tuple(dest)][1] != parking.EMPTY and pickup:
            return False
        return True

    def step(self):
        """
        Returns:
        car_despawns : [id, ...]
        car_spawns : [(id, z, y, x), ...]
        car_moves : [(id, to_z, to_y, to_x)), ...]
        lift_moves : [(id, to_z, to_y, to_x)), ...]
        """
        
        car_despawns = []
        car_spawns = []
        car_moves = []
        lift_moves = []

        if self._scenario is None:
            sp = tuple(self._spawnpoints[0])
            if self._array[sp][1] == parking.EMPTY:
                cid = self._spawn(sp)
                car_spawns.append((cid, *sp))

        for lid, l in enumerate(self._lifts):
            axis = numpy.random.randint(3)
            src = tuple(l)
            dest = list(l)
            dest[axis] += numpy.random.randint(-1, 2)
            pickup = numpy.random.randint(5) and self._array[src][1] != parking.EMPTY
            if self._valid_move(src, dest, pickup):
                self._move(lid, dest, pickup, lift_moves, car_moves)

        return car_despawns, car_spawns, car_moves, lift_moves
