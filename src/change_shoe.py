import uuid

from PIL import Image


def remove_white_background_and_crop(image):
    rgba = image.convert("RGBA")
    data = rgba.getdata()

    new_data = []
    min_x, min_y, max_x, max_y = rgba.width, rgba.height, 0, 0

    for y in range(rgba.height):
        for x in range(rgba.width):
            item = data[y * rgba.width + x]
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    rgba.putdata(new_data)
    cropped = rgba.crop((min_x, min_y, max_x + 1, max_y + 1))
    return cropped


def get_mask_bounds(mask):
    data = mask.convert("L").getdata()
    width, height = mask.size

    min_x, min_y, max_x, max_y = width, height, 0, 0

    for y in range(height):
        for x in range(width):
            if data[y * width + x] > 0:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    return min_x, min_y, max_x + 1, max_y + 1


def resize_image(image, mask, increase_px: int = 0):
    mask_bounds = get_mask_bounds(mask)
    mask_size = (
        mask_bounds[2] - mask_bounds[0] + increase_px,
        mask_bounds[3] - mask_bounds[1] + increase_px,
    )

    image.thumbnail(mask_size, Image.LANCZOS)

    new_image = Image.new("RGBA", mask_size, (0, 0, 0, 0))
    position = (
        (mask_size[0] - image.size[0]) // 2,
        (mask_size[1] - image.size[1]) // 2,
    )
    new_image.paste(image, position, image)

    return new_image


def change_shoe(
    person_path: str = "res/man.jpg",
    shoe_path: str = "res/shoe.jpg",
    mask_path: str = "res/mask.jpg",
) -> str:
    man = Image.open(person_path)
    mask = Image.open(mask_path)
    shoe = Image.open(shoe_path)

    shoe_no_bg = remove_white_background_and_crop(shoe)
    resized_shoe = resize_image(shoe_no_bg, mask)
    man_rgba = man.convert("RGB")
    result = Image.new("RGB", man.size)
    result.paste(man_rgba, (0, 0))
    mask_bounds = get_mask_bounds(mask)
    result.paste(resized_shoe, mask_bounds[:2], resized_shoe)
    result_path = f"res/result_{uuid.uuid4()}.jpg"
    result.save(result_path)

    return result_path


if __name__ == "__main__":
    change_shoe()
