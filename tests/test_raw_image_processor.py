import os
import unittest
from raw_image_processor.convert_images import raw_image_processor


class TestRawImageProcessor(unittest.TestCase):
    def test_raw_image_processor(self):
        base_name = os.path.dirname(__file__)
        input_path = os.path.join(base_name, 'data/test_example_frames.tar')
        expected_output_path = os.path.join(base_name, 'data/test_example_frames_png.tar')
        expected_frame_statistics = [
            {
                "frame": "Frame_0071_ts_34710.000000.png",
                "average_pixel_value": 125.56559136284723,
                "std_of_pixel_in_frame": 63.45898373103604
            },
            {
                "frame": "Frame_0070_ts_34700.000000.png",
                "average_pixel_value": 125.59364474826388,
                "std_of_pixel_in_frame": 63.46799084371201
            },
            {
                "frame": "Frame_0072_ts_34720.000000.png",
                "average_pixel_value": 125.46891927083334,
                "std_of_pixel_in_frame": 63.446946355756324
            }
        ]
        output_path, frame_statistics = raw_image_processor(input_path=input_path)
        assert output_path == expected_output_path

        # Remove the output file if it exists
        if os.path.exists(expected_output_path):
            os.remove(expected_output_path)

        # Assertion for file not existing after removal
        assert not os.path.exists(expected_output_path)

        assert len(frame_statistics) == len(expected_frame_statistics)
