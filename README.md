# Background Removal Service

[![Python application test with Github Actions](https://github.com/blueskycircle/background-removal/actions/workflows/main.yml/badge.svg)](https://github.com/blueskycircle/background-removal/actions/workflows/main.yml)

A command-line tool for removing backgrounds from images using the rembg library.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Installing from source](#installing-from-source)
- [Usage](#usage)
  - [Basic Commands](#basic-commands)
    - [Show tool information](#show-tool-information)
    - [Remove background from a single image](#remove-background-from-a-single-image)
    - [Batch process all images in a directory](#batch-process-all-images-in-a-directory)
  - [Command Options](#command-options)
    - [Remove Command](#remove-command)
    - [Batch Command](#batch-command)

## Features

- Remove backgrounds from images with a single command
- Replace transparent backgrounds with solid colors
- Process individual images or entire directories
- Support for recursive directory processing
- PNG and JPEG output formats

## Installation

### Prerequisites

- Python 3.7 or higher

### Installing from source

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd bg-removal-service
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Commands

#### Show tool information
```bash
python cli.py info
```

#### Remove background from a single image
```bash
python cli.py remove input.jpg output.png
```

#### Batch process all images in a directory
```bash
python cli.py batch input_folder output_folder
```

### Command Options

#### Remove Command

```bash
python cli.py remove INPUT_PATH [OUTPUT_PATH] [OPTIONS]
```

- `INPUT_PATH`: Path to the input image
- `OUTPUT_PATH`: (Optional) Path where the processed image will be saved
  - If not provided, output will be saved as "[original]_output.[format]"

Options:
- `--format`, `-f`: Output format (PNG or JPEG) [default: PNG]
- `--bg-color`, `-c`: Replace transparent background with color as RGB values (e.g., 255 0 0 for red)

Examples:
```bash
# Remove background and keep transparency (PNG)
python cli.py remove photo.jpg

# Remove background and save as JPEG
python cli.py remove photo.jpg result.jpg --format JPEG

# Remove background and replace with red
python cli.py remove photo.jpg result.png --bg-color 255 0 0
```

#### Batch Command

```bash
python cli.py batch INPUT_DIR [OUTPUT_DIR] [OPTIONS]
```

- `INPUT_DIR`: Directory containing images to process
- `OUTPUT_DIR`: (Optional) Directory where processed images will be saved
  - If not provided, output will be saved to "[input_dir]_output"

Options:
- `--format`, `-f`: Output format (PNG or JPEG) [default: PNG]
- `--recursive/--no-recursive`: Process subdirectories recursively [default: False]
- `--bg-color`, `-c`: Replace transparent background with color as RGB values

Examples:
```bash
# Process all images in a directory
python cli.py batch photos

# Process all images and subdirectories
python cli.py batch photos processed --recursive

# Process all images and convert to JPEG
python cli.py batch photos --format JPEG

# Process all images and replace background with blue color
python cli.py batch photos --bg-color 37 150 190
```
