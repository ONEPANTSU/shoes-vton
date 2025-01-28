import uuid

from simple_lama_inpainting import SimpleLama
from PIL import Image
import cv2


def remove_shoes(
    img_path: str,
    mask_path: str,
) -> str:
    path = f"res/removed_shoes_{uuid.uuid4()}.jpg"

    # Using OpenCV
    img = cv2.imread(img_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

    cv2.imwrite(path, img)

    # Using Lama
    simple_lama = SimpleLama()
    image = Image.open(path).convert("RGB")
    mask = Image.open(mask_path).convert("L")

    result = simple_lama(image, mask).resize(image.size)
    result.save(path)
    return path
