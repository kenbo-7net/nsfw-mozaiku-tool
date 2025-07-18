import cv2

def load_image(image_path):
    return cv2.imread(image_path)

def apply_mosaic(image, x1, y1, x2, y2, size=30):
    roi = image[y1:y2, x1:x2]
    if roi.size == 0:
        return image
    roi = cv2.resize(roi, (size, size), interpolation=cv2.INTER_LINEAR)
    roi = cv2.resize(roi, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
    image[y1:y2, x1:x2] = roi
    return image
