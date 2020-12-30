from .actions import *


class Engine:
    def __init__(self, width, height, view_width, view_height, tileset, title):
        from os.path import join
        from .event_handler import EventHandler

        self.width = width
        self.height = height
        self.view_width = view_width
        self.view_height = view_height
        self.tileset = join("assets", tileset)
        self.title = title

        self.console = self.__create_console__()
        self.window = self.__create_window__()

        self.event_handler = EventHandler()

        self.vfx = []

        self.map_type = 0
        self.maps = []
        self.build_map()

        self.player = self.place_actor()
        self._update_fov()

        self.actors = self.place_npcs()

    def __create_console__(self):
        from tcod.console import Console

        return Console(
            width=self.width,
            height=self.height,
            order="F",
        )

    def __create_window__(self):
        from tcod.context import new
        from tcod.tileset import load_tilesheet, CHARMAP_CP437

        tileset = load_tilesheet(
            path=self.tileset,
            columns=16,
            rows=16,
            charmap=CHARMAP_CP437,
        )
        return new(
            rows=self.height,
            columns=self.width,
            tileset=tileset,
            vsync=True,
            title=self.title,
        )

    def build_map(self):
        from .game_map import FractalMap

        if self.map_type == 0:
            terrain = FractalMap(
                width=200,
                height=200,
                ragged=0.85,
            )

            terrain.scale(0.01)

            self.maps.append(terrain)
            self.map = terrain

    def _update_fov(self):
        from tcod.map import compute_fov

        self.map.visible[:] = compute_fov(
            transparency=self.map.tiles["transparent"],
            pov=(self.player.x, self.player.y),
            radius=8,
            algorithm=2,
        )
        self.map.explored |= self.map.visible

    def place_actor(self, icon="@", controlled=True):
        from .actor import Actor
        from numpy.random import randint

        offsets = [
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (0, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        ]

        while True:
            randx = randint(1, self.map.width - 1)
            randy = randint(1, self.map.height - 1)

            placers = []
            for offset in offsets:
                ox, oy = offset
                placers.append(self.map.tiles[randx + ox, randy + oy]["walkable"])

            if all(placers):
                return Actor(randx, randy, icon, controlled)

    def place_npcs(self):
        out = [self.place_actor("@", False) for _ in range(14)]
        return out

    def event_loop(self):
        import tcod.event as e
        from time import sleep

        for event in e.wait(0.16):

            self.window.convert_event(event)
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            else:
                self.vfx.clear()

            if isinstance(action, EscapeAction):
                raise SystemExit()

            if isinstance(action, MoveAction):
                action.perform(
                    terrain=self.map,
                    actor=self.player,
                    callback=self._update_fov,
                )

            if isinstance(action, ClickAction):
                actualx = action.x - self.map.player_at[0] + self.player.x
                actualy = action.y - self.map.player_at[1] + self.player.y

                self.player.q = action.perform(
                    player_position=(self.player.x, self.player.y),
                    target_position=(actualx, actualy),
                    map_tiles=self.map.tiles,
                    callback=self._update_fov,
                )

            if isinstance(action, RightClickAction):
                from .constants import color_wild

                for x, y in action.perform(self.map.player_at, self.map.tiles)[:8]:
                    self.vfx.append(
                        dict(
                            x=x,
                            y=y,
                            string="~",
                            fg=color_wild["special"],
                            bg=color_wild["bg"][0],
                        )
                    )

        # auto events
        if sum([len(ent.q) for ent in [self.player] if ent.q is not None]):
            for entity in [self.player]:
                entity.step_along(terrain=self.map.tiles)

                if entity == self.player:
                    self._update_fov()

            sleep(0.05)
            self.render()

    def render(self):
        self.console.clear()

        self.map.render(
            wide=self.view_width - 1,
            tall=self.view_height - 1,
            focus=self.player,
            console=self.console,
        )

        for fx in self.vfx:
            self.console.print(**fx)

        self.player.render(self.map.player_at, self.console)

        for npc in self.actors:
            npcx = npc.x - self.player.x + self.map.player_at[0]
            npcy = npc.y - self.player.y + self.map.player_at[1]

            if self.map.visible[npc.x, npc.y]:
                from .constants import color_wild

                self.console.print(
                    x=npcx,
                    y=npcy,
                    string="@",
                    fg=color_wild["item"][1],
                )
                # npc.render((npcx, npcy), self.console)
                self.map.tiles[npcx, npcy]["walkable"] = False

        self.window.present(self.console)
