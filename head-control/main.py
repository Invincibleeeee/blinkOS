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
# Main loop
# ========================
while True:
    ret, frame = cap.read()
    if not ret:
        print("WARNING: Failed to read frame from webcam. Retrying...")
        continue  # skip this iteration

    frame = cv2.flip(frame, 1)  # mirror
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    try:
        results = face_mesh.process(rgb)
    except Exception as e:
        print(f"WARNING: Mediapipe error: {e}")
        continue  # skip this frame

    # Get current thresholds from trackbars (sensitivity options)
    SCROLL_THRESHOLD = cv2.getTrackbarPos("VScroll Thresh", "Head Control UX")
    HSCROLL_THRESHOLD = cv2.getTrackbarPos("HScroll Thresh", "Head Control UX")

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]

        # Draw face mesh
        mp_draw.draw_landmarks(
            frame, face_landmarks, mp_face.FACEMESH_TESSELATION,
            mp_draw.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1),
            mp_draw.DrawingSpec(color=(0,0,255), thickness=1)
        )

        # Get nose tip
        nose_x, nose_y = get_nose_pos(face_landmarks.landmark, w, h)

        # Apply smoothing
        nose_x_history.append(nose_x)
        nose_y_history.append(nose_y)
        smooth_x = int(sum(nose_x_history)/len(nose_x_history))
        smooth_y = int(sum(nose_y_history)/len(nose_y_history))

        # Draw nose tip
        cv2.circle(frame, (smooth_x, smooth_y), 6, (255,0,0), -1)

        if calibrated:
            dx = smooth_x - neutral_x
            dy = smooth_y - neutral_y

            current_time = time.time()

            # Vertical scroll up/down with cooldown and proportional amount
            if abs(dy) > SCROLL_THRESHOLD and current_time - last_action_time['vertical'] > ACTION_COOLDOWN:
                # Proportional scroll for smoother control
                scroll_factor = abs(dy) / SCROLL_THRESHOLD
                scroll_amount = int(50 * scroll_factor)  # Base amount scaled by how far head is moved
                if dy < -SCROLL_THRESHOLD:
                    pyautogui.scroll(scroll_amount)
                elif dy > SCROLL_THRESHOLD:
                    pyautogui.scroll(-scroll_amount)
                last_action_time['vertical'] = current_time

            # Horizontal scroll left/right with cooldown and proportional amount
            if abs(dx) > HSCROLL_THRESHOLD and current_time - last_action_time['horizontal'] > ACTION_COOLDOWN:
                # Proportional hscroll for smoother control
                hscroll_factor = abs(dx) / HSCROLL_THRESHOLD
                hscroll_amount = int(50 * hscroll_factor)  # Base amount scaled by how far head is moved
                if dx < -HSCROLL_THRESHOLD:
                    horizontal_scroll(-hscroll_amount)  # Left: negative
                elif dx > HSCROLL_THRESHOLD:
                    horizontal_scroll(hscroll_amount)  # Right: positive
                last_action_time['horizontal'] = current_time

            # Draw neutral position visual
            cv2.circle(frame, (neutral_x, neutral_y), 6, (0,255,255), 2)
            cv2.line(frame, (neutral_x, 0), (neutral_x, h), (0,255,255), 1)
            cv2.line(frame, (0, neutral_y), (w, neutral_y), (0,255,255), 1)

    # UI Text
    if not calibrated:
        cv2.putText(frame, "Press 'c' to calibrate neutral head", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
    else:
        cv2.putText(frame, "Calibrated! Move your head to scroll vertically/horizontally", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.imshow("Head Control UX", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC
        break
    elif key == ord('c'):
        if results.multi_face_landmarks:
            # Use smoothed position for calibration
            neutral_x = smooth_x
            neutral_y = smooth_y
            calibrated = True
            print(f"Calibrated at: {neutral_x}, {neutral_y}")

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