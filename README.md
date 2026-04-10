# ComfyUI TinyPNG

A ComfyUI custom node for compressing images via the TinyPNG API.

一个基于 TinyPNG API 的 ComfyUI 自定义节点，用于在工作流中直接压缩图片。

## Features / 功能

- Compress image batches in ComfyUI (`IMAGE`) / 支持 ComfyUI 图像批量压缩
- TinyPNG smart resize methods: `scale`, `fit`, `cover`, `thumb` / 支持 TinyPNG 智能缩放与裁切
- Optional metadata preserve (`copyright`, `creation`, `location`) / 可选保留元数据
- Returns compression stats text (`info`) / 输出压缩统计信息

## Installation / 安装

### Install with ComfyUI Manager / 通过 ComfyUI Manager 安装

1. Open `ComfyUI Manager` -> `Extension Manager`.
2. Search `ComfyUI TinyPNG` or `comfyui-tinypng`.
3. Install and restart ComfyUI.

1. 打开 `ComfyUI Manager` -> `Extension Manager`
2. 搜索 `ComfyUI TinyPNG` 或 `comfyui-tinypng`
3. 安装后重启 ComfyUI

### Manual install / 手动安装

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/knottttt/comfyui-tinyPNG.git
cd comfyui-tinyPNG
pip install -r requirements.txt
```

Then restart ComfyUI. / 然后重启 ComfyUI。

## Usage / 使用说明

- Add node: `TinyPNG Compress`
- Required: TinyPNG API key from <https://tinypng.com/developers>
- `operation=compress` for compression only
- `operation=smart_resize` with `resize_method` for TinyPNG resizing

- 节点名：`TinyPNG Compress`
- 必须填写 TinyPNG API Key：<https://tinypng.com/developers>
- `operation=compress` 仅压缩
- `operation=smart_resize` 配合 `resize_method` 做智能缩放/裁切

## Screenshot / 节点截图

Add screenshot file to repository and update this section, e.g. `assets/screenshot.png`.

请将节点截图放入仓库（例如 `assets/screenshot.png`）并替换此占位说明。

## License

MIT. See [LICENSE](./LICENSE).