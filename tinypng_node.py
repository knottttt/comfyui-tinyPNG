import io
from typing import List, Tuple

import numpy as np
import torch
from PIL import Image

try:
    import tinify
except Exception:  # pragma: no cover
    tinify = None


def _tensor_to_pil(image_tensor: torch.Tensor) -> Image.Image:
    image_np = image_tensor.detach().cpu().numpy()
    image_np = np.clip(image_np * 255.0, 0, 255).astype(np.uint8)

    if image_np.ndim != 3:
        raise ValueError(f"Expected HWC image tensor, got shape {image_np.shape}.")

    channels = image_np.shape[2]
    if channels == 1:
        return Image.fromarray(image_np[:, :, 0], mode="L")
    if channels == 3:
        return Image.fromarray(image_np, mode="RGB")
    if channels == 4:
        return Image.fromarray(image_np, mode="RGBA")

    raise ValueError(f"Unsupported channel count: {channels}")


def _pil_to_tensor(image: Image.Image) -> torch.Tensor:
    # Keep alpha channel when present to avoid turning transparent areas into black.
    if "A" in image.getbands():
        out = image.convert("RGBA")
    else:
        out = image.convert("RGB")
    image_np = np.asarray(out).astype(np.float32) / 255.0
    return torch.from_numpy(image_np)


def _tiny_resize(source, method: str, width: int, height: int):
    if method == "scale":
        options = {"method": method}
        if width > 0:
            options["width"] = width
        elif height > 0:
            options["height"] = height
        else:
            return source
        return source.resize(**options)

    if width <= 0 or height <= 0:
        return source

    return source.resize(method=method, width=width, height=height)


class TinyPNGCompressNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "operation": (["compress", "smart_resize"], {"default": "compress"}),
                "resize_method": (["scale", "fit", "cover", "thumb"], {"default": "scale"}),
                "width": ("INT", {"default": 0, "min": 0, "max": 16384, "step": 1}),
                "height": ("INT", {"default": 0, "min": 0, "max": 16384, "step": 1}),
                "preserve_copyright": ("BOOLEAN", {"default": False}),
                "preserve_creation": ("BOOLEAN", {"default": False}),
                "preserve_location": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "info")
    FUNCTION = "run"
    CATEGORY = "image/TinyPNG"

    def run(
        self,
        image: torch.Tensor,
        api_key: str,
        operation: str,
        resize_method: str,
        width: int,
        height: int,
        preserve_copyright: bool,
        preserve_creation: bool,
        preserve_location: bool,
    ) -> Tuple[torch.Tensor, str]:
        if tinify is None:
            raise RuntimeError("Missing dependency: tinify. Please `pip install -r requirements.txt`.")

        key = (api_key or "").strip()
        if not key:
            raise ValueError("TinyPNG API key is required.")

        tinify.key = key

        preserve_items: List[str] = []
        if preserve_copyright:
            preserve_items.append("copyright")
        if preserve_creation:
            preserve_items.append("creation")
        if preserve_location:
            preserve_items.append("location")

        output_batch = []
        total_in = 0
        total_out = 0

        for idx in range(image.shape[0]):
            pil_image = _tensor_to_pil(image[idx])
            raw_buf = io.BytesIO()
            pil_image.save(raw_buf, format="PNG")
            input_bytes = raw_buf.getvalue()
            total_in += len(input_bytes)

            source = tinify.from_buffer(input_bytes)
            if preserve_items:
                source = source.preserve(*preserve_items)

            if operation == "smart_resize":
                source = _tiny_resize(source, resize_method, width, height)

            output_bytes = source.to_buffer()
            total_out += len(output_bytes)

            output_pil = Image.open(io.BytesIO(output_bytes))
            output_batch.append(_pil_to_tensor(output_pil))

        output_tensor = torch.stack(output_batch, dim=0)

        ratio = 0.0
        if total_in > 0:
            ratio = 1.0 - (total_out / float(total_in))

        info = (
            f"batch={image.shape[0]}, input={total_in} bytes, output={total_out} bytes, "
            f"saved={ratio * 100.0:.2f}%"
        )

        return (output_tensor, info)
