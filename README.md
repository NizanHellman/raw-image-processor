# raw-image-processor
raw-image-processor is a versatile tool designed for processing raw binary image data. This Python script facilitates the conversion of raw image files to the widely supported PNG format. The processor handles tar archives, extracting contents, performing the conversion, and repackaging the results into a new tar archive.

## CI Status

[![Build Status](https://github.com/NizanHellman/raw-image-processor/workflows/Run%20Tests/badge.svg)](https://github.com/NizanHellman/raw-image-processor/actions)


## Installation

To install `raw-image-processor`, use the following command:

```bash
pip install raw-image-processor
```

## Usage

To use `raw-image-processor`, import the `raw_image_processor` function and call it with the necessary parameters:

```python
import json
from raw_image_processor import raw_image_processor


def convert_raw_to_png():
    input_path = 'path/to/your/example_frames.tar'
    output_path, frame_statistics = raw_image_processor(input_path=input_path)
    print(f'Output path: {output_path}')
    print(f'Image statistics:\n{json.dumps(frame_statistics, indent=2)}')


if __name__ == '__main__':
    convert_raw_to_png()
```
### Inputs:
* `input_path` (required): Path to the raw tar file.
* `output_path` (optional): Output path for the PNG tar file. Defaults to the same location as the input.
* `img_size` (optional): Tuple specifying the image size. Defaults to (1280, 720).
* `threads` (optional): Number of threads the program will use. Defaults to 10.
### Outputs:
* `output_path` (str): The PNG tar file's output path.
* `frame_statistics` (list of dict): An array with statistics for each frame.

Each element in frame_statistics is a dictionary with the following structure:
```python
{
    'frame': 'some_frame_filename.png',
    'average_pixel_value': 125.46891927083334,
    'std_of_pixel_in_frame': 63.446946355756324
}
```
## Solution Overview

The `raw-image-processor` follows a sequential process for efficient raw image data conversion:

### 1. File Extraction and Object Building

- Extracts files from the raw tar archive.
- Constructs an object for each .raw file with filename, image size, and raw data.

### 2. PNG Conversion and Statistics Calculation

- Converts raw images to PNG format and calculates statistics.
- Multi-threaded for improved efficiency.
- Utilizes Numpy for average pixel value and standard deviation per frame.

### 3. Tar File Creation

- Generates a tar file from temporary directories containing PNG images.

## Build and Run Locally

To run the `raw-image-processor` locally, follow these steps:

### Clone the Repository

```bash
git clone https://github.com/your-username/raw-image-processor.git
cd raw-image-processor
```

### Initialize Poetry
```bash
poetry init
```

### Install Dependencies
```bash
poetry install
```

### Activate Virtual Environment
```bash
poetry shell
```

### Run Tests
```bash
poetry run pytest
```

### Run with CLI (Interactive)
```bash
poetry run convert-images
```
or
```bash
poetry run python raw_image_processor/convert_images.py
```
* The CLI is interactive and will prompt you for the required inputs.
* The output will be displayed in the terminal.


## TODO

- **Git Workflow for Automated Tests:**
  - Implement a CI workflow to run tests automatically for every commit.
  - Configure the workflow to execute your test suite on each pull request and push event.
