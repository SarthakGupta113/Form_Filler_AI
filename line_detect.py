import cv2
import numpy as np
import matplotlib.pyplot as plt
def skeletonize(image):
    size = np.size(image)
    skel = np.zeros(image.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    while True:
        eroded = cv2.erode(image, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(image, temp)
        skel = cv2.bitwise_or(skel, temp)
        image = eroded.copy()
        if cv2.countNonZero(image) == 0:
            break
    return skel
def preprocess_image(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(image)
    adaptive_thresh = cv2.adaptiveThreshold(
        enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 10)
    return adaptive_thresh
def lineDetect(image_path: str):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    binary_image = preprocess_image(image)
    skeleton = skeletonize(binary_image)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    detect_horizontal = cv2.morphologyEx(skeleton, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    detect_vertical = cv2.morphologyEx(skeleton, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    contours_horizontal, _ = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_vertical, _ = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    vertical_boxes = [cv2.boundingRect(contour) for contour in contours_vertical]
    intersecting_y_coordinates = set()
    for contour in contours_horizontal:
        x, y, w, h = cv2.boundingRect(contour)
        if h < 5:  
            for vx, vy, vw, vh in vertical_boxes:
                if (vx < x + w and vx + vw > x) and (vy <= y <= vy + vh):
                    intersecting_y_coordinates.add(y)
                    break
    isolated_horizontal_lines = {}
    line_index = 1
    for contour in contours_horizontal:
        x, y, w, h = cv2.boundingRect(contour)
        if h < 5 and y not in intersecting_y_coordinates:
            isolated_horizontal_lines[f"Line {line_index}"] = {"x": x, "y": y, "w": w, "h": h}
            line_index += 1
    # output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # for line_data in isolated_horizontal_lines.values():
    #     x, y, w, h = line_data["x"], line_data["y"], line_data["w"], line_data["h"]
    #     cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # plt.imshow(output_image)
    # plt.axis('off')
    # plt.show()
    return isolated_horizontal_lines