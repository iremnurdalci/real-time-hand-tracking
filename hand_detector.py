import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self):
        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,  # bir el arıyoruz
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.mp_draw = mp.solutions.drawing_utils
        # elin 21 noktasını görüntünün üzerine çizer

    def detect(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb_frame)
        # el algılama işlemi

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]

            # elin görüntüsünü çizme kısmı
            self.mp_draw.draw_landmarks(
                frame,
                hand,
                self.mp_hands.HAND_CONNECTIONS
            )

            return hand

        return None

    def get_hand_center(self, hand, frame_width, frame_height):
        """
        Elin 21 landmark noktasını kullanarak
        elin yaklaşık merkez koordinatını hesaplar.
        """

        x_coordinates = []
        y_coordinates = []

        for landmark in hand.landmark: # Elin 21 noktasının koordinatlarını alıyoruz
            x_coordinates.append(landmark.x)
            y_coordinates.append(landmark.y)

        # Ortalama X ve Y değerlerini hesaplıyoruz
        center_x = int(
            sum(x_coordinates) / len(x_coordinates) * frame_width
        )

        center_y = int(
            sum(y_coordinates) / len(y_coordinates) * frame_height
        )

        return center_x, center_y
   