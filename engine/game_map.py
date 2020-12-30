class Map:
    def __init__(self, width, height):
        from numpy import full
        from .tile import wild_ground

        self.width = width
        self.height = height
        self.player_at = None

        self.tiles = full(
            (width, height),
            fill_value=wild_ground[0],
            order="F",
        )
        self.visible = full((width, height), fill_value=False, order="F")
        self.explored = full((width, height), fill_value=False, order="F")

    def in_bounds(self, x, y):
        return 1 <= x < self.width and 1 <= y < self.height

    def render(self, wide, tall, focus, console):
        from numpy import select
        from .tile import hidden

        # horizontal
        if focus.x <= wide // 2:
            focalx = max(0, focus.x)
            left = 0

        elif focus.x >= (self.width - wide // 2):
            focalx = min(wide, wide - self.width + focus.x)
            left = self.width - wide

        else:
            focalx = wide // 2
            left = focus.x - wide // 2

        # vertical
        if focus.y <= tall // 2:
            focaly = max(0, focus.y)
            top = 0

        elif focus.y >= (self.height - tall // 2):
            focaly = min(tall, tall - self.height + focus.y)
            top = self.height - tall

        else:
            focaly = tall // 2
            top = focus.y - tall // 2

        right = left + wide
        left += 1

        bottom = top + tall
        top += 1

        # actual render
        console.tiles_rgb[1:wide, 1:tall] = select(
            condlist=[
                self.visible[left:right, top:bottom],
                self.explored[left:right, top:bottom],
            ],
            choicelist=[
                self.tiles["lit"][left:right, top:bottom],
                self.tiles["dark"][left:right, top:bottom],
            ],
            default=hidden,
        )
        self.player_at = focalx, focaly


class FractalMap(Map):
    def __init__(self, width, height, ragged):
        from tcod.noise import Noise
        from numpy import arange, float32

        super().__init__(width, height)

        self.noise = Noise(
            dimensions=2,
            algorithm=2,
            implementation=2,
            hurst=ragged,
            lacunarity=2.0,
            octaves=4,
        )

        self.ogrid = [arange(width, dtype=float32), arange(height, dtype=float32)]

        self.prepare()

    def scale(self, x=1, y=None):
        self.ogrid[0] *= x
        self.ogrid[1] *= y if y is not None else x

        self.prepare()

    def prepare(self):
        from .util import tileselector
        from .tile import wild_ground, wild_feature, wild_blocker

        sample = self.noise.sample_ogrid(self.ogrid)

        blocker = sample >= 0.9
        feature = sample < 0.9
        ground = sample < 0.75

        self.tiles[blocker] = tileselector(
            wild_blocker,
            self.tiles[blocker].size,
            [0.25, 0.25, 0.25, 0.25],
        )
        self.tiles[feature] = tileselector(wild_feature, self.tiles[feature].size)
        self.tiles[ground] = tileselector(wild_ground, self.tiles[ground].size)
