import cv2
import time

from hand_detector import HandDetector
from tracker import Tracker #hız ve yön hesaplamalarını bu sınıftan alıyoruz


def main():

    # Sınıfları oluştur
    detector = HandDetector()
    tracker = Tracker()

    # Kamerayı başlat
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

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

        # Görüntüyü yatay olarak çevir
        frame = cv2.flip(frame, 1)

        # Eli algıla
        hand = detector.detect(frame)

        if hand is not None:

            height, width, _ = frame.shape

            # Elin merkez koordinatlarını bul
            center = detector.get_hand_center(
                hand, width, height
            )

            # Takip verilerini hesapla
            tracking_data = tracker.update(
                center, width, height
            )

            center_x, center_y = tracking_data["center"]
            camera_center_x, camera_center_y = tracking_data["camera_center"]

            error_x, error_y = tracking_data["error"]
            direction_x, direction_y = tracking_data["direction"]
            speed_x, speed_y = tracking_data["speed"]

            # El merkezini kırmızı noktayla göster
            cv2.circle(
                frame, (center_x, center_y),
                10, (0, 0, 255), -1
            )

            # Kamera merkezini mavi noktayla göster
            cv2.circle(
                frame, (camera_center_x, camera_center_y),
                8, (255, 0, 0), -1
            )

            # El koordinatları
            cv2.putText(
                frame,
                f"Hand: ({center_x}, {center_y})",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 255, 0), 2
            )

            # Hata değerleri
            cv2.putText(
                frame,
                f"Error: ({error_x}, {error_y})",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 255, 255), 2
            )

            # Yön bilgisi
            cv2.putText(
                frame,
                f"Direction: ({direction_x}, {direction_y})",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 0), 2
            )

            # Hız bilgisi
            cv2.putText(
                frame,
                f"Speed: ({speed_x}, {speed_y})",
                (20, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2
            )

        else:
            # El algılanmazsa takip hızlarını sıfırla
            tracker.reset()

        # FPS hesaplama
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8, (0, 255, 0), 2
        )

        # Görüntüyü göster
        cv2.imshow("Hand Tracking", frame)

        # Q tuşuyla çık
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
