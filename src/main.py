from change_shoe import change_shoe
from inpaint import remove_shoes
from jpg2glb import get_3d_from_2d
from mask import get_left_right_shoes_masks
from glb2jpg import get_2d_from_3d
from rotation import Rotation, predict_rotation
import os


def shoe_vton_pipeline(
    person_path: str = "res/man.jpg",
    shoe_path: str = "res/shoe.jpg",
) -> str:
    left_mask, right_mask, both_mask = get_left_right_shoes_masks(person_path)

    left_rotation: Rotation = predict_rotation(
        person_path, left_mask
    )  # TODO: implement
    right_rotation: Rotation = predict_rotation(
        person_path, right_mask
    )  # TODO: implement

    glb_path = get_3d_from_2d(shoe_path)  # TODO: implement

    left_shoe_path = get_2d_from_3d(glb_path, left_rotation)
    right_shoe_path = get_2d_from_3d(
        glb_path,
        right_rotation,
        flip=True,
    )
    removed_shoes_path = remove_shoes(
        person_path,
        both_mask,
    )
    one_shoe_path = change_shoe(removed_shoes_path, left_shoe_path, left_mask)
    result_path = change_shoe(one_shoe_path, right_shoe_path, right_mask)
    for tmp_path in (
        left_mask,
        right_mask,
        both_mask,
        left_shoe_path,
        removed_shoes_path,
        right_shoe_path,
        one_shoe_path,
    ):
        os.remove(tmp_path)

    return result_path


if __name__ == "__main__":
    path = shoe_vton_pipeline("res/person.jpg", "res/puma-green.jpg")
    print(path)
