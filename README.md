# 🏭 Industrial Color-Sorting & Safety Vision Pipeline

Hey there! 👋 Welcome to my GitHub repo. 

I put this project together to solve a classic factory automation puzzle: **how do you sort objects quickly on a conveyor belt while making sure you don't accidentally endanger human operators?** 

Instead of leaning on heavy, resource-hungry AI models that lag out, I built a lightweight, lightning-fast computer vision pipeline using **Python** and **OpenCV**. It handles precise color-and-shape sorting on one end, and acts as a digital safety guard on the other.

---

## 🧠 Why I Built This
Let’s be honest—manual sorting is slow and repetitive. But in real industrial settings, safety is the absolute priority. I wanted a system that could do two things seamlessly:
1. **Smart Sorting:** Identify objects moving through a workspace using color spaces and geometric shape analysis.
2. **Safety Override:** Instantly trigger a full-screen red-border alert if a human enters a restricted machinery zone.

---

## 🛠 What's Under the Hood?
* **Language:** Python 3.x
* **Vision Processing:** OpenCV (`cv2`)
* **Math & Matrices:** NumPy
* **Environment:** Developed and tested on Windows 11 / VS Code

---

## 🕹 Interactive Controls (Try them out!)
When you fire up `main.py`, you can control the live feed directly from your keyboard:

| Key | What it does |
| :--- | :--- |
| **`[M]`** | Toggle Binary Mask view (see what the camera’s thresholding actually isolates) |
| **`[V]`** | Vector Skeleton mode (draws the geometric outlines and vertices) |
| **`[C]`** | Photonic Calibration mode (samples ambient HSV values so you can fix lighting issues on the fly) |
| **`[H]`** | Human Safety Override (toggles the safety alarm ON/OFF) |
| **`[S]`** | Snapshot Shutter (snaps a clean evidence capture with all HUD graphics intact) |
| **`[F]`** | Freeze Stream (pauses the video feed so you can inspect a frame closely) |
| **`[1-7]`** | Switch between different color profiles (Red, Green, Blue, etc.) |

---

## ✨ Cool Technical Details
* **Smart Shape Filtering:** Instead of just relying on raw vertex counts (which loves to flicker), I used circularity ratio calculations to reliably tell circles, squares, and polygons apart.
* **Noise Reduction:** Webcams can be notoriously jittery. I added a Gaussian blur pass combined with elliptical morphological closing to keep the bounding boxes rock-solid.
* **Bio-Kinematic Safety:** The system watches out for massive, organic shapes to flag human presence, switching into an emergency alert mode instantly.

---

## 🎯 Who is this for?
* **Plant Managers & Safety Folks:** Looking to scale up throughput while cutting down workplace liabilities.
* **Automation Engineers:** Interested in low-latency vision systems that don't need a heavy GPU.
* **Students & Devs:** Tinkering with OpenCV, color masking, and contour detection.

---

## 📝 Final Note
This was built as part of my coursework. If you're testing it out locally, make sure your room has decent lighting and your webcam lens is clean. If the colors aren't picking up right away, just tap **`[C]`** to calibrate to your environment!

*Found a bug or want to suggest an improvement? Feel free to open an issue or drop a pull request. Enjoy!*
