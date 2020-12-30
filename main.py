def main():
    from engine import Engine

    engine = Engine(
        width=80,
        height=50,
        view_width=60,
        view_height=50,
        tileset="Anno_16x16.png",
        title="Squad RL",
    )

    while True:
        engine.event_loop()
        engine.render()


if __name__ == "__main__":
    main()
