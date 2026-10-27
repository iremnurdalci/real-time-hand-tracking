import cv2
import time

from hand_detector import HandDetector


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

        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
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