from .tinypng_node import TinyPNGCompressNode

NODE_CLASS_MAPPINGS = {
    "TinyPNGCompress": TinyPNGCompressNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TinyPNGCompress": "TinyPNG Compress",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]