from numpy import array, dtype, int32, bool as nbool
from .constants import color_wild

graphic_dt = dtype([("ch", int32), ("fg", "3B"), ("bg", "3B")])

tile_dt = dtype(
    [
        ("lit", graphic_dt),
        ("dark", graphic_dt),
        ("walkable", nbool),
        ("transparent", nbool),
    ]
)


def make_tile(icon, color, walkable, transparent):
    lit = (ord(icon), color[0], color[2])
    dark = (ord(icon), color[1], color[2])

    return array((lit, dark, walkable, transparent), dtype=tile_dt)


hidden = array((ord(" "), color_wild["bg"][0], color_wild["bg"][0]), dtype=graphic_dt)

wild_ground = [
    make_tile(
        " ", (color_wild["bg"][0], color_wild["bg"][0], color_wild["bg"][0]), True, True
    ),
    make_tile(
        ".", (color_wild["bg"][1], color_wild["bg"][0], color_wild["bg"][0]), True, True
    ),
]

wild_feature = [
    make_tile(
        " ", (color_wild["bg"][0], color_wild["bg"][0], color_wild["bg"][0]), True, True
    ),
    make_tile(
        ".", (color_wild["bg"][1], color_wild["bg"][0], color_wild["bg"][0]), True, True
    ),
    make_tile(
        ":",
        (color_wild["item"][0], color_wild["bg"][1], color_wild["bg"][0]),
        False,
        True,
    ),
]

wild_blocker = [
    make_tile(
        "#",
        (color_wild["item"][0], color_wild["bg"][0], color_wild["bg"][0]),
        False,
        True,
    ),
    make_tile(
        "T",
        (color_wild["item"][0], color_wild["bg"][1], color_wild["bg"][0]),
        False,
        False,
    ),
    make_tile(
        "Y",
        (color_wild["item"][1], color_wild["bg"][1], color_wild["bg"][0]),
        False,
        False,
    ),
    make_tile(
        "*",
        (color_wild["item"][2], color_wild["item"][0], color_wild["bg"][0]),
        False,
        True,
    ),
]
