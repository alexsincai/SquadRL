class Action:
    def perform(self):
        pass


class EscapeAction(Action):
    def perform(self):
        pass


class MoveAction(Action):
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def perform(self, terrain, actor, callback):
        dx = actor.x + self.dx
        dy = actor.y + self.dy

        if not terrain.in_bounds(dx, dy):
            return

        if not terrain.tiles["walkable"][dx, dy]:
            return

        actor.move(dx=self.dx, dy=self.dy)
        actor.q.clear()
        callback()


class ClickAction(Action):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def perform(self, player_position, target_position, map_tiles, callback):
        from numpy import ones, int8
        from tcod.path import SimpleGraph, Pathfinder

        maxx, maxy = map_tiles.shape
        tgtx, tgty = target_position
        target_position = min(tgtx, maxx - 1), min(tgty, maxy - 1)

        cost = ones(map_tiles.shape, dtype=int8, order="F")
        for x in range(2, map_tiles.shape[0]):
            for y in range(2, map_tiles.shape[1]):
                if not map_tiles[x, y]["walkable"]:
                    cost[x, y] = -1

        graph = SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pf = Pathfinder(graph)
        pf.add_root(player_position)

        callback()
        return pf.path_from(target_position).tolist()[:-1]


class RightClickAction(Action):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def perform(self, player_position, map_tiles):
        from tcod.los import bresenham

        lasing = []
        for spot in bresenham(player_position, (self.x, self.y)).tolist()[1:]:
            x, y = spot
            if map_tiles[x, y]["transparent"]:
                lasing.append(spot)

        return lasing
