import sys
import os
import cv2
import time
import numpy as np

# Universal Machine Portability
script_location = os.path.abspath(__file__)
universal_project_root = os.path.dirname(script_location)

if universal_project_root not in sys.path:
    sys.path.insert(0, universal_project_root)

from color_data import COLOR_PROFILES
from vision import detect_colored_objects

def main():
    print("=========================================================")
    print("   CV EXPO: THE 5-HOTKEY VIVA DEFENSE SUITE              ")
    print("=========================================================")
    
    cap = cv2.VideoCapture(0)
    time.sleep(2.0) 
    
    if not cap.isOpened():
        print("[!] ERROR: Camera Port 0 Locked. Try VideoCapture(1).")
        return

    current_key = '1'
    viewport_mode = "STANDARD" 
    is_frozen = False
    human_mode = False # HUMAN SAFETY TOGGLE
    last_valid_frame = None
    prev_frame_time = 0
    
    print(f"[+] ONLINE. Active Matrix: {COLOR_PROFILES[current_key]['name']}")
    print("[!] SHORTCUTS ACTIVE ON YOUR KEYBOARD:")
    print("    [M] -> Pure Black Mask View | [V] -> Vector Skeleton Mode")
    print("    [C] -> Photonic Calibrate   | [H] -> HUMAN SAFETY TOGGLE")
    print("    [S] -> Snapshot Shutter     | [F] -> FREEZE VIDEO STREAM")
    print("    [1-5] Switch Color          | [Q] Exit\n")

    while True:
        if not is_frozen:
            ret, live_frame = cap.read()
            if not ret or live_frame is None: continue
            frame = cv2.flip(live_frame, 1)
            last_valid_frame = frame.copy()
        else:
            if last_valid_frame is not None:
                frame = last_valid_frame.copy()
            else:
                continue

        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time) if (new_frame_time - prev_frame_time) > 0 else 0
        prev_frame_time = new_frame_time
        
        # --- KEYBOARD LISTENER (Removed the broken [S] trigger from here!) ---
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'): break
        elif key == ord('f'):
            is_frozen = not is_frozen
        elif key == ord('m'): viewport_mode = "STANDARD" if viewport_mode == "MASK" else "MASK"
        elif key == ord('v'): viewport_mode = "STANDARD" if viewport_mode == "VECTOR" else "VECTOR"
        elif key == ord('c'): viewport_mode = "STANDARD" if viewport_mode == "CALIBRATE" else "CALIBRATE"
        elif key == ord('h'): 
            human_mode = not human_mode
            print(f"[*] Human Safety Override: {'ON' if human_mode else 'OFF'}")
        elif chr(key) in COLOR_PROFILES:
            current_key = chr(key)

        profile = COLOR_PROFILES[current_key]
        ui_color = profile['bgr']
        
        # Safely calls vision pipeline
        rects, shapes, purities, approxs, mask, hsv = detect_colored_objects(frame, profile, min_area=800, human_mode=human_mode)
        
        # --- TOP HUD ---
        cv2.rectangle(frame, (0, 0), (640, 45), (0, 0, 0), -1)
        frz_tag = " [FROZEN]" if is_frozen else ""
        hum_tag = " | HUMAN ALARM: ON" if human_mode else ""
        cv2.putText(frame, f"MODE:{viewport_mode}{frz_tag}{hum_tag} | FPS:{int(fps)} | TARGETS:{len(rects)}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, ui_color, 2)

        # --- THE 4 DISPLAY RENDERERS ---
        if viewport_mode == "MASK" and mask is not None:
            output = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            cv2.putText(output, "BINARY SEGMENTATION", (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,255,255), 2)
            
        elif viewport_mode == "VECTOR" and len(approxs) > 0:
            output = np.zeros_like(frame)
            for i, poly in enumerate(approxs):
                cv2.drawContours(output, [poly], -1, (0, 255, 0), 2) 
                for pt in poly:
                    cv2.circle(output, tuple(pt[0]), 6, (0, 0, 255), -1) 
                cv2.putText(output, f"VERTICES: {len(poly)}", (rects[i][0], rects[i][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

        elif viewport_mode == "CALIBRATE" and hsv is not None:
            output = frame.copy()
            for i, (x, y, w, h) in enumerate(rects):
                roi = hsv[y:y+h, x:x+w]
                mH, mS, mV, _ = cv2.mean(roi)
                cv2.rectangle(output, (x, y), (x+w, y+h), ui_color, 2)
                cv2.rectangle(output, (x, y+h), (x+w, y+h+40), (0,0,0), -1)
                cv2.putText(output, f"H:{int(mH)} S:{int(mS)} V:{int(mV)}", (x+5, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,255,255), 1)

        else: # STANDARD MODE
            output = frame.copy()
            human_in_frame = False 
            
            # Draw Loop
            for i, (x, y, w, h) in enumerate(rects):
                roi = hsv[y:y+h, x:x+w]
                mH, mS, mV, _ = cv2.mean(roi)
                hsv_text = f"H:{int(mH)} S:{int(mS)} V:{int(mV)}"

                if shapes[i] == "HUMAN DETECTED":
                    human_in_frame = True 
                else:
                    cv2.rectangle(output, (x, y), (x+w, y+h), ui_color, 3)
                    cv2.putText(output, f"[{shapes[i]}] ({purities[i]}%)", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, ui_color, 2)
                    cv2.putText(output, hsv_text, (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

            # THE MASSIVE HUMAN WARNING ALARM
            if human_in_frame:
                cv2.rectangle(output, (0, 0), (output.shape[1], output.shape[0]), (0, 0, 255), 15)
                cv2.putText(output, "!!! WARNING: HUMAN PRESENT !!!", (20, output.shape[0]//2), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 4)

        # --- THE ONLY SNAPSHOT TRIGGER (Safely captures 'output' with all graphics) ---
        if key == ord('s'):
            receipt = f"SCREEN_CAPTURE_{int(time.time())}.jpg"
            cv2.imwrite(receipt, output) 
            print(f"[📸 SHUTTER] Evidence preserved with graphics: {receipt}")

        cv2.imshow("CV EXPO - Master Faculty Build", output)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()