from paddleocr import PaddleOCR
import numpy as np
import cv2
import traceback

# Create an image with text "ABC 123"
img = np.ones((100, 300, 3), dtype=np.uint8) * 255
cv2.putText(img, "ABC 123", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

try:
    ocr = PaddleOCR(use_textline_orientation=True, lang='en', device='cpu', enable_mkldnn=False)
    print("Initialization successful")
    
    result = ocr.ocr(img)
    if result and result[0]:
        res = result[0]
        print("Type of res:", type(res))
        print("Attributes of res:", dir(res))
        
        # Check standard attributes
        if hasattr(res, 'dt_polys'):
            print("dt_polys:", res.dt_polys)
        if hasattr(res, 'rec_texts'):
            print("rec_texts:", res.rec_texts)
        if hasattr(res, 'rec_scores'):
            print("rec_scores:", res.rec_scores)
            
        # Check if it can be converted to the old format
        # Some versions have a .to_list() or similar
        # Based on typical PaddleX results:
        # result[0] is an OCRResult object
        # It contains multiple detections.
        
        # In PaddleX OCR pipeline:
        # result[0].dt_polys: list of [x1, y1, x2, y2, ...]
        # result[0].rec_texts: list of texts
        # result[0].rec_scores: list of scores
        
        for i in range(len(res.rec_texts)):
            print(f"Match {i}: {res.rec_texts[i]} (Score: {res.rec_scores[i]})")

except Exception as e:
    print("Error:", e)
    traceback.print_exc()
