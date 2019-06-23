import cocos


class RepeatingEvent:
    """Repeat a tile animation endlessly."""

    ANIMATIONS = dict()
    ANIMATIONS["flowers_yb"] = {"file": "flowers_yb.png", "row": 1, "col": 8}
    ANIMATIONS["flowers_ry"] = {"file": "flowers_ry.png", "row": 1, "col": 8}

    def __init__(self, map_scene, object: cocos.tiles.TmxObject) -> None:
        """Create an event repeating a tile animation endlessly.

        :param map_scene: The scene containing the map.
        :param object: The object containing all the info about the event.
        """

        if "animation" in object.properties:
            map_scene.repeating_animation(object.px, object.py,
                                          RepeatingEvent.ANIMATIONS[object.properties["animation"]])
