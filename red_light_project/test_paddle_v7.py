from paddleocr import PaddleOCR
import numpy as np
import cv2

img = np.ones((100, 300, 3), dtype=np.uint8) * 255
cv2.putText(img, "ABC 123", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

try:
    ocr = PaddleOCR(use_textline_orientation=True, lang='en', device='cpu', enable_mkldnn=False)
    result = ocr.ocr(img)
    if result and result[0]:
        res = result[0]
        print("Type:", type(res))
        print("DIR:", dir(res))
        # Print actual values for likely candidates
        for attr in ['dt_polys', 'rec_text', 'rec_score', 'dt_boxes', 'ocr_text', 'ocr_score', 'texts', 'scores', 'ocr_results']:
             if hasattr(res, attr):
                 print(f"{attr}: {getattr(res, attr)}")
        
        # Check standard properties
        print("Dict keys:", res.keys() if hasattr(res, 'keys') else "No keys()")
        print("Result content:", res)

except Exception as e:
    print("Error:", e)
