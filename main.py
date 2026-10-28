import cv2
import time

from hand_detector import HandDetector
from config import DEAD_ZONE_X, DEAD_ZONE_Y


def main():
    detector = HandDetector()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Kamera açılamadı!")
        return

    print("Kamera başladı.")
    print("Çıkmak için Q tuşuna bas.")

    previous_time = time.time()

    while True:
        success, frame = cap.read()

        if not success:
            print("Görüntü alınamadı!")
            break

        frame = cv2.flip(frame, 1)

        hand = detector.detect(frame)
        if hand :
            height, width, _ = frame.shape
            center_x, center_y = detector.get_hand_center(hand, width, height)
            camera_center_x, camera_center_y = width // 2, height // 2 #kameranın merkezini bulma kısmı
            error_x = center_x - camera_center_x # el ile kamera arasındaki hata 
            error_y = center_y - camera_center_y
            if abs(error_x) <= DEAD_ZONE_X:
                direction_x = "Center" #merkezde
            elif error_x > 0:
                direction_x = "Right"   #sağda
            else:
                direction_x = "Left" # solda

            if abs(error_y) <= DEAD_ZONE_Y:
                    direction_y = "Center" 
            elif error_y > 0:
                    direction_y = "down"    
            else:
                    direction_y = "up"


            cv2.circle(frame, (center_x, center_y), 10, (0, 0, 255), -1)# elin merkezini kırmızı nokta olarak gösterir
            cv2.circle(frame, (camera_center_x, camera_center_y), 8, (255, 0, 0), -1) # kameranın merkezini mavi nokta olarak gösterir
            cv2.putText(# merkez kordinatlarını ekrana yazdırma kısmı
                frame,
                f"Hand: ({center_x}, {center_y})",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )
            cv2.putText(
                frame,
                f"Error: ({error_x}, {error_y})",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )
            cv2.putText(
                frame,
                f"Direction: ({direction_x}, {direction_y})",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )


        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()