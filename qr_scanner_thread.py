from PyQt5.QtCore import QThread, pyqtSignal
import cv2

class QRScannerThread(QThread):
    scanned = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.error.emit("Failed to open camera.")
            return
        detector = cv2.QRCodeDetector()

        while True:
            ret, frame = cap.read()
            if not ret:
                self.error.emit("Failed to capture from camera.")
                break

            value, pts, _ = detector.detectAndDecode(frame)
            if value:
                self.scanned.emit(value.strip())

            cv2.imshow("QR Code Scanner - Press 'q' to Quit", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
