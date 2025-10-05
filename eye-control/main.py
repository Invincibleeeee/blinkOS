
import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import math
from collections import deque
import sys
from scipy.spatial.distance import cdist
from scipy.interpolate import RBFInterpolator

# Disable pyautogui failsafe
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

class PrecisionEyeTracker:
    def __init__(self):
        # HIGH ACCURACY CONFIGURATION
        self.CAM_TRY_INDICES = [0, 1, 2, 3]
        self.CAM_W, self.CAM_H = 1280, 720  # Higher resolution for better accuracy
        
        # 9-POINT CALIBRATION GRID (3x3)
        self.CALIB_MARGIN = 0.08  # Smaller margin for more screen coverage
        self.CALIB_GRID_SIZE = 3  # 3x3 = 9 points
        self.CALIB_HOLD_FRAMES = 100  # More samples for precision
        self.CALIB_MIN_STABLE_FRAMES = 60  # Very strict stability
        self.CALIB_STABLE_TOLERANCE = 1.5  # Extremely tight tolerance
        
        # PRECISION SMOOTHING - Balanced for accuracy
        self.SMOOTHING_BUFFER_SIZE = 8  # Smaller buffer for responsiveness
        self.PRECISION_ALPHA = 0.35  # More responsive than ultra-stable
        self.PRECISION_DEADZONE = 3   # Smaller deadzone for accuracy
        self.MIN_MOVEMENT_THRESHOLD = 1.5  # Detect smaller movements
        self.OUTLIER_THRESHOLD = 25  # Tighter outlier detection
        
        # ADVANCED MAPPING
        self.USE_RBF_INTERPOLATION = True  # Radial Basis Function for local accuracy
        self.USE_LOCAL_WEIGHTING = True    # Weight nearby calibration points more
        self.RBF_SMOOTHING = 0.1          # RBF smoothing parameter
        
        # BLINK CLICKING FOR TYPING
        self.BLINK_THRESHOLD = 0.25  # Initial EAR threshold, will be calibrated
        self.BLINK_DEBOUNCE = 0.5  # Seconds between clicks to prevent rapid firing
        self.last_blink_time = 0
        self.was_blink = False
        
        # KEYBOARD OPTIMIZATION
        self.KEYBOARD_MODE = True  # Special mode for typing
        self.TYPING_PRECISION_BOOST = True  # Extra precision near keyboard area
        
        # UI
        self.PREVIEW_WINDOW = "Precision Eye Tracker - Typing Ready"
        self.CALIB_WINDOW = "9-Point Calibration - Maximum Accuracy"
        self.FONT = cv2.FONT_HERSHEY_SIMPLEX
        
        # Initialize
        self.setup_camera()
        self.setup_mediapipe()
        self.setup_screen()
        self.setup_advanced_filters()
        self.reset_calibration()
        
        # Windows
        cv2.namedWindow(self.PREVIEW_WINDOW, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.PREVIEW_WINDOW, 1000, 700)
        cv2.namedWindow(self.CALIB_WINDOW, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.CALIB_WINDOW, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        print("🎯 PRECISION EYE TRACKER INITIALIZED!")
        print("📝 Optimized for on-screen keyboard typing")
        print(f"🎯 {len(self.calib_points)} calibration points for maximum accuracy")
        print("👁️ Blink-click enabled: Look at target and blink to click")
        print("Controls: C=calibrate | SPACE=accept | N=skip | ESC=quit")

    def setup_camera(self):
        """Enhanced camera setup for precision"""
        self.cap = None
        self.cam_index = None
        
        for idx in self.CAM_TRY_INDICES:
            print(f"[CAMERA] Trying camera {idx}...")
            try:
                cap = cv2.VideoCapture(idx)
                if cap and cap.isOpened():
                    # Set higher resolution for better precision
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.CAM_W)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.CAM_H)
                    cap.set(cv2.CAP_PROP_FPS, 60)  # Higher FPS if possible
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Manual exposure for stability
                    
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        self.cap = cap
                        self.cam_index = idx
                        actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        print(f"[CAMERA] Opened camera {idx} at {actual_w}x{actual_h}")
                        return
                cap.release()
            except Exception as e:
                print(f"[CAMERA] Error with camera {idx}: {e}")
                
        print("[ERROR] Could not initialize camera!")
        sys.exit(1)

    def setup_mediapipe(self):
        """Ultra-precise MediaPipe setup"""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            refine_landmarks=True,
            max_num_faces=1,
            min_detection_confidence=0.8,  # Higher confidence
            min_tracking_confidence=0.8
        )
        
        # Enhanced landmark sets
        self.LEFT_IRIS = [468, 469, 470, 471]
        self.RIGHT_IRIS = [473, 474, 475, 476]
        self.LEFT_EYE_CORNERS = [33, 133]
        self.RIGHT_EYE_CORNERS = [362, 263]
        
        # Additional reference points for stability
        self.NOSE_TIP = 1
        self.FACE_CENTER = 9
        
        # Blink detection points - matching the patented formula with two vertical measurements
        self.LEFT_EYE_INDICES = [33, 133, 159, 145, 158, 144]  # h_left, h_right, upper1, lower1, upper2, lower2
        self.RIGHT_EYE_INDICES = [263, 362, 386, 374, 387, 373]

    def setup_screen(self):
        """Create 9-point calibration grid"""
        try:
            self.SCREEN_W, self.SCREEN_H = pyautogui.size()
            print(f"[SCREEN] Resolution: {self.SCREEN_W}x{self.SCREEN_H}")
            
            # Create 3x3 calibration grid for essential accuracy
            margin_x = int(self.SCREEN_W * self.CALIB_MARGIN)
            margin_y = int(self.SCREEN_H * self.CALIB_MARGIN)
            
            # Generate grid points
            x_points = np.linspace(margin_x, self.SCREEN_W - margin_x, self.CALIB_GRID_SIZE)
            y_points = np.linspace(margin_y, self.SCREEN_H - margin_y, self.CALIB_GRID_SIZE)
            
            self.calib_points = []
            for y in y_points:
                for x in x_points:
                    self.calib_points.append((int(x), int(y)))
            
            print(f"[CALIBRATION] Created {len(self.calib_points)}-point precision grid")
            
            # Define keyboard area for precision boosting
            self.keyboard_area = {
                'top': int(self.SCREEN_H * 0.6),
                'bottom': self.SCREEN_H,
                'left': 0,
                'right': self.SCREEN_W
            }
            
        except Exception as e:
            print(f"[ERROR] Screen setup failed: {e}")
            sys.exit(1)

    def setup_advanced_filters(self):
        """Initialize advanced filtering systems"""
        self.position_buffer = deque(maxlen=self.SMOOTHING_BUFFER_SIZE)
        self.velocity_buffer = deque(maxlen=4)
        self.acceleration_buffer = deque(maxlen=3)
        
        # Precision tracking
        self.last_raw_pos = None
        self.last_smooth_pos = None
        self.last_output_pos = None
        self.consecutive_stable_frames = 0
        
        # Advanced smoothing weights (recent samples more important)
        self.weights = np.exp(np.linspace(-1, 0, self.SMOOTHING_BUFFER_SIZE))
        self.weights /= self.weights.sum()

    def reset_calibration(self):
        """Reset calibration state"""
        self.calibration_data = []
        self.screen_points = []
        self.calib_index = -1
        self.sample_buffer = deque(maxlen=self.CALIB_HOLD_FRAMES)
        self.stability_counter = 0
        self.open_ear_values = []  # For calibrating EAR threshold
        
        # Reset mapping
        self.rbf_interpolator_x = None
        self.rbf_interpolator_y = None
        self.mapping_weights_x = None
        self.mapping_weights_y = None
        
        # Reset filters
        self.setup_advanced_filters()

    def get_landmark_coords(self, landmarks, index, img_width, img_height):
        """High-precision landmark coordinate extraction"""
        lm = landmarks[index]
        # Use sub-pixel precision
        return lm.x * img_width, lm.y * img_height

    def get_iris_center_precise(self, landmarks, iris_indices, img_width, img_height):
        """Ultra-precise iris center calculation"""
        points = [self.get_landmark_coords(landmarks, idx, img_width, img_height) 
                 for idx in iris_indices]
        
        # Weighted center (some iris points are more reliable)
        weights = [1.2, 1.0, 1.2, 1.0]  # Top and bottom points slightly more weight
        
        x_coords = [p[0] * w for p, w in zip(points, weights)]
        y_coords = [p[1] * w for p, w in zip(points, weights)]
        
        total_weight = sum(weights)
        return sum(x_coords) / total_weight, sum(y_coords) / total_weight

    def calculate_ear(self, landmarks, eye_indices, img_width, img_height):
        """Calculate Eye Aspect Ratio using patented formula"""
        p_hleft = np.array(self.get_landmark_coords(landmarks, eye_indices[0], img_width, img_height))
        p_hright = np.array(self.get_landmark_coords(landmarks, eye_indices[1], img_width, img_height))
        p_upper1 = np.array(self.get_landmark_coords(landmarks, eye_indices[2], img_width, img_height))
        p_lower1 = np.array(self.get_landmark_coords(landmarks, eye_indices[3], img_width, img_height))
        p_upper2 = np.array(self.get_landmark_coords(landmarks, eye_indices[4], img_width, img_height))
        p_lower2 = np.array(self.get_landmark_coords(landmarks, eye_indices[5], img_width, img_height))
        
        v1 = np.linalg.norm(p_upper1 - p_lower1)
        v2 = np.linalg.norm(p_upper2 - p_lower2)
        h = np.linalg.norm(p_hleft - p_hright)
        
        return (v1 + v2) / (2.0 * h)

    def detect_blink(self, landmarks, img_width, img_height):
        """Detect if a blink is occurring"""
        left_ear = self.calculate_ear(landmarks, self.LEFT_EYE_INDICES, img_width, img_height)
        right_ear = self.calculate_ear(landmarks, self.RIGHT_EYE_INDICES, img_width, img_height)
        avg_ear = (left_ear + right_ear) / 2.0
        return avg_ear < self.BLINK_THRESHOLD

    def extract_precision_gaze_features(self, landmarks, img_width, img_height):
        """Extract high-precision gaze features with head pose compensation and EAR"""
        try:
            # Get eye corners with sub-pixel precision
            left_outer = self.get_landmark_coords(landmarks, self.LEFT_EYE_CORNERS[0], img_width, img_height)
            left_inner = self.get_landmark_coords(landmarks, self.LEFT_EYE_CORNERS[1], img_width, img_height)
            right_inner = self.get_landmark_coords(landmarks, self.RIGHT_EYE_CORNERS[0], img_width, img_height)
            right_outer = self.get_landmark_coords(landmarks, self.RIGHT_EYE_CORNERS[1], img_width, img_height)
            
            # Get face reference points for head pose compensation
            nose_tip = self.get_landmark_coords(landmarks, self.NOSE_TIP, img_width, img_height)
            face_center = self.get_landmark_coords(landmarks, self.FACE_CENTER, img_width, img_height)
            
            # Calculate eye parameters with head pose compensation
            left_center_x = (left_outer[0] + left_inner[0]) / 2.0
            left_center_y = (left_outer[1] + left_inner[1]) / 2.0
            left_width = math.hypot(left_inner[0] - left_outer[0], left_inner[1] - left_outer[1])
            
            right_center_x = (right_inner[0] + right_outer[0]) / 2.0
            right_center_y = (right_inner[1] + right_outer[1]) / 2.0
            right_width = math.hypot(right_outer[0] - right_inner[0], right_outer[1] - right_inner[1])
            
            # Ensure minimum eye width for stability
            left_width = max(25.0, left_width)
            right_width = max(25.0, right_width)
            
            # Get precise iris centers
            left_iris_x, left_iris_y = self.get_iris_center_precise(landmarks, self.LEFT_IRIS, img_width, img_height)
            right_iris_x, right_iris_y = self.get_iris_center_precise(landmarks, self.RIGHT_IRIS, img_width, img_height)
            
            # Normalize with enhanced precision
            left_norm_x = (left_iris_x - left_center_x) / left_width
            left_norm_y = (left_iris_y - left_center_y) / left_width
            right_norm_x = (right_iris_x - right_center_x) / right_width
            right_norm_y = (right_iris_y - right_center_y) / right_width
            
            # Clamp to prevent extreme values
            left_norm_x = np.clip(left_norm_x, -0.6, 0.6)
            left_norm_y = np.clip(left_norm_y, -0.4, 0.4)
            right_norm_x = np.clip(right_norm_x, -0.6, 0.6)
            right_norm_y = np.clip(right_norm_y, -0.4, 0.4)
            
            # Enhanced averaging with eye dominance consideration
            eye_dominance = 0.55  # Slight left eye preference (adjustable)
            gaze_x = left_norm_x * eye_dominance + right_norm_x * (1 - eye_dominance)
            gaze_y = left_norm_y * eye_dominance + right_norm_y * (1 - eye_dominance)
            
            # Head pose compensation
            head_tilt_x = (nose_tip[0] - face_center[0]) / img_width
            head_tilt_y = (nose_tip[1] - face_center[1]) / img_height
            
            # Compensate gaze for head pose
            gaze_x -= head_tilt_x * 0.3
            gaze_y -= head_tilt_y * 0.2
            
            # Calculate average EAR for calibration
            left_ear = self.calculate_ear(landmarks, self.LEFT_EYE_INDICES, img_width, img_height)
            right_ear = self.calculate_ear(landmarks, self.RIGHT_EYE_INDICES, img_width, img_height)
            avg_ear = (left_ear + right_ear) / 2.0
            
            return gaze_x, gaze_y, {
                'left_iris': (left_iris_x, left_iris_y),
                'right_iris': (right_iris_x, right_iris_y),
                'left_center': (left_center_x, left_center_y),
                'right_center': (right_center_x, right_center_y),
                'head_pose': (head_tilt_x, head_tilt_y)
            }, avg_ear
            
        except Exception as e:
            return None, None, None, None

    def fit_precision_mapping(self):
        """Fit high-precision mapping using RBF interpolation"""
        try:
            if len(self.calibration_data) < 6:  # Need fewer points for RBF with reduced grid
                print(f"[WARN] Need at least 6 calibration points, have {len(self.calibration_data)}")
                return False
            
            calib_array = np.array(self.calibration_data)
            screen_array = np.array(self.screen_points)
            
            if self.USE_RBF_INTERPOLATION:
                # Use RBF interpolation for local accuracy
                print("[MAPPING] Using RBF interpolation for maximum accuracy...")
                
                try:
                    self.rbf_interpolator_x = RBFInterpolator(
                        calib_array, screen_array[:, 0],
                        smoothing=self.RBF_SMOOTHING,
                        kernel='thin_plate_spline'  # Best for 2D mapping
                    )
                    self.rbf_interpolator_y = RBFInterpolator(
                        calib_array, screen_array[:, 1],
                        smoothing=self.RBF_SMOOTHING,
                        kernel='thin_plate_spline'
                    )
                    
                    print(f"[SUCCESS] RBF mapping created with {len(self.calibration_data)} points")
                    return True
                    
                except Exception as e:
                    print(f"[WARN] RBF failed, falling back to polynomial: {e}")
                    # Fallback to polynomial mapping
                    return self.fit_polynomial_mapping()
            else:
                return self.fit_polynomial_mapping()
                
        except Exception as e:
            print(f"[ERROR] Mapping failed: {e}")
            return False

    def fit_polynomial_mapping(self):
        """Fallback polynomial mapping with local weighting"""
        try:
            calib_array = np.array(self.calibration_data)
            screen_array = np.array(self.screen_points)
            
            # Enhanced polynomial features for better accuracy
            def create_features(gx, gy):
                return np.array([
                    1.0, gx, gy,                    # Linear
                    gx*gy, gx*gx, gy*gy,           # Quadratic
                    gx*gx*gy, gx*gy*gy,            # Cubic interactions
                    gx*gx*gx, gy*gy*gy             # Pure cubic
                ])
            
            # Create feature matrix
            feature_matrix = np.stack([create_features(gx, gy) for gx, gy in calib_array])
            
            # Strong regularization for stability
            ridge_lambda = 1e-3
            regularization = ridge_lambda * np.eye(feature_matrix.shape[1])
            gram_matrix = feature_matrix.T @ feature_matrix + regularization
            
            # Solve for weights
            self.mapping_weights_x = np.linalg.solve(gram_matrix, feature_matrix.T @ screen_array[:, 0])
            self.mapping_weights_y = np.linalg.solve(gram_matrix, feature_matrix.T @ screen_array[:, 1])
            
            self.create_features = create_features  # Store for later use
            
            print(f"[SUCCESS] Polynomial mapping created with {len(self.calibration_data)} points")
            return True
            
        except Exception as e:
            print(f"[ERROR] Polynomial mapping failed: {e}")
            return False

    def map_gaze_to_screen_precise(self, gaze_x, gaze_y):
        """High-precision gaze to screen mapping"""
        if self.rbf_interpolator_x is not None and self.rbf_interpolator_y is not None:
            # Use RBF interpolation
            try:
                query_point = np.array([[gaze_x, gaze_y]])
                screen_x = float(self.rbf_interpolator_x(query_point)[0])
                screen_y = float(self.rbf_interpolator_y(query_point)[0])
                
                # Apply local precision boosting in keyboard area
                if self.is_in_keyboard_area(screen_x, screen_y):
                    screen_x, screen_y = self.apply_keyboard_precision_boost(screen_x, screen_y, gaze_x, gaze_y)
                
            except Exception as e:
                print(f"[WARN] RBF mapping error: {e}")
                return None, None
                
        elif self.mapping_weights_x is not None and self.mapping_weights_y is not None:
            # Use polynomial mapping
            try:
                features = self.create_features(gaze_x, gaze_y)
                screen_x = float(np.dot(self.mapping_weights_x, features))
                screen_y = float(np.dot(self.mapping_weights_y, features))
            except Exception as e:
                print(f"[WARN] Polynomial mapping error: {e}")
                return None, None
        else:
            return None, None
        
        # Clamp to screen bounds
        screen_x = max(5, min(self.SCREEN_W - 5, screen_x))
        screen_y = max(5, min(self.SCREEN_H - 5, screen_y))
        
        return screen_x, screen_y

    def is_in_keyboard_area(self, x, y):
        """Check if position is in typical keyboard area"""
        return (self.keyboard_area['left'] <= x <= self.keyboard_area['right'] and
                self.keyboard_area['top'] <= y <= self.keyboard_area['bottom'])

    def apply_keyboard_precision_boost(self, screen_x, screen_y, gaze_x, gaze_y):
        """Apply extra precision in keyboard area using local calibration points"""
        if not self.USE_LOCAL_WEIGHTING:
            return screen_x, screen_y
            
        try:
            # Find nearest calibration points in keyboard area
            keyboard_calib_points = []
            keyboard_screen_points = []
            
            for i, (calib_gaze, screen_point) in enumerate(zip(self.calibration_data, self.screen_points)):
                if self.is_in_keyboard_area(screen_point[0], screen_point[1]):
                    keyboard_calib_points.append(calib_gaze)
                    keyboard_screen_points.append(screen_point)
            
            if len(keyboard_calib_points) >= 3:
                # Use local weighted interpolation
                calib_array = np.array(keyboard_calib_points)
                screen_array = np.array(keyboard_screen_points)
                
                # Calculate distances to current gaze point
                distances = cdist([[gaze_x, gaze_y]], calib_array)[0]
                
                # Use inverse distance weighting with higher precision
                weights = 1.0 / (distances + 0.01)  # Small epsilon to avoid division by zero
                weights = weights / np.sum(weights)
                
                # Apply local correction
                local_x = np.sum(screen_array[:, 0] * weights)
                local_y = np.sum(screen_array[:, 1] * weights)
                
                # Blend with original estimate (favor local in keyboard area)
                blend_factor = 0.7
                screen_x = screen_x * (1 - blend_factor) + local_x * blend_factor
                screen_y = screen_y * (1 - blend_factor) + local_y * blend_factor
                
        except Exception as e:
            pass  # If local boost fails, use original estimate
            
        return screen_x, screen_y

    def apply_precision_smoothing(self, raw_x, raw_y):
        """Precision-focused smoothing that preserves accuracy"""
        if raw_x is None or raw_y is None:
            return None, None
        
        current_pos = np.array([raw_x, raw_y])
        
        # STAGE 1: Outlier rejection with tighter threshold
        if len(self.position_buffer) >= 3:
            recent_positions = np.array(list(self.position_buffer)[-3:])
            median_pos = np.median(recent_positions, axis=0)
            distance = np.linalg.norm(current_pos - median_pos)
            
            if distance > self.OUTLIER_THRESHOLD:
                # Clamp outlier to max jump distance
                direction = (current_pos - median_pos) / distance
                current_pos = median_pos + direction * self.OUTLIER_THRESHOLD
        
        # Add to buffer
        self.position_buffer.append(current_pos)
        
        if len(self.position_buffer) < 3:
            self.last_raw_pos = current_pos
            return current_pos[0], current_pos[1]
        
        # STAGE 2: Adaptive weighted averaging
        buffer_array = np.array(list(self.position_buffer))
        
        # Calculate movement variance to adjust smoothing
        if len(buffer_array) >= 4:
            recent_movement = np.std(buffer_array[-4:], axis=0)
            movement_intensity = np.mean(recent_movement)
            
            # Adapt smoothing based on movement - less smoothing when moving fast
            adaptive_alpha = self.PRECISION_ALPHA * (1.0 + movement_intensity * 0.5)
            adaptive_alpha = min(0.8, adaptive_alpha)  # Cap at 0.8 for responsiveness
        else:
            adaptive_alpha = self.PRECISION_ALPHA
        
        # Apply weighted moving average
        weighted_pos = np.average(buffer_array, axis=0, weights=self.weights[:len(buffer_array)])
        
        # STAGE 3: Exponential smoothing with adaptation
        if self.last_smooth_pos is not None:
            smoothed_pos = adaptive_alpha * weighted_pos + (1 - adaptive_alpha) * self.last_smooth_pos
        else:
            smoothed_pos = weighted_pos
        
        # STAGE 4: Precision deadzone (smaller than ultra-stable version)
        if self.last_output_pos is not None:
            distance_from_last = np.linalg.norm(smoothed_pos - self.last_output_pos)
            
            if distance_from_last < self.PRECISION_DEADZONE:
                # In precision deadzone - minimal movement
                smoothed_pos = self.last_output_pos * 0.7 + smoothed_pos * 0.3
            elif distance_from_last < self.MIN_MOVEMENT_THRESHOLD:
                # Small movement - gentle smoothing
                smoothed_pos = self.last_output_pos * 0.5 + smoothed_pos * 0.5
        
        # Update tracking
        self.last_smooth_pos = smoothed_pos.copy()
        self.last_output_pos = smoothed_pos.copy()
        
        return float(smoothed_pos[0]), float(smoothed_pos[1])

    def handle_blink_clicking(self, cursor_x, cursor_y, landmarks, img_width, img_height):
        """Handle blink-based clicking for typing"""
        try:
            current_time = time.time()
            is_blink = self.detect_blink(landmarks, img_width, img_height)
            
            if is_blink and not self.was_blink and (current_time - self.last_blink_time > self.BLINK_DEBOUNCE):
                # Blink onset detected
                print(f"[BLINK] Click at ({int(cursor_x)}, {int(cursor_y)})")
                pyautogui.click(int(cursor_x), int(cursor_y))
                self.last_blink_time = current_time
                
            self.was_blink = is_blink
            
        except Exception as e:
            print(f"[WARN] Blink click error: {e}")

    def draw_calibration_screen_25point(self):
        """Draw 9-point calibration interface"""
        canvas = np.ones((self.SCREEN_H, self.SCREEN_W, 3), dtype=np.uint8) * 250
        
        if 0 <= self.calib_index < len(self.calib_points):
            target_x, target_y = self.calib_points[self.calib_index]
            
            # Draw precision target
            cv2.circle(canvas, (target_x, target_y), 35, (0, 0, 0), -1)
            cv2.circle(canvas, (target_x, target_y), 60, (80, 80, 80), 4)
            cv2.circle(canvas, (target_x, target_y), 8, (255, 255, 255), -1)
            cv2.circle(canvas, (target_x, target_y), 2, (0, 0, 0), -1)
            
            # Progress info
            progress_text = f"PRECISION CALIBRATION: POINT {self.calib_index + 1} OF {len(self.calib_points)}"
            cv2.putText(canvas, progress_text, (50, 80), self.FONT, 1.6, (0, 0, 0), 3)
            
            # Grid position info
            grid_row = self.calib_index // self.CALIB_GRID_SIZE + 1
            grid_col = self.calib_index % self.CALIB_GRID_SIZE + 1
            grid_text = f"Grid Position: Row {grid_row}, Column {grid_col}"
            cv2.putText(canvas, grid_text, (50, 130), self.FONT, 1.2, (60, 60, 60), 2)
            
            # Instructions
            instructions = [
                "LOOK AT THE CENTER DOT AND HOLD PERFECTLY STILL",
                "This 9-point calibration ensures surgical precision for typing",
                "Each point needs 100 stable samples - please be patient",
                "Press SPACE to accept manually | Press N to skip problematic points"
            ]
            
            for i, instruction in enumerate(instructions):
                cv2.putText(canvas, instruction, (50, 180 + i * 40), self.FONT, 0.9, (80, 80, 80), 2)
            
            # Show all calibration points as dots
            for i, (px, py) in enumerate(self.calib_points):
                if i < self.calib_index:
                    # Completed points - green
                    cv2.circle(canvas, (px, py), 8, (0, 180, 0), -1)
                elif i == self.calib_index:
                    # Current point - already drawn above
                    pass
                else:
                    # Future points - gray
                    cv2.circle(canvas, (px, py), 4, (150, 150, 150), -1)
                    
        else:
            # Idle state
            title = "PRECISION EYE TRACKER - TYPING OPTIMIZED"
            cv2.putText(canvas, title, (self.SCREEN_W//2 - 450, self.SCREEN_H//2 - 100), 
                       self.FONT, 2.0, (0, 0, 0), 4)
            
            subtitle = "9-Point Calibration for Maximum Accuracy"
            cv2.putText(canvas, subtitle, (self.SCREEN_W//2 - 350, self.SCREEN_H//2 - 50), 
                       self.FONT, 1.4, (60, 60, 60), 3)
            
            instruction = "Press 'C' to start precision calibration"
            cv2.putText(canvas, instruction, (self.SCREEN_W//2 - 280, self.SCREEN_H//2 + 20), 
                       self.FONT, 1.2, (0, 0, 0), 2)
            
            blink_status = "Blink-click: ENABLED"
            cv2.putText(canvas, blink_status, (self.SCREEN_W//2 - 300, self.SCREEN_H//2 + 80), 
                       self.FONT, 1.0, (0, 100, 200), 2)
        
        cv2.imshow(self.CALIB_WINDOW, canvas)

    def draw_enhanced_progress_bars(self, frame, sample_progress, stability_progress):
        """Enhanced progress visualization for precision calibration"""
        h, w = frame.shape[:2]
        
        # Sample collection progress
        bar_width = int(w * 0.8)
        bar_x = (w - bar_width) // 2
        sample_y = h - 120
        
        cv2.rectangle(frame, (bar_x, sample_y), (bar_x + bar_width, sample_y + 30), (30, 30, 30), -1)
        cv2.rectangle(frame, (bar_x, sample_y), (bar_x + int(bar_width * sample_progress), sample_y + 30), (0, 200, 0), -1)
        cv2.putText(frame, f"SAMPLES: {len(self.sample_buffer)}/{self.CALIB_HOLD_FRAMES} ({int(sample_progress * 100)}%)", 
                   (bar_x, sample_y - 10), self.FONT, 0.8, (255, 255, 255), 2)
        
        # Stability progress
        stability_y = h - 80
        stability_width = int(bar_width * stability_progress)
        
        cv2.rectangle(frame, (bar_x, stability_y), (bar_x + bar_width, stability_y + 25), (30, 30, 30), -1)
        cv2.rectangle(frame, (bar_x, stability_y), (bar_x + stability_width, stability_y + 25), (0, 255, 255), -1)
        cv2.putText(frame, f"STABILITY: {self.stability_counter}/{self.CALIB_MIN_STABLE_FRAMES} ({int(stability_progress * 100)}%)", 
                   (bar_x, stability_y - 10), self.FONT, 0.8, (255, 255, 255), 2)
        
        # Precision indicator
        if stability_progress >= 1.0 and sample_progress >= 1.0:
            cv2.putText(frame, "PRECISION TARGET ACHIEVED - ADVANCING!", 
                       (bar_x, stability_y - 50), self.FONT, 0.9, (0, 255, 0), 2)
        elif stability_progress < 0.2:
            cv2.putText(frame, "HOLD PERFECTLY STILL - PRECISION REQUIRED!", 
                       (bar_x, stability_y - 50), self.FONT, 0.9, (0, 150, 255), 2)

    def process_precision_calibration(self, frame, gaze_x, gaze_y, avg_ear):
        """Process calibration point with precision requirements and EAR calibration"""
        self.sample_buffer.append((gaze_x, gaze_y))
        
        # Ultra-strict stability checking
        if len(self.sample_buffer) >= 15:
            # Check stability over larger window for precision
            recent_samples = list(self.sample_buffer)[-15:]
            recent_array = np.array(recent_samples)
            
            # Calculate stability metrics
            std_x = np.std(recent_array[:, 0])
            std_y = np.std(recent_array[:, 1])
            max_std = max(std_x, std_y)
            
            # Very tight stability requirement
            if max_std < (self.CALIB_STABLE_TOLERANCE / 100.0):
                self.stability_counter += 1
                self.open_ear_values.append(avg_ear)  # Collect open eye EAR during stable frames
            else:
                # Decrease stability counter more aggressively for precision
                self.stability_counter = max(0, self.stability_counter - 5)
        
        # Progress indicators
        sample_progress = len(self.sample_buffer) / self.CALIB_HOLD_FRAMES
        stability_progress = min(1.0, self.stability_counter / self.CALIB_MIN_STABLE_FRAMES)
        
        self.draw_enhanced_progress_bars(frame, sample_progress, stability_progress)
        
        # Auto-advance with very strict requirements
        if (len(self.sample_buffer) >= self.CALIB_HOLD_FRAMES and 
            self.stability_counter >= self.CALIB_MIN_STABLE_FRAMES):
            self.accept_precision_calibration_point()

    def accept_precision_calibration_point(self):
        """Accept calibration point with precision averaging"""
        if len(self.sample_buffer) > 20:
            samples_array = np.array(list(self.sample_buffer))
            
            # Use only the most stable samples (middle 50% after sorting by stability)
            center_start = int(len(samples_array) * 0.25)
            center_end = int(len(samples_array) * 0.75)
            
            # Sort by distance from median to find most stable samples
            median_sample = np.median(samples_array, axis=0)
            distances = [np.linalg.norm(sample - median_sample) for sample in samples_array]
            sorted_indices = np.argsort(distances)
            
            # Use the most stable samples
            stable_indices = sorted_indices[:int(len(sorted_indices) * 0.6)]
            stable_samples = samples_array[stable_indices]
            
            # Precision weighted average (central samples have higher weight)
            weights = np.ones(len(stable_samples))
            center_idx = len(stable_samples) // 2
            
            for i in range(len(weights)):
                distance_from_center = abs(i - center_idx)
                weights[i] = 1.0 / (1.0 + distance_from_center * 0.05)
            
            weights /= weights.sum()
            
            avg_x = np.average(stable_samples[:, 0], weights=weights)
            avg_y = np.average(stable_samples[:, 1], weights=weights)
            
            self.calibration_data.append((avg_x, avg_y))
            self.screen_points.append(self.calib_points[self.calib_index])
            
            print(f"[PRECISION] Point {self.calib_index + 1}/{len(self.calib_points)} - Precision: {np.std(stable_samples, axis=0)}")
            
            # Reset for next point
            self.sample_buffer.clear()
            self.stability_counter = 0
            self.calib_index += 1
            
            if self.calib_index >= len(self.calib_points):
                self.complete_precision_calibration()
            else:
                time.sleep(0.4)  # Longer pause for precision

    def complete_precision_calibration(self):
        """Complete precision calibration and set personalized EAR threshold"""
        success = self.fit_precision_mapping()
        
        if success:
            print("🎯 PRECISION CALIBRATION COMPLETED! 🎯")
            print(f"📍 {len(self.calibration_data)} points calibrated for maximum accuracy")
            print("⌨️ Ready for precise on-screen keyboard typing!")
            print("👁️ Blink-click ENABLED")
            
            # Calibrate EAR threshold based on collected open eye values
            if self.open_ear_values:
                avg_open_ear = np.mean(self.open_ear_values)
                self.BLINK_THRESHOLD = max(0.15, min(0.3, avg_open_ear * 0.75))
                print(f"[EAR CALIB] Average open EAR: {avg_open_ear:.4f}, set blink threshold to {self.BLINK_THRESHOLD:.4f}")
            else:
                print("[WARN] No EAR values collected, using default threshold")
            
            self.calib_index = -1  # Enter tracking mode
            
            # Reset smoothing for clean tracking start
            self.setup_advanced_filters()
            
        else:
            print("[ERROR] Precision calibration failed - please try again")
            self.reset_calibration()
        
        time.sleep(0.5)

    def run_precision_tracking(self):
        """Main precision tracking loop"""
        self.draw_calibration_screen_25point()
        frame_count = 0
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.01)
                continue
                
            frame_count += 1
            frame = cv2.flip(frame, 1)
            frame_height, frame_width = frame.shape[:2]
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            try:
                results = self.face_mesh.process(rgb_frame)
            except Exception:
                results = None
            
            # Process at full frame rate for precision
            if results and results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark
                gaze_x, gaze_y, eye_info, avg_ear = self.extract_precision_gaze_features(landmarks, frame_width, frame_height)
                
                if gaze_x is not None and gaze_y is not None and eye_info is not None:
                    # Draw precision eye tracking overlay
                    self.draw_precision_overlay(frame, eye_info)
                    
                    # Handle calibration
                    if 0 <= self.calib_index < len(self.calib_points):
                        self.process_precision_calibration(frame, gaze_x, gaze_y, avg_ear)
                        
                    # Handle precision tracking
                    elif (self.rbf_interpolator_x is not None or self.mapping_weights_x is not None):
                        self.process_precision_tracking(frame, gaze_x, gaze_y, landmarks, frame_width, frame_height)
                        
                    else:
                        cv2.putText(frame, "READY FOR 9-POINT PRECISION CALIBRATION - Press 'C'", 
                                   (10, 30), self.FONT, 0.7, (0, 255, 255), 2)
                else:
                    cv2.putText(frame, "Eye tracking failed - adjust lighting/position", 
                               (10, 30), self.FONT, 0.7, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Face not detected - center face in camera view", 
                           (10, 30), self.FONT, 0.7, (0, 0, 255), 2)
            
            # Show accuracy metrics
            if hasattr(self, 'last_output_pos') and self.last_output_pos is not None:
                accuracy_text = f"Precision Mode: {len(self.calibration_data)} cal points"
                cv2.putText(frame, accuracy_text, (frame_width - 400, 30), self.FONT, 0.6, (0, 255, 0), 2)
                
                blink_text = f"Blink: ENABLED (Threshold: {self.BLINK_THRESHOLD:.2f})"
                cv2.putText(frame, blink_text, (frame_width - 300, 60), self.FONT, 0.6, (255, 255, 0), 2)
            
            cv2.imshow(self.PREVIEW_WINDOW, frame)
            self.draw_calibration_screen_25point()
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if not self.handle_precision_keyboard(key):
                break
        
        self.cleanup()

    def process_precision_tracking(self, frame, gaze_x, gaze_y, landmarks, img_width, img_height):
        """Process precision tracking with blink-click support"""
        raw_x, raw_y = self.map_gaze_to_screen_precise(gaze_x, gaze_y)
        
        if raw_x is not None and raw_y is not None:
            # Apply precision smoothing
            smooth_x, smooth_y = self.apply_precision_smoothing(raw_x, raw_y)
            
            if smooth_x is not None and smooth_y is not None:
                try:
                    # Move cursor
                    pyautogui.moveTo(int(smooth_x), int(smooth_y))
                    
                    # Handle blink clicking for typing
                    self.handle_blink_clicking(smooth_x, smooth_y, landmarks, img_width, img_height)
                    
                    # Status display
                    cv2.putText(frame, f"PRECISION TRACKING: ({int(smooth_x)}, {int(smooth_y)})", 
                               (10, 30), self.FONT, 0.8, (0, 255, 0), 2)
                    
                    if self.is_in_keyboard_area(smooth_x, smooth_y):
                        cv2.putText(frame, "KEYBOARD AREA - ENHANCED PRECISION", 
                                   (10, 60), self.FONT, 0.7, (0, 255, 255), 2)
                    
                    if self.was_blink:
                        cv2.putText(frame, "BLINK DETECTED", 
                                   (10, 90), self.FONT, 0.7, (255, 255, 0), 2)
                    
                    cv2.putText(frame, "Controls: C=recalibrate | ESC=quit", 
                               (10, frame.shape[0] - 20), self.FONT, 0.6, (200, 200, 200), 2)
                               
                except Exception as e:
                    print(f"[WARN] Tracking error: {e}")

    def draw_precision_overlay(self, frame, eye_info):
        """Draw precision tracking visualization"""
        left_iris = eye_info['left_iris']
        right_iris = eye_info['right_iris']
        
        # Draw precise iris tracking
        cv2.circle(frame, (int(left_iris[0]), int(left_iris[1])), 4, (0, 255, 255), -1)
        cv2.circle(frame, (int(right_iris[0]), int(right_iris[1])), 4, (0, 255, 255), -1) 
        cv2.circle(frame, (int(left_iris[0]), int(left_iris[1])), 8, (0, 255, 255), 1)
        cv2.circle(frame, (int(right_iris[0]), int(right_iris[1])), 8, (0, 255, 255), 1)
        
        # Combined gaze point
        combined_x = (left_iris[0] + right_iris[0]) / 2
        combined_y = (left_iris[1] + right_iris[1]) / 2
        cv2.circle(frame, (int(combined_x), int(combined_y)), 6, (255, 0, 0), -1)
        cv2.circle(frame, (int(combined_x), int(combined_y)), 12, (255, 0, 0), 2)
        
        # Draw precision crosshair
        cv2.line(frame, (int(combined_x) - 15, int(combined_y)), 
                (int(combined_x) + 15, int(combined_y)), (255, 255, 255), 1)
        cv2.line(frame, (int(combined_x), int(combined_y) - 15), 
                (int(combined_x), int(combined_y) + 15), (255, 255, 255), 1)

    def handle_precision_keyboard(self, key):
        """Handle keyboard input for precision tracker"""
        if key == 27:  # ESC
            return False
            
        elif key in (ord('c'), ord('C')):
            print("🎯 Starting 9-point PRECISION calibration...")
            print("📝 This will take several minutes but ensures typing accuracy")
            self.reset_calibration()
            self.calib_index = 0
            
        elif key == 32:  # SPACE
            if 0 <= self.calib_index < len(self.calib_points):
                self.accept_precision_calibration_point()
                
        elif key in (ord('n'), ord('N')):
            if 0 <= self.calib_index < len(self.calib_points):
                print(f"⏭️ Skipping calibration point {self.calib_index + 1}")
                self.sample_buffer.clear()
                self.stability_counter = 0
                self.calib_index += 1
                
                if self.calib_index >= len(self.calib_points):
                    self.complete_precision_calibration()
        
        # Precision tuning during tracking
        elif key == ord('1'):
            self.PRECISION_ALPHA = max(0.1, self.PRECISION_ALPHA - 0.05)
            print(f"🎯 Increased smoothing: {self.PRECISION_ALPHA:.2f}")
        elif key == ord('2'):
            self.PRECISION_ALPHA = min(0.7, self.PRECISION_ALPHA + 0.05)
            print(f"🎯 Decreased smoothing: {self.PRECISION_ALPHA:.2f}")
        
        return True

    def cleanup(self):
        """Clean up resources"""
        if self.cap:
            self.cap.release() 
        cv2.destroyAllWindows()
        print("🎯 Precision eye tracker shut down")


# Main execution
if __name__ == "__main__":
    try:
        print("=" * 80)
        print("    🎯 PRECISION EYE TRACKER - TYPING OPTIMIZED 🎯")
        print("=" * 80)
        print("FEATURES:")
        print("• 9-point calibration grid (3x3) for essential accuracy")
        print("• RBF interpolation for local precision")
        print("• Keyboard area precision boosting")
        print("• Blink-click functionality for typing with personalized EAR threshold")
        print("• Enhanced head pose compensation")
        print("• Local weighted interpolation")
        print("• Precision-focused smoothing")
        print("• Patented EAR formula with user-specific calibration")
        print("=" * 80)
        print()
        print("TYPING CONTROLS:")
        print("• Look at letter and blink to type it")
        print("• Press 'C' to recalibrate for better accuracy")
        print()
        print("PRECISION TUNING (during tracking):")
        print("• Press 1/2: Adjust smoothing")
        print("=" * 80)
        print()
        
        tracker = PrecisionEyeTracker()
        tracker.run_precision_tracking()
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            cv2.destroyAllWindows()
        except:
            pass
        print("👋 Goodbye!")