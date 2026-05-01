from paddleocr import PaddleOCR
import numpy as np
import cv2

img = np.ones((100, 300, 3), dtype=np.uint8) * 255
cv2.putText(img, "ABC 123", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

ocr = PaddleOCR(use_textline_orientation=True, lang='en', device='cpu', enable_mkldnn=False)
result = ocr.ocr(img)

if result and result[0]:
    res = result[0]
    print("Is it a dict?", isinstance(res, dict))
    print("Does it have keys?", hasattr(res, 'keys'))
    if 'rec_texts' in res:
        print("rec_texts found!")
        for idx, text in enumerate(res['rec_texts']):
            score = res['rec_scores'][idx]
            print(f"Text: {text}, Score: {score}")
    else:
        print("rec_texts NOT found in keys:", res.keys())
