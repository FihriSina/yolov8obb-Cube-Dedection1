from ultralytics import YOLO
import cv2
import math
import numpy as np

# Modeli yükle
model = YOLO("runs/obb/train2/weights/best.pt")

# Kamera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera acilamadi.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kare alinamadi.")
        break

    # Tahmin
    results = model.predict(source=frame, imgsz=640, conf=0.4, verbose=False)
    annotated_frame = results[0].plot()

    # OBB sonuçları varsa işle
    if results[0].obb is not None and len(results[0].obb.xyxyxyxy) > 0:
        obb_xy = results[0].obb.xyxyxyxy.cpu().numpy()
        confs = results[0].obb.conf.cpu().numpy()
        classes = results[0].obb.cls.cpu().numpy()

        for i, pts in enumerate(obb_xy):
            # pts shape: (4,2)
            pts = np.array(pts, dtype=np.float32)

            # merkez
            cx = int(np.mean(pts[:, 0]))
            cy = int(np.mean(pts[:, 1]))

            # açı: ilk kenardan hesap
            dx = pts[1][0] - pts[0][0]
            dy = pts[1][1] - pts[0][1]
            angle = math.degrees(math.atan2(dy, dx))

            # genişlik, yükseklik
            width = np.linalg.norm(pts[1] - pts[0])
            height = np.linalg.norm(pts[2] - pts[1])
            area = int(width * height)

            conf = float(confs[i])

            # merkez noktası çiz
            cv2.circle(annotated_frame, (cx, cy), 5, (0, 255, 0), -1)

            # bilgi metni
            info1 = f"cx:{cx} cy:{cy}"
            info2 = f"angle:{angle:.1f}"
            info3 = f"conf:{conf:.2f} area:{area}"

            # yazıları merkezin yanına koy
            cv2.putText(annotated_frame, info1, (cx + 10, cy - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(annotated_frame, info2, (cx + 10, cy + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(annotated_frame, info3, (cx + 10, cy + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    # ekranın tam ortasına da dikey çizgi koyalım
    h, w = annotated_frame.shape[:2]
    cv2.line(annotated_frame, (w // 2, 0), (w // 2, h), (255, 0, 0), 2)

    cv2.imshow("YOLOv8-OBB Live Test", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()