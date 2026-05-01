from paddleocr import PaddleOCR
import numpy as np
import cv2

# Create an image with text "ABC 123"
img = np.ones((100, 300, 3), dtype=np.uint8) * 255
cv2.putText(img, "ABC 123", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

try:
    ocr = PaddleOCR(use_textline_orientation=True, lang='en', device='cpu')
    print("Initialization successful")
    result = ocr.ocr(img)
    print("OCR result type:", type(result))
    print("OCR result:", result)
    
    if result and result[0]:
        for line in result[0]:
            print("Line:", line)
            print("Text:", line[1][0])
            print("Conf:", line[1][1])
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
