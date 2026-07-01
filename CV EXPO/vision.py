import cv2
import numpy as np

def detect_colored_objects(frame, profile, min_area=800, human_mode=False):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, profile['lower1'], profile['upper1'])
    
    if profile.get('lower2') is not None:
        mask2 = cv2.inRange(hsv, profile['lower2'], profile['upper2'])
        mask = cv2.bitwise_or(mask, mask2)
        
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    rects, shapes, purities, approxs = [], [], [], []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        if area > min_area:
            # --- MASSIVE OBJECT FILTER ---
            if area > 15000: 
                if human_mode:
                    x, y, w, h = cv2.boundingRect(cnt)
                    roi_mask = mask[y:y+h, x:x+w]
                    purity = int((cv2.countNonZero(roi_mask) / (w * h)) * 100)
                    
                    rects.append((x, y, w, h))
                    shapes.append("HUMAN DETECTED")
                    purities.append(purity)
                    approxs.append(cv2.approxPolyDP(cnt, 0.035 * cv2.arcLength(cnt, True), True))
                else:
                    continue # Ignores massive objects when H is OFF
                    
            # --- NORMAL INDUSTRIAL OBJECTS ---
            else:
                x, y, w, h = cv2.boundingRect(cnt)
                roi_mask = mask[y:y+h, x:x+w]
                purity = int((cv2.countNonZero(roi_mask) / (w * h)) * 100)
                
                if purity >= 60:
                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.035 * peri, True)
                    vertices = len(approx)
                    
                    # Mathematical Shape Classification
                    if vertices == 3: shape = "TRIANGLE"
                    elif vertices == 4:
                        ar = float(w) / float(h)
                        shape = "SQUARE" if 0.88 <= ar <= 1.12 else "RECTANGLE"
                    elif vertices >= 6:
                        _, radius = cv2.minEnclosingCircle(cnt)
                        circle_area = np.pi * (radius ** 2)
                        shape = "CIRCLE" if (area / circle_area) >= 0.78 else "POLYGON"
                    else:
                        shape = "POLYGON"

                    # --- THE FIX: STRICT GEOMETRIC FILTER ---
                    # If safety is OFF, completely ignore irregular/organic "Polygon" shapes (like fingers)
                    if not human_mode and shape == "POLYGON":
                        continue 
                        
                    # If it passes the geometry test, send it to the UI
                    rects.append((x, y, w, h))
                    shapes.append(shape)
                    purities.append(purity)
                    approxs.append(approx)
            
    return rects, shapes, purities, approxs, mask, hsv