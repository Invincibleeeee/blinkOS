import cv2
import mediapipe as mp
import pyautogui
import collections
import sys
import time

# ========================
# Configurable parameters
# ========================
BASE_SCROLL_THRESHOLD = 12   # smaller = more sensitive
BASE_HSCROLL_THRESHOLD = 12
SMOOTHING_FRAMES = 5    # moving average frames for nose position
ACTION_COOLDOWN = 0.05  # seconds between actions (for both vertical and horizontal)

# ========================
# Mediapipe init
# ========================
mp_face = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils
face_mesh = mp_face.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# ========================
# Video capture init
# ========================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Could not open webcam. Make sure it is connected and not used by another program.")
    sys.exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ========================
# Calibration and smoothing
# ========================
neutral_x, neutral_y = 0, 0
calibrated = False

nose_x_history = collections.deque(maxlen=SMOOTHING_FRAMES)
nose_y_history = collections.deque(maxlen=SMOOTHING_FRAMES)

last_action_time = {'vertical': 0, 'horizontal': 0}

# ========================
# Helper functions
# ========================
def get_nose_pos(landmarks, w, h):
    """Returns nose tip position (landmark 1)"""
    nose = landmarks[1]
    return int(nose.x * w), int(nose.y * h)

def nothing(x):
    pass

def horizontal_scroll(amount):
    """Cross-platform horizontal scroll"""
    if sys.platform == 'win32':
        pyautogui.keyDown('shift')
        pyautogui.scroll(-amount)
        pyautogui.keyUp('shift')
    else:
        pyautogui.hscroll(amount)

# Create window and trackbars for sensitivity (threshold adjustment)
cv2.namedWindow("Head Control UX")
cv2.createTrackbar("VScroll Thresh", "Head Control UX", BASE_SCROLL_THRESHOLD, 50, nothing)
cv2.createTrackbar("HScroll Thresh", "Head Control UX", BASE_HSCROLL_THRESHOLD, 50, nothing)

print("INFO: Press 'c' to calibrate your neutral head position. ESC to quit.")
print("INFO: Use trackbars to adjust thresholds (lower = more sensitive).")


# ========================
# Cleanup
# ========================
cap.release()
cv2.destroyAllWindows()



# import cv2
# import mediapipe as mp
# import pyautogui
# cam = cv2.VideoCapture(0)
# face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
# screen_w, screen_h = pyautogui.size()
# while True:
#     _, frame = cam.read()
#     frame = cv2.flip(frame, 1)
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     output = face_mesh.process(rgb_frame)
#     landmark_points = output.multi_face_landmarks
#     frame_h, frame_w, _ = frame.shape
#     if landmark_points:
#         landmarks = landmark_points[0].landmark
#         for id, landmark in enumerate(landmarks[474:478]):
#             x = int(landmark.x * frame_w)
#             y = int(landmark.y * frame_h)
#             cv2.circle(frame, (x, y), 3, (0, 255, 0))
#             if id == 1:
#                 screen_x = screen_w * landmark.x
#                 screen_y = screen_h * landmark.y
#                 pyautogui.moveTo(screen_x, screen_y)
#         left = [landmarks[145], landmarks[159]]
#         for landmark in left:
#             x = int(landmark.x * frame_w)
#             y = int(landmark.y * frame_h)
#             cv2.circle(frame, (x, y), 3, (0, 255, 255))
#         if (left[0].y - left[1].y) < 0.004:
#             pyautogui.click()
#             pyautogui.sleep(1)
#     cv2.imshow('Eye Controlled Mouse', frame)
#     cv2.waitKey(1)