from paddleocr import PaddleOCR
import numpy as np
import cv2

img = np.ones((100, 300, 3), dtype=np.uint8) * 255
cv2.putText(img, "ABC 123", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

try:
    ocr = PaddleOCR(use_textline_orientation=True, lang='en', device='cpu', enable_mkldnn=False)
    result = ocr.ocr(img)
    print("Result structure:")
    print(result)
    print("Type of result:", type(result))
    if result and len(result) > 0:
        print("Type of result[0]:", type(result[0]))
        if isinstance(result[0], list):
             for line in result[0]:
                 print("line length:", len(line))
                 print("line[0]:", line[0])
                 print("line[1]:", line[1])
except Exception as e:
    print(e)
