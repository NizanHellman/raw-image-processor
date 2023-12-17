import os.path
import shutil
import tarfile
import time
from pathlib import Path
from PIL import Image
import numpy

PROJECT_PATH = os.path.join(os.path.dirname(__file__), '../')


def get_image_statistics(image):
    numpy_image = numpy.frombuffer(image, dtype=numpy.uint8)
    average_pixel_value = numpy_image.mean()
    std_of_pixel_value = numpy_image.std()
    return average_pixel_value, std_of_pixel_value


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, 'w') as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def convert_to_png_and_get_statistics(raw_folder_path, list_of_raw_files):
    image_statistics = []
    png_dir_name = f'{raw_folder_path}_png'
    os.mkdir(os.path.join(PROJECT_PATH, 'data', png_dir_name))
    with open(list_of_raw_files, 'r') as raw_files:
        for raw_file in raw_files:
            raw_file = os.path.join(PROJECT_PATH, 'data/example_frames', raw_file.strip())
            raw_file_name = Path(raw_file).stem
            with open(raw_file, 'rb') as raw_data_file:
                raw_data = raw_data_file.read()
                img_size = (1280, 720)
                img = Image.frombytes('L', img_size, raw_data)
                png_file_name = f'{raw_file_name}.png'
                img.save(os.path.join(png_dir_name, png_file_name))
                avg, std = get_image_statistics(raw_data)
                image_statistics.append({
                    'frame': png_file_name,
                    'average_pixel_value': avg,
                    'std_of_pixel_in_frame': std
                })

    return image_statistics


def extract_tar_files(tar_file_path, extract_to):
    with tarfile.open(tar_file_path, 'r') as tar_file:
        tar_file.extractall(extract_to)


def raw_image_processor(raw_tar_input_path, list_of_raw_in_tar_path):
    data_files_path = os.path.dirname(raw_tar_input_path)
    tar_name_no_ext = Path(raw_tar_input_path).stem
    extracted_tar_dir_name = os.path.join(data_files_path, tar_name_no_ext)
    extract_tar_files(raw_tar_input_path, extracted_tar_dir_name)
    image_statistics = convert_to_png_and_get_statistics(extracted_tar_dir_name, list_of_raw_in_tar_path)
    png_tar_name = f'{extracted_tar_dir_name}_png.tar'
    make_tarfile(png_tar_name, f'{extracted_tar_dir_name}_png')
    return png_tar_name, image_statistics


if __name__ == '__main__':
    start_time = time.time()
    try:
        shutil.rmtree(os.path.join(PROJECT_PATH, 'data/example_frames'))
        shutil.rmtree(os.path.join(PROJECT_PATH, 'data/example_frames_png'))
        os.remove(os.path.join(PROJECT_PATH, 'data/example_frames_png.tar'))
    except:
        pass
    raw_tar_input_path_relative = 'data/example_frames.tar'
    raw_tar_input_path = os.path.join(PROJECT_PATH, raw_tar_input_path_relative)
    list_of_raw_in_tar_path_relative = 'data/example_frames.lst'
    list_of_raw_in_tar_path = os.path.join(PROJECT_PATH, list_of_raw_in_tar_path_relative)
    print(raw_image_processor(raw_tar_input_path, list_of_raw_in_tar_path))

    print("--- %s seconds ---" % (time.time() - start_time))
