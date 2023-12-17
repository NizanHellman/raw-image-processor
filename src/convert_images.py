import os.path
import shutil
import tarfile
import time
from pathlib import Path
from PIL import Image
import numpy

PROJECT_PATH = os.path.join(os.path.dirname(__file__), '../')
TEMP_OUTPUT_FOLDER = 'example_frames_png'
TEMP_OUTPUT_PATH = os.path.join(PROJECT_PATH, 'data', TEMP_OUTPUT_FOLDER)


def get_image_statistics(image):
    numpy_image = numpy.frombuffer(image, dtype=numpy.uint8)
    average_pixel_value = numpy_image.mean()
    std_of_pixel_value = numpy_image.std()
    return average_pixel_value, std_of_pixel_value


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, 'w') as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def process_raw_file(raw_data_file):
    raw_file_name = Path(raw_data_file.entry_name).stem
    raw_data = raw_data_file.read()
    img_size = (1280, 720)
    img = Image.frombytes('L', img_size, raw_data)
    png_file_name = f'{raw_file_name}.png'
    img.save(os.path.join(TEMP_OUTPUT_PATH, png_file_name))
    avg, std = get_image_statistics(raw_data)
    frame_obj = {
        'frame': png_file_name,
        'average_pixel_value': avg,
        'std_of_pixel_in_frame': std
    }
    return frame_obj


def convert_to_png_and_get_statistics(raw_files):
    image_statistics = []
    os.mkdir(TEMP_OUTPUT_PATH)
    for raw_file in raw_files:
        image_statistics.append(process_raw_file(raw_file))

    return image_statistics


def extract_tar_files(tar_file_path):
    with tarfile.open(tar_file_path, 'r') as tar_file:
        for entry in tar_file:
            with tar_file.extractfile(entry) as raw_file:
                raw_file.entry_name = entry.name
                raw_file.temp_folder = 'example_frames_png'
                yield raw_file


def raw_image_processor(raw_tar_input_path):
    data_files_path = os.path.dirname(raw_tar_input_path)
    tar_name_no_ext = Path(raw_tar_input_path).stem
    extracted_tar_dir_name = os.path.join(data_files_path, tar_name_no_ext)
    raw_files = extract_tar_files(raw_tar_input_path)
    image_statistics = convert_to_png_and_get_statistics(raw_files)
    png_tar_name = f'{extracted_tar_dir_name}_png.tar'
    make_tarfile(png_tar_name, f'{extracted_tar_dir_name}_png')
    return png_tar_name, image_statistics


if __name__ == '__main__':
    start_time = time.time()
    try:
        shutil.rmtree(os.path.join(PROJECT_PATH, 'data/example_frames_png'))
    except:
        pass
    try:
        os.remove(os.path.join(PROJECT_PATH, 'data/example_frames_png.tar'))
    except:
        pass
    raw_tar_input_path_relative = 'data/example_frames.tar'
    raw_tar_input_path = os.path.join(PROJECT_PATH, raw_tar_input_path_relative)
    print(raw_image_processor(raw_tar_input_path))

    print("--- %s seconds ---" % (time.time() - start_time))
