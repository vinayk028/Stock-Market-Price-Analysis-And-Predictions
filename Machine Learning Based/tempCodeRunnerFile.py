import cv2
import numpy as np
import PIL.Image


def read_image(image_path):
    """
    Read an image from a file.

    Args:
        image_path (str): The path to the image file.

    Returns:
        PIL.Image.Image: A Pillow Image object.
    """
    try:
        image = PIL.Image.open(image_path)
        return image
    except Exception as e:
        raise Exception(f"Error reading image: {str(e)}")


def process_image(image):
    """
    Perform image processing on the input image.

    Args:
        image (PIL.Image.Image): A Pillow Image object.

    Returns:
        np.ndarray: A NumPy array representing the processed image.
    """
    try:
        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_image, 100, 200)
        kernel = np.ones((3, 3), np.uint8)
        dilated_edges = cv2.dilate(edges, kernel, iterations=1)
        eroded_edges = cv2.erode(dilated_edges, kernel, iterations=1)
        return eroded_edges
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")


def extract_marked_levels(image):
    """
    Extract the marked levels from the input image.

    Args:
        image (np.ndarray): A NumPy array representing the processed image.

    Returns:
        list: A list of marked levels.
    """
    try:
        rois = [contour for contour in cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] if cv2.contourArea(contour) >= 10]
        marked_levels = [cv2.moments(
            roi)['m10'] / cv2.moments(roi)['m00'] for roi in rois]
        return marked_levels
    except Exception as e:
        raise Exception(f"Error extracting marked levels: {str(e)}")


def get_marked_levels(image_path):
    """
    Extract marked levels from a stock chart image.

    Args:
        image_path (str): The path to the image file.

    Returns:
        dict: A dictionary of marked levels or an error message if an issue occurs.
    """
    try:
        image = read_image(image_path)
        processed_image = process_image(image)
        marked_levels = extract_marked_levels(processed_image)
        return {'marked_levels': marked_levels}
    except Exception as e:
        return {'error': str(e)}


if __name__ == "__main__":
    # Example usage:
    image_path = 'AssignmentImage-2.png'
    marked_levels = get_marked_levels(image_path)

    if 'error' in marked_levels:
        print(f"Error: {marked_levels['error']}")
    else:
        print(f"Marked Levels: {marked_levels['marked_levels']}")
