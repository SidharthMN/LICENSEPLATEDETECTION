from paddleocr import PaddleOCR
import numpy as np
import cv2
import traceback

# Create an image with text "ABC 123"
img = np.ones((100, 300, 3), dtype=np.uint8) * 255
cv2.putText(img, "ABC 123", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

try:
    print("Initializing PaddleOCR...")
    # Explicitly set versions and disable mkldnn
    ocr = PaddleOCR(use_textline_orientation=True, lang='en', device='cpu', enable_mkldnn=False, ocr_version='PP-OCRv4')
    print("Initialization successful")
    
    print("Running OCR...")
    result = ocr.ocr(img, cls=True)
    print("OCR result type:", type(result))
    print("OCR result:", result)
    
    if result is None:
        print("Result is None")
    elif len(result) == 0:
        print("Result is empty list")
    else:
        for i, res in enumerate(result):
            print(f"Result[{i}]:", res)
            if res is not None:
                for line in res:
                    print("  Line:", line)
                    text = line[1][0]
                    conf = line[1][1]
                    print(f"  Text: {text}, Conf: {conf}")
except Exception as e:
    print("Caught Exception:", e)
    traceback.print_exc()
