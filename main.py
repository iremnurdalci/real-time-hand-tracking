
import cv2
import time

from camera import Camera
from hand_detector import HandDetector
from tracker import Tracker


def main():

    # Sınıfları oluştur
    camera = Camera()
    detector = HandDetector()
    tracker = Tracker()

    try:

        # Kamerayı başlat
        camera.start()

        print("El takip sistemi başladı.")
        print("Çıkmak için Q tuşuna bas.")

        previous_time = time.time()

        while True:

            # Kameradan görüntü al
            success, frame = camera.read()

            if not success:
                print("Görüntü alınamadı!")
                break

            # Görüntüyü yatay çevir
            frame = cv2.flip(frame, 1)

            # El algılama
            hand = detector.detect(frame)

            if hand is not None:

                height, width, _ = frame.shape

                # El merkezini bul
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

                # El merkezini göster
                cv2.circle(
                    frame,
                    (center_x, center_y),
                    10,
                    (0, 0, 255),
                    -1
                )

                # Kamera merkezini göster
                cv2.circle(
                    frame,
                    (camera_center_x, camera_center_y),
                    8,
                    (255, 0, 0),
                    -1
                )

                # El koordinatları
                cv2.putText(
                    frame,
                    f"Hand: ({center_x}, {center_y})",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                # Hata değerleri
                cv2.putText(
                    frame,
                    f"Error: ({error_x}, {error_y})",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2
                )

                # Yön bilgisi
                cv2.putText(
                    frame,
                    f"Direction: ({direction_x}, {direction_y})",
                    (20, 160),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 0),
                    2
                )

                # Hız bilgisi
                cv2.putText(
                    frame,
                    f"Speed: ({speed_x}, {speed_y})",
                    (20, 200),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

            else:
                # El kaybolursa takip hızlarını sıfırla
                tracker.reset()

            # FPS hesaplama
            current_time = time.time()
            elapsed_time = current_time - previous_time

            fps = 1 / elapsed_time if elapsed_time > 0 else 0
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

            # Görüntüyü göster
            cv2.imshow("Hand Tracking", frame)

            # Q tuşuyla çık
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        # Kaynakları güvenli şekilde kapat
        camera.release()
        detector.close()
        cv2.destroyAllWindows()

        print("El takip sistemi kapatıldı.")


if __name__ == "__main__":
    main()

