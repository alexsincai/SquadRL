class Actor:
    def __init__(self, x, y, icon="@", controlled=False):
        self.x = x
        self.y = y
        self.icon = icon
        self.controlled = controlled
        self.q = []

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def step_along(self, terrain):
        mx, my = self.q.pop()
        mx -= self.x
        my -= self.y
        self.move(mx, my)

    def render(self, pos, console):
        from .constants import color_wild

        x, y = pos
        console.print(
            x=x,
            y=y,
            string=self.icon,
            fg=color_wild["character"][1],
            bg=color_wild["bg"][0],
        )
