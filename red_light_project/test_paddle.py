from paddleocr import PaddleOCR
import numpy as np

# Create a dummy image
img = np.zeros((100, 300, 3), dtype=np.uint8)

try:
    ocr = PaddleOCR(use_textline_orientation=True, lang='en', device='cpu')
    print("Initialization successful")
    result = ocr.ocr(img)
    print("OCR result type:", type(result))
    print("OCR result:", result)
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
