# Heye - 视觉语言模型命令行工具

在刘慈欣的科幻小说《带上她的眼睛》中，主人公携带了一双眼睛——一位被困在地下世界的年轻女孩的眼睛，通过他的经历来观察地表世界。正如那双眼睛让某个人能够看到超出自己 immediate surroundings 的事物一样，Heye 通过人工智能的力量让你能够看到图像表面之外的内容。

Heye 是一个用于与视觉语言模型 (VLM) 交互的命令行界面工具。它允许你使用各种 AI 模型分析图像，并获得关于图像内容的描述性响应。

## 功能特性

- 支持多种视觉语言模型
- 命令行界面，易于使用
- 所有设置的配置持久化（一次性设置，永久记住）
- 图像验证和错误处理
- 实时流式响应
- 国际字符的 Unicode 支持

## 支持的模型

- `qwen3-vl-plus`
- `qwen3-vl-flash`
- `qwen-vl-ocr-latest`

## 安装

1. 克隆仓库：
   ```
   git clone <repository-url>
   ```

2. 安装所需依赖：
   ```
   pip install -r requirements.txt
   ```

3. 设置环境变量中的 API 密钥：
   ```
   export DASHSCOPE_API_KEY=your_api_key_here
   ```

## 使用方法

基本用法：
```bash
python heye.py -p path/to/image.jpg "描述这张图片"
```

### 命令行参数

- `-p`, `--path` (必需): 要分析的图像文件路径
- `query` (可选): 模型的问题或提示 (默认: "图中描绘的是什么景象?")
- `-m`, `--model` (可选): 用于处理的模型 (默认: qwen3-vl-plus)
- `--base-url` (可选): API 基础 URL
- `--api-token` (可选): API 认证令牌

### 配置持久化

工具会将所有配置保存在 `~/.heye` 文件中。**重要提示:** 所有参数 (`--base-url`, `--api-token`, `--model`, 和查询文本) 只需要配置一次，就会在所有后续运行中被记住。

首次运行时设置自定义配置：
```bash
python heye.py --base-url "https://your-api-endpoint.com" --api-token "your-token" -m "qwen3-vl-plus" -p image.jpg "详细描述这张图片"
```

后续运行 (使用所有已保存的配置 - 无需再次指定相同参数)：
```bash
python heye.py -p image.jpg
```

这使得日常使用更加便捷 - 初始设置后，你只需要提供图像路径！

### 示例

1. 基本图像分析：
   ```bash
   python heye.py -p photo.jpg "图片里有什么?"
   ```

2. 使用特定模型 (只需要一次，会被记住)：
   ```bash
   python heye.py -p diagram.png -m "qwen3-vl-flash"
   ```

3. 使用自定义 API 设置 (只需要一次，会被记住)：
   ```bash
   python heye.py --base-url "https://your-api.com" --api-token "your-token" -p chart.jpg
   ```

4. 初始配置后，只需：
   ```bash
   python heye.py -p another_image.jpg
   ```

## 支持的图像格式

- PNG
- JPG/JPEG
- BMP
- WEBP
- TIFF/TIF

## 错误处理

工具为常见问题提供用户友好的错误消息：
- 文件未找到错误
- 无效图像格式错误
- API 连接错误
- 不支持的模型错误

## 环境变量

- `DASHSCOPE_API_KEY`: 你的 DashScope API 密钥 (可以被 --api-token 覆盖)

## 环境要求

- Python 3.10+
- openai Python 包
- 访问受支持的视觉语言模型 API

## 许可证

MIT