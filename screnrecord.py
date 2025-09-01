#!/usr/bin/env python3
# pip install opencv-python pyautogui

import cv2
import numpy as np
import pyautogui

# macOS: System Settings > Privacy & Security > Screen Recording → allow your terminal/IDE

def main():
    # Screen size (width, height)
    sw, sh = pyautogui.size()
    SCREEN_SIZE = (sw, sh)

    # Video writer (choose a codec your OS supports)
    # On Windows/Linux, 'XVID' + .avi is fine. On macOS, prefer 'mp4v' + .mp4
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # change to 'XVID' if you want .avi
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, SCREEN_SIZE)

    webcam = cv2.VideoCapture(0)
    if not webcam.isOpened():
        print("Could not open webcam 0")
        return

    # Optional: set webcam capture size (not guaranteed)
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Recording screen with webcam picture-in-picture. Press 'q' to quit.")
    while True:
        # Screenshot (RGB PIL -> numpy RGB)
        img_rgb = np.array(pyautogui.screenshot())

        # Convert to BGR for OpenCV
        img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

        # Read webcam
        ret, frame = webcam.read()
        if not ret or frame is None:
            print("Webcam frame grab failed.")
            break

        # Resize webcam feed to a small overlay (e.g., 320x240)
        overlay_w, overlay_h = 320, 240
        cam_small = cv2.resize(frame, (overlay_w, overlay_h))

        # Paste top-left corner; ensure it fits
        img[0:overlay_h, 0:overlay_w] = cam_small

        # Show live preview
        cv2.imshow('frame', img)

        # Write to video file (must be BGR and match SCREEN_SIZE)
        out.write(img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("quit")
            break

    # Cleanup (after loop)
    webcam.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()




