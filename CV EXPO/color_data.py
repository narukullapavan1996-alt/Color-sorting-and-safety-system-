import numpy as np

COLOR_PROFILES = {
    '1': {'name': 'RED', 'lower1': np.array([0, 150, 100]), 'upper1': np.array([10, 255, 255]), 'lower2': np.array([170, 150, 100]), 'upper2': np.array([180, 255, 255]), 'bgr': (0, 0, 255)},
    '2': {'name': 'GREEN', 'lower1': np.array([40, 100, 100]), 'upper1': np.array([80, 255, 255]), 'bgr': (0, 255, 0)},
    '3': {'name': 'BLUE', 'lower1': np.array([100, 150, 100]), 'upper1': np.array([130, 255, 255]), 'bgr': (255, 0, 0)},
    '4': {'name': 'YELLOW', 'lower1': np.array([20, 150, 150]), 'upper1': np.array([30, 255, 255]), 'bgr': (0, 255, 255)},
    '5': {'name': 'CYAN', 'lower1': np.array([85, 150, 150]), 'upper1': np.array([95, 255, 255]), 'bgr': (255, 255, 0)},
    '6': {'name': 'MAGENTA', 'lower1': np.array([140, 150, 150]), 'upper1': np.array([160, 255, 255]), 'bgr': (255, 0, 255)},
    '7': {'name': 'ORANGE', 'lower1': np.array([10, 150, 150]), 'upper1': np.array([20, 255, 255]), 'bgr': (0, 165, 255)}
}