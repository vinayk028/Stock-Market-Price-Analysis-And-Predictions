import unittest
import os
from main import get_marked_levels

class TestMarkedLevelsExtraction(unittest.TestCase):
    def test_successful_extraction(self):
        image_path = 'AssignmentImage-2.png'
        result = get_marked_levels(image_path)

        self.assertTrue('marked_levels' in result)
        self.assertTrue(len(result['marked_levels']) > 0)

    def test_missing_image(self):
        image_path = 'nonexistent_image.png'
        result = get_marked_levels(image_path)

        self.assertTrue('error' in result)
        self.assertIn("Error reading image", result['error'])

    def test_image_processing_error(self):
        # Create a temporary corrupted image
        corrupt_image_path = 'corrupt_image.png'
        with open(corrupt_image_path, 'wb') as f:
            f.write(b'Invalid image data')

        result = get_marked_levels(corrupt_image_path)

        self.assertTrue('error' in result)
        if "Error processing image" not in result['error']:
            self.assertIn("Error reading image", result['error'])

        # Clean up the temporary file
        os.remove(corrupt_image_path)

if __name__ == '__main__':
    unittest.main()
