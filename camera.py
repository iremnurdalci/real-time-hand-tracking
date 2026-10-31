
import cv2
import platform
from pathlib import Path

from config import (# kamera ayarlarını aldık
    FRAME_WIDTH,
    FRAME_HEIGHT,
    CAMERA_BACKEND,
    CAMERA_INDEX
)


class Camera:

    def __init__(self):

        self.camera = None
        self.backend = self._select_backend()# kamera  türünü seçiyoruz
        self.is_started = False

        if self.backend == "picamera2": # Picamera2 backendini seç

            from picamera2 import Picamera2

            self.camera = Picamera2()

            camera_config = self.camera.create_video_configuration(
                main={
                    "size": (FRAME_WIDTH, FRAME_HEIGHT),
                    "format": "BGR888"
                },
                buffer_count=4
            )

            self.camera.configure(camera_config)# ayaralrı kameraya uygular

        elif self.backend == "opencv":

            self.camera = cv2.VideoCapture(CAMERA_INDEX)

            self.camera.set(
                cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH
            )

            self.camera.set(
                cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT
            )

    def _select_backend(self):

        if CAMERA_BACKEND != "auto":
            return CAMERA_BACKEND

        # Raspberry Pi modelini kontrol et
        model_path = Path("/proc/device-tree/model")

        if model_path.exists():
            model = model_path.read_bytes().decode(
                "utf-8", errors="ignore"
            )

            if "Raspberry Pi" in model:
                return "picamera2"

        return "opencv"

    def start(self):# kamerayı başlatır

        if self.backend == "picamera2":
            self.camera.start()

        elif not self.camera.isOpened():
            raise RuntimeError("Kamera açılamadı!")

        self.is_started = True
        print(f"Kamera başlatıldı: {self.backend}")

    def read(self):# kameradan görüntü alma

        if not self.is_started:
            raise RuntimeError("Önce start() çağrılmalı!")

        if self.backend == "picamera2":

            frame = self.camera.capture_array()

            return True, frame

        return self.camera.read()

    def release(self):# kamera kapatılır

        if self.camera is not None:

            if self.backend == "picamera2":

                if self.is_started:
                    self.camera.stop()

                self.camera.close()

            else:
                self.camera.release()

            self.is_started = False
            self.camera = None
