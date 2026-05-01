from paddleocr import PaddleOCR
import numpy as np
import cv2

img = np.ones((100, 300, 3), dtype=np.uint8) * 255
cv2.putText(img, "ABC 123", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

ocr = PaddleOCR(use_textline_orientation=True, lang='en', device='cpu', enable_mkldnn=False)
result = ocr.ocr(img)
print("Result:")
print(result)
if result and len(result) > 0:
    res0 = result[0]
    print(type(res0))
    if type(res0) == list:
        print("it is a list", res0)
    else:
        print("dir:", dir(res0))
        for attr in dir(res0):
             if not attr.startswith('__'):
                  print(f"{attr}: {getattr(res0, attr)}")
