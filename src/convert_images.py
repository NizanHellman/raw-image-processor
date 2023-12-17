import os.path
import tarfile
import tempfile
import time
from dataclasses import dataclass
from multiprocessing.dummy import Pool
from pathlib import Path
from typing import Tuple, Any

from PIL import Image
import numpy


@dataclass
class RawFile:
    tar_file: tarfile.ExFileObject
    entry_name: str
    temp_dir: str
    img_size: tuple[int, int]


def get_image_statistics(image: bytes) -> Tuple[float, float]:
    numpy_image = numpy.frombuffer(image, dtype=numpy.uint8)
    average_pixel_value = numpy_image.mean()
    std_of_pixel_value = numpy_image.std()
    return average_pixel_value, std_of_pixel_value


def make_tarfile(output_filename: str, source_dir: str) -> None:
    with tarfile.open(output_filename, 'w') as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def process_raw_file(raw_data_file: RawFile) -> dict:
    raw_file_name = Path(raw_data_file.entry_name).stem
    png_file_name = f'{raw_file_name}.png'

    with raw_data_file.tar_file as file:
        raw_data = file.read()

    img_size = raw_data_file.img_size
    img = Image.frombytes('L', img_size, raw_data)
    img.save(os.path.join(raw_data_file.temp_dir, png_file_name))

    avg, std = get_image_statistics(raw_data)

    frame_obj = {
        'frame': png_file_name,
        'average_pixel_value': avg,
        'std_of_pixel_in_frame': std
    }

    return frame_obj


def convert_to_png_and_get_statistics(raw_files: list[RawFile], threads: int) -> list:
    with Pool(threads) as pool:
        image_statistics = pool.map(process_raw_file, raw_files)

    return image_statistics


def extract_tar_files_and_add_meta_data(tar_file_path: str, temp_dir: str, img_size: Tuple[int, int]) -> Tuple[tarfile.TarFile, list[RawFile]]:
    raw_files = []
    tar_file = tarfile.open(tar_file_path, 'r')
    for entry in tar_file:
        raw_file = RawFile(tar_file=tar_file.extractfile(entry),
                           entry_name=entry.name,
                           temp_dir=temp_dir,
                           img_size=img_size)
        raw_files.append(raw_file)
    return tar_file, raw_files


def extract_output_file_path_from_input_path(input_path: str) -> str:
    input_file_path, input_file_name_ext = os.path.split(input_path)
    input_file_name_no_ext, input_file_ext = os.path.splitext(input_file_name_ext)
    output_path = os.path.join(input_file_path, f"{input_file_name_no_ext}_png.tar")
    return output_path


def raw_image_processor(input_path: str, output_path: str = None, img_size: Tuple[int, int] = (1280, 720), threads: int = 10) -> Tuple[str, list]:
    output_path = output_path or extract_output_file_path_from_input_path(input_path)
    with tempfile.TemporaryDirectory() as temp_dir:
        tar_file, raw_files = extract_tar_files_and_add_meta_data(input_path, temp_dir, img_size)
        image_statistics = convert_to_png_and_get_statistics(raw_files, threads)
        tar_file.close()
        make_tarfile(output_path, temp_dir)
    return output_path, image_statistics


if __name__ == '__main__':
    start_time = time.time()
    project_path = os.path.join(os.path.dirname(__file__), '../')
    try:
        os.remove(os.path.join(project_path, 'data/example_frames_png.tar'))
    except:
        pass
    raw_tar_input_path_relative = 'data/example_frames.tar'
    raw_tar_input_path = os.path.join(project_path, raw_tar_input_path_relative)
    print(raw_image_processor(raw_tar_input_path))

    print("--- %s seconds ---" % (time.time() - start_time))
