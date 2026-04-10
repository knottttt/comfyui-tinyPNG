# ComfyUI TinyPNG

Language / 语言: [English](./README.md) | [中文](./README_zh.md)

一个基于 TinyPNG API 的 ComfyUI 自定义节点，用于在工作流中直接压缩图片。

## 功能

- 支持 ComfyUI 图像批量压缩（`IMAGE`）
- 支持 TinyPNG 智能缩放与裁切：`scale`、`fit`、`cover`、`thumb`
- 可选保留元数据：`copyright`、`creation`、`location`
- 输出压缩统计信息（`info`）

## 安装

### 通过 ComfyUI Manager 安装

1. 打开 `ComfyUI Manager` -> `Extension Manager`
2. 搜索 `ComfyUI TinyPNG` 或 `comfyui-tinypng`
3. 安装后重启 ComfyUI

### 手动安装

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/knottttt/comfyui-tinyPNG.git
cd comfyui-tinyPNG
pip install -r requirements.txt
```

然后重启 ComfyUI。

## 使用说明

- 节点名：`TinyPNG Compress`
- 必须填写 TinyPNG API Key：<https://tinypng.com/developers>
- `operation=compress`：仅压缩
- `operation=smart_resize`：配合 `resize_method` 做智能缩放/裁切

## 截图

请将节点截图放入仓库（例如 `assets/screenshot.png`）并替换此占位说明。

## 致谢

- 本项目灵感与实现思路参考自 [TinyGUI](https://github.com/chenjing1294/TinyGUI)。

## 许可证

MIT，详见 [LICENSE](./LICENSE)。