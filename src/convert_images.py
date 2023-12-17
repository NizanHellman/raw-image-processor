import os.path
import shutil
import tarfile
import time
from pathlib import Path
from PIL import Image

PROJECT_PATH = os.path.join(os.path.dirname(__file__), '../')


def convert_to_png(raw_folder_path, list_of_raw_files):
    png_dir_name = f'{raw_folder_path}_png'
    os.mkdir(os.path.join(PROJECT_PATH, 'data', png_dir_name))
    with open(list_of_raw_files, 'r') as raw_files:
        for raw_file in raw_files:
            raw_file = os.path.join(PROJECT_PATH, 'data/example_frames', raw_file.strip())
            raw_file_name = Path(raw_file).stem
            with open(raw_file, 'rb') as raw_data:
                img_size = (1280, 720)
                img = Image.frombytes('L', img_size, raw_data.read())
                img.save(os.path.join(png_dir_name, f'{raw_file_name}.png'))


def extract_tar_files(tar_file_path, extract_to):
    with tarfile.open(tar_file_path, 'r') as tar_file:
        tar_file.extractall(extract_to)


def raw_image_processor(raw_tar_input_path, list_of_raw_in_tar_path):
    data_files_path = os.path.dirname(raw_tar_input_path)
    tar_name_no_ext = Path(raw_tar_input_path).stem
    extracted_tar_dir_name = os.path.join(data_files_path, tar_name_no_ext)
    extract_tar_files(raw_tar_input_path, extracted_tar_dir_name)
    convert_to_png(extracted_tar_dir_name, list_of_raw_in_tar_path)


if __name__ == '__main__':
    start_time = time.time()
    try:
        shutil.rmtree(os.path.join(PROJECT_PATH, 'data/example_frames'))
        shutil.rmtree(os.path.join(PROJECT_PATH, 'data/example_frames_png'))
    except:
        pass
    raw_tar_input_path_relative = 'data/example_frames.tar'
    raw_tar_input_path = os.path.join(PROJECT_PATH, raw_tar_input_path_relative)
    list_of_raw_in_tar_path_relative = 'data/example_frames.lst'
    list_of_raw_in_tar_path = os.path.join(PROJECT_PATH, list_of_raw_in_tar_path_relative)
    raw_image_processor(raw_tar_input_path, list_of_raw_in_tar_path)

    print("--- %s seconds ---" % (time.time() - start_time))
