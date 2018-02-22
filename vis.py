import sys
import bge
import parking
from backend import Backend
from mathutils import Vector

class Vis:
    def __init__(self, array, lifts):
        scene = bge.logic.getCurrentScene()
        self._scene = scene
        self._array = array
        self._levels = [set() for _ in range(len(array))]
        for zi, z in enumerate(array):
            for yi, y in enumerate(z):
                for xi, x in enumerate(y):
                    t, c = x
                    objs = {
                            parking.FLOOR : "floor",
                            parking.ENTRANCE : "entrance",
                            parking.EXIT : "exit",
                            }
                    if t in objs:
                        obj = scene.addObject(objs[t])
                        obj.worldPosition = (xi, yi, zi)
                        self._levels[zi].add(obj)

        self._cars = {}
        self._lifts = {}
        for i, l in enumerate(lifts):
            lift = scene.addObject("lift")
            lift.worldPosition = [*reversed(l)]
            self._lifts[i] = lift

        self._backend = Backend(array, lifts)
        self._tick_period = scene.objects["control"]["tick_period"]

    def set_level_visibility(self, level, visibility):
        for o in self._levels[level]:
            o.visible = visibility

    def get_level_visibility(self, level):
        if len(self._levels[level]) > 0:
            return next(iter(self._levels[level])).visible
        else:
            return False

    def step(self):
        car_despawns, car_spawns, car_moves, lift_moves = self._backend.step()
        for cid in car_despawns:
            self._cars[cid].endObject()
            self._cars.pop(cid)

        for cs in car_spawns:
            cid = cs[0]
            dest = cs[1:]
            car = self._scene.addObject("car")
            self._cars[cid] = car
            car.position = Vector(reversed(dest))

        for o in self._scene.objects:
            o.worldLinearVelocity = (0,0,0)

        for cm in car_moves:
            cid = cm[0]
            dest = cm[1:]
            car = self._cars[cid]
            car.worldLinearVelocity = (Vector(reversed(dest)) - car.position) / self._tick_period

        for lm in lift_moves:
            lid = lm[0]
            dest = lm[1:]
            lift = self._lifts[lid]
            lift.worldLinearVelocity = (Vector(reversed(dest)) - lift.position) / self._tick_period
