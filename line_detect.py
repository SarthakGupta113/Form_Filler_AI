import cv2
import numpy as np
import matplotlib.pyplot as plt
def lineDetect(image_path: str):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    detect_horizontal = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    detect_vertical = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
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
            isolated_horizontal_lines[f"Line {line_index}"] = { "x": x, "y": y, "w": w, "h": h}
            line_index += 1
    # final_image = cv2.bitwise_not(detect_horizontal)
    # # plt.imshow(final_image, cmap='gray')
    # # plt.axis('off')
    # # plt.show()
    return isolated_horizontal_lines