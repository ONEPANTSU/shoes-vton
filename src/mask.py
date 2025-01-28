from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation
from PIL import Image
import torch.nn as nn
import torch
from torchvision.utils import save_image
import uuid
import cv2
import numpy as np


def get_left_right_shoes_masks(person_path: str) -> tuple[str, str, str]:
    processor = SegformerImageProcessor.from_pretrained(
        "mattmdjaga/segformer_b2_clothes"
    )
    model = AutoModelForSemanticSegmentation.from_pretrained(
        "mattmdjaga/segformer_b2_clothes"
    )

    image = Image.open(person_path)
    inputs = processor(images=image, return_tensors="pt")

    outputs = model(**inputs)
    logits = outputs.logits.cpu()

    upsampled_logits = nn.functional.interpolate(
        logits,
        size=image.size[::-1],
        mode="bilinear",
        align_corners=False,
    )

    pred_seg = upsampled_logits.argmax(dim=1)[0]
    filtered_seg = torch.where((pred_seg == 9), 255, 0).byte()
    left_path = f"res/left_mask_{uuid.uuid4()}.jpg"
    save_image(filtered_seg.float(), left_path)
    dilate_mask(left_path)

    filtered_seg = torch.where((pred_seg == 10), 255, 0).byte()
    right_path = f"res/right_mask_{uuid.uuid4()}.jpg"
    save_image(filtered_seg.float(), right_path)
    dilate_mask(right_path)

    filtered_seg = torch.where((pred_seg == 9) | (pred_seg == 10), 255, 0).byte()
    both_path = f"res/left_right_mask_{uuid.uuid4()}.jpg"
    save_image(filtered_seg.float(), both_path)
    dilate_mask(both_path)

    return left_path, right_path, both_path


def dilate_mask(mask_path, dilation_percent=2):
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    height, width = mask.shape

    kernel_size = int(min(height, width) * dilation_percent / 100)

    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    dilated_mask = cv2.dilate(mask, kernel, iterations=1)

    cv2.imwrite(mask_path, dilated_mask)
