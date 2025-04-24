import cv2
import numpy as np
from pyzbar.pyzbar import decode


def analyze_barcode_from_pil(pil_image):
    # Convert PIL image to OpenCV format
    cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    barcodes = decode(cv_image)
    results = []

    for barcode in barcodes:
        data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        results.append({'type': barcode_type, 'data': data})

        # Draw rectangle (optional for debugging)
        pts = [(point.x, point.y) for point in barcode.polygon]
        cv2.polylines(cv_image, [np.array(pts, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.putText(cv_image, f'{barcode_type}: {data}', (pts[0][0], pts[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    return results, cv_image  # Return both barcode data and annotated image
