# 움직이는 사람을 인식해 이동 경로를 따라 선을 그려줍니다.

import cv2
import numpy as np
import torch
import supervision as sv
from ultralytics import YOLO

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# 모델 경로(수정 필요)
model = YOLO("best.pt")
box_annotator = sv.BoxAnnotator(
    thickness=2,
    text_thickness=2,
    text_scale=1
)

# 영상 경로(수정 필요)
cap = cv2.VideoCapture("/Users/hui-ryung/Desktop/CameraRoll/group/friend_group_1.mp4")

# 좌표 리스트 초기화
points = []

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break
    results = model.predict(img)[0]
    try:
        for box in results.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box.tolist())
            # 박스 그리기
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # 박스의 정 가운데에 점 찍기
            center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img, (center_x, center_y), 10, (0, 0, 255), -1)

            # 현재 좌표를 리스트에 추가
            points.append((center_x, center_y))

            # 이전 점과 현재 점을 연결하는 선 그리기
            for i in range(1, len(points)):
                cv2.line(img, points[i - 1], points[i], (255, 0, 0), 1)
    except:
        center_x, center_y = -1, -1

    frame = box_annotator.annotate(scene=img, detections=sv.Detections.from_yolov8(results))
    cv2.imshow("YoLO Test", frame)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()