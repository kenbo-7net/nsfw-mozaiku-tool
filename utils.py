import cv2

def apply_mosaic(image, bboxes, ratio=0.02):
    result = image.copy()
    for (x, y, w, h) in bboxes:
        mosaic = cv2.resize(result[y:y+h, x:x+w], None, fx=ratio, fy=ratio, interpolation=cv2.INTER_LINEAR)
        mosaic = cv2.resize(mosaic, (w, h), interpolation=cv2.INTER_NEAREST)
        result[y:y+h, x:x+w] = mosaic
    return result
