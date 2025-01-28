import uuid

import trimesh
import numpy as np
from PIL import Image

from rotation import Rotation


def get_2d_from_3d(
    glb_path: str,
    rotation: Rotation = Rotation.front,
    flip: bool = False,
) -> str:
    mesh = trimesh.load(glb_path, force="mesh")
    rotate_params = []
    match rotation:
        case Rotation.front:
            rotate_params = [np.pi / 2, [0, 1, 0]]

        case Rotation.right:
            rotate_params = [np.pi / 3, [0, 1, 0]]

        case Rotation.left:
            rotate_params = [2 * np.pi / 3, [0, 1, 0]]

        case Rotation.semi_right:
            rotate_params = [3 * np.pi / 8, [0, 1, 0]]

        case Rotation.semi_left:
            rotate_params = [5 * np.pi / 8, [0, 1, 0]]

    rotation_matrix = trimesh.transformations.rotation_matrix(*rotate_params)
    mesh.apply_transform(rotation_matrix)

    rotation_matrix = trimesh.transformations.rotation_matrix(np.pi / 18, [1, 0, 0])
    mesh.apply_transform(rotation_matrix)
    scene = mesh.scene()

    image = scene.save_image(resolution=[1920, 1080])
    img_path = f"res/result_{uuid.uuid4()}.jpg"
    with open(img_path, "wb") as f:
        f.write(image)

    if flip:
        img = Image.open(img_path).convert("RGB")
        flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        flipped_img.save(img_path)

    return img_path


if __name__ == "__main__":
    for r in list(Rotation):
        get_2d_from_3d("../res/sample.glb", r)
