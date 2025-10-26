# Heye - Vision Language Model CLI Tool

In Liu Cixin's science fiction novella "Taking Her Eyes" (《带上她的眼睛》), the protagonist carries with him a pair of eyes - those of a young woman trapped in an underground world, seeing the surface world through his experiences. Just as those eyes allowed someone to see beyond their immediate surroundings, Heye allows you to see beyond the surface of your images through the power of artificial intelligence.

Heye is a command-line interface tool for interacting with vision language models (VLMs). It allows you to analyze images using various AI models and get descriptive responses about the content of those images.

## Features

- Support for multiple vision language models
- Command-line interface for easy usage
- Configuration persistence for ALL settings (set once, remembered forever)
- Image validation and error handling
- Streaming responses for real-time output
- Unicode support for international characters

## Supported Models

- `qwen3-vl-plus`
- `qwen3-vl-flash`
- `qwen-vl-ocr-latest`

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your API key as an environment variable:
   ```
   export DASHSCOPE_API_KEY=your_api_key_here
   ```

## Usage

Basic usage:
```bash
python heye.py -p path/to/image.jpg "Describe this image"
```

### Command Line Arguments

- `-p`, `--path` (required): Path to the image file to analyze
- `query` (optional): Question or prompt for the model (default: "What scene is depicted in the image?")
- `-m`, `--model` (optional): Model to use for processing (default: qwen3-vl-plus)
- `--base-url` (optional): API base URL
- `--api-token` (optional): API token for authentication

### Configuration Persistence

The tool saves ALL your configuration in `~/.heye` file. **Important:** All parameters (`--base-url`, `--api-token`, `--model`, and `query`) only need to be configured once and will be remembered for all future runs.

First run with custom settings:
```bash
python heye.py --base-url "https://your-api-endpoint.com" --api-token "your-token" -m "qwen3-vl-plus" -p image.jpg "Describe this image in detail"
```

Subsequent runs (uses ALL saved configuration - no need to specify the same parameters again):
```bash
python heye.py -p image.jpg
```

This makes it even more convenient for daily use - after initial setup, you only need to provide the image path!

### Examples

1. Basic image analysis:
   ```bash
   python heye.py -p photo.jpg "What's in this picture?"
   ```

2. Using a specific model (only needed once, will be remembered):
   ```bash
   python heye.py -p diagram.png -m "qwen3-vl-flash"
   ```

3. With custom API settings (only needed once, will be remembered):
   ```bash
   python heye.py --base-url "https://your-api.com" --api-token "your-token" -p chart.jpg
   ```

4. After initial configuration, simply:
   ```bash
   python heye.py -p another_image.jpg
   ```

## Supported Image Formats

- PNG
- JPG/JPEG
- BMP
- WEBP
- TIFF/TIF

## Error Handling

The tool provides user-friendly error messages for common issues:
- File not found errors
- Invalid image format errors
- API connection errors
- Unsupported model errors

## Environment Variables

- `DASHSCOPE_API_KEY`: Your DashScope API key (can be overridden with --api-token)

## Requirements

- Python 3.10+
- openai Python package
- Access to a supported vision language model API

## License

MIT