#!/usr/bin/env python3
"""
Heye - A Vision Language Model CLI Tool

This tool allows you to analyze images using various AI models and get descriptive
responses about the content of those images. Configuration is persisted across runs
for convenience.
"""

import argparse
from pathlib import Path
import os
import json
import base64
import codecs

from openai import OpenAI


class Eye:
    """
    Main class for processing images with vision language models.

    Supports configuration persistence - parameters only need to be specified once
    and will be remembered for subsequent runs.
    """

    # Supported models
    SUPPORTED_MODELS = [
        "qwen3-vl-plus",
        "qwen3-vl-flash",
        "qwen-vl-ocr-latest"
    ]

    def __init__(self, image_path, query_text=None, model_name=None, base_url=None, api_token=None):
        """
        Initialize the Eye processor.

        Args:
            image_path (str): Path to the image file to analyze
            query_text (str, optional): Question or prompt for the model
            model_name (str, optional): Model to use for processing
            base_url (str, optional): API base URL
            api_token (str, optional): API token for authentication
        """
        self.config_file = Path.home() / ".heye"
        self._setup_configuration(query_text, model_name, base_url, api_token)
        # self._validate_model()

        self.image_path = image_path

        self.client = OpenAI(
            api_key=self.api_token,
            base_url=self.base_url,
        )

    def _setup_configuration(self, query_text, model_name, base_url, api_token):
        """Set up configuration from file and command line arguments."""
        config = self.load_config()

        # Update config if new values provided
        if base_url is not None:
            config['base_url'] = base_url
        if api_token is not None:
            config['api_token'] = api_token
        if model_name is not None:
            config['model_name'] = model_name
        if query_text is not None:
            config['query_text'] = query_text

        # Save config if any new values were provided
        if base_url is not None or api_token is not None or model_name is not None or query_text is not None:
            self.save_config(config)

        # Use config values or defaults
        self.base_url = config.get(
            'base_url', "https://dashscope.aliyuncs.com/compatible-mode/v1")
        self.api_token = config.get(
            'api_token', os.getenv('DASHSCOPE_API_KEY'))
        self.model_name = model_name or config.get(
            'model_name', "qwen3-vl-plus")
        self.query_text = query_text or config.get(
            'query_text', "What scene is depicted in the image?")

    def _validate_model(self):
        """Validate that the selected model is supported."""
        if self.model_name not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Unsupported model: {self.model_name}. Supported models are: {', '.join(self.SUPPORTED_MODELS)}")

    # Configuration methods
    def load_config(self):
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                # Use codecs to ensure proper encoding handling
                with codecs.open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError, UnicodeDecodeError):
                return {}
        return {}

    def save_config(self, config):
        """Save configuration to file with proper Unicode handling."""
        try:
            # Use codecs to ensure proper encoding handling
            with codecs.open(self.config_file, 'w', encoding='utf-8') as f:
                # Use ensure_ascii=False to prevent Unicode escaping
                json.dump(config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save config to {self.config_file}: {e}")

    # Image processing methods
    def validate_image(self, image_path):
        """Validate that the image file exists and is of a supported format."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"{image_path} does not exist.")

        # Supported image formats (excluding GIF)
        supported_extensions = (".png", ".jpg", ".jpeg",
                                ".bmp", ".webp", ".tiff", ".tif")
        if not image_path.lower().endswith(supported_extensions):
            raise ValueError(
                f"{image_path} is not a valid image file. Supported formats: PNG, JPG, JPEG, BMP, WEBP, TIFF, TIF")

    def encode_image(self, image_path):
        """Encode image file to base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def get_image_content_type(self, image_path):
        """Get the correct content type based on file extension."""
        extension = image_path.lower().split('.')[-1]
        content_types = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'bmp': 'image/bmp',
            'webp': 'image/webp',
            'tiff': 'image/tiff',
            'tif': 'image/tiff'
        }
        return content_types.get(extension, 'image/png')

    def send_messages(self, messages):
        """Send messages to the model API."""
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            stream=True,
        )

    def process_query(self):
        """Process the image query and stream the response."""
        self.validate_image(self.image_path)
        base64_image = self.encode_image(self.image_path)
        content_type = self.get_image_content_type(self.image_path)

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{content_type};base64,{base64_image}"},
                    },
                    {"type": "text", "text": self.query_text},
                ],
            }
        ]

        stream = self.send_messages(messages)
        assistant_content = ""

        for chunk in stream:
            delta = chunk.choices[0].delta

            if delta.content:
                print(delta.content, end="")
                assistant_content += delta.content


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Process an image with VL model")
    parser.add_argument(
        "query", nargs='*', help="Query text for the image (only needs to be specified once, will be remembered)")
    parser.add_argument("-p", "--path", required=True,
                        help="Path to the image file")
    parser.add_argument("-m", "--model", default=None,
                        choices=["qwen3-vl-plus", "qwen3-vl-flash",
                                 "qwen-vl-ocr-latest"],
                        help="Model name to use for processing (only needs to be specified once, will be remembered)")
    parser.add_argument("--base-url", default=None,
                        help="API base URL (only needs to be specified once, will be remembered)")
    parser.add_argument("--api-token", default=None,
                        help="API token for authentication (only needs to be specified once, will be remembered)")

    args = parser.parse_args()

    # Process query text
    args.query = " ".join(args.query) if args.query else None

    return args


def main():
    """Main entry point."""
    try:
        args = parse_args()
        eye = Eye(args.path, args.query, args.model,
                  args.base_url, args.api_token)
        eye.process_query()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    main()
