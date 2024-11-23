import cv2
import numpy as np
import matplotlib.pyplot as plt

def detectRectangles(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangles = []
    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:
            x, y, width, height = cv2.boundingRect(approx)
            if(width>5 and height>5):
                rectangles.append({
                    "top_left": [x, y],
                    "width": width,
                    "height": height
                })
    return rectangles