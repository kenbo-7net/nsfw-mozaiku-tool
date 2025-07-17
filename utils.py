import cv2

def mosaic_area(img, x1, y1, x2, y2, size):
    w = x2 - x1
    h = y2 - y1
    roi = img[y1:y2, x1:x2]
    roi = cv2.resize(roi, (size, size), interpolation=cv2.INTER_LINEAR)
    roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_NEAREST)
    img[y1:y2, x1:x2] = roi
    return img
