
from config import (
    DEAD_ZONE_X,
    DEAD_ZONE_Y,
    MIN_SPEED,
    MAX_SPEED
)


def calculate_speed(error, dead_zone):
    """
    Elin merkezden uzaklığına göre hedef hızı hesaplar.
    """

    distance = abs(error)

    if distance <= dead_zone:
        return 0

    effective_distance = distance - dead_zone

    max_error = 320 - dead_zone

    ratio = min(effective_distance / max_error, 1.0)

    speed = MIN_SPEED + ratio * (MAX_SPEED - MIN_SPEED)

    return int(speed)


class SpeedSmoother:

    def __init__(self, smoothing_factor=0.3):
        self.current_speed = 0.0
        self.smoothing_factor = smoothing_factor

    def update(self, target_speed):

        self.current_speed += (
            self.smoothing_factor
            * (target_speed - self.current_speed)
        )

        return int(self.current_speed)


class Tracker:

    def __init__(self):

        self.smoother_x = SpeedSmoother(0.3)
        self.smoother_y = SpeedSmoother(0.3)

    def update(self, hand_center, frame_width, frame_height):

        center_x, center_y = hand_center

        camera_center_x = frame_width // 2
        camera_center_y = frame_height // 2

        error_x = center_x - camera_center_x
        error_y = center_y - camera_center_y

        # Yatay yön
        if abs(error_x) <= DEAD_ZONE_X:
            direction_x = "CENTER"
        elif error_x > 0:
            direction_x = "RIGHT"
        else:
            direction_x = "LEFT"

        # Dikey yön
        if abs(error_y) <= DEAD_ZONE_Y:
            direction_y = "CENTER"
        elif error_y > 0:
            direction_y = "DOWN"
        else:
            direction_y = "UP"

        # Hedef hızlar
        speed_x = calculate_speed(error_x, DEAD_ZONE_X)
        speed_y = calculate_speed(error_y, DEAD_ZONE_Y)

        # Yumuşatılmış hızlar
        smooth_speed_x = self.smoother_x.update(speed_x)
        smooth_speed_y = self.smoother_y.update(speed_y)

        return {
            "center": (center_x, center_y),
            "camera_center": (camera_center_x, camera_center_y),
            "error": (error_x, error_y),
            "direction": (direction_x, direction_y),
            "speed": (smooth_speed_x, smooth_speed_y)
        }

    def reset(self):

        self.smoother_x.update(0)
        self.smoother_y.update(0)
   
            