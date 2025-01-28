from enum import Enum
import random


class Rotation(str, Enum):
    front = "front"
    left = "left"
    right = "right"
    semi_right = "semi_right"
    semi_left = "semi_left"


def predict_rotation(person_path: str, mask_path: str) -> Rotation:
    # TODO: train classifier
    # return Rotation.semi_left
    return random.choice([Rotation.semi_left, Rotation.left])
