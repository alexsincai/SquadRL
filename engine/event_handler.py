import tcod.event as e
from .actions import *


class EventHandler(e.EventDispatch[Action]):
    def ev_quit(self, event: e.Quit):
        return EscapeAction()

    def ev_keydown(self, event: e.KeyDown):
        action = None

        key = event.sym

        if key == e.K_ESCAPE:
            action = EscapeAction()

        MOVE_KEYS = {
            e.K_UP: (0, -1),
            e.K_w: (0, -1),
            e.K_DOWN: (0, 1),
            e.K_s: (0, 1),
            e.K_LEFT: (-1, 0),
            e.K_a: (-1, 0),
            e.K_RIGHT: (1, 0),
            e.K_d: (1, 0),
        }

        if key in MOVE_KEYS:
            action = MoveAction(*MOVE_KEYS[key])

        return action

    def ev_mousebuttondown(self, event: e.MouseButtonDown):
        if event.button == 1:
            return ClickAction(*event.tile)

        if event.button == 3:
            return RightClickAction(*event.tile)
