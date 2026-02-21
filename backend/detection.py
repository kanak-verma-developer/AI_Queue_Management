import os
import cv2
import torch
from ultralytics import YOLO

# -------------------------------
# Load YOLO Model Safely
# -------------------------------

# Fix: Line was too long (E501). Broken into two steps.
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, "..", "models", "yolov8n.pt")

# Force CPU if GPU not available
device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    model = YOLO(model_path)
    model.to(device)
except Exception as e:
    print("Error loading YOLO model:", e)
    model = None


# -------------------------------
# Detection Function
# -------------------------------

# Fix: Added 2 blank lines above (E302)
def detect_people(frame):
    """
    Detect people in an image or video frame.
    Returns: processed_frame, people_count
    """
    if frame is None or model is None:
        return frame, 0

    people_count = 0

    try:
        # Run prediction
        results = model.predict(
            frame, conf=0.4, device=device, verbose=False
        )

        for result in results:
            if result.boxes is None:
                continue

            boxes = result.boxes.xyxy.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy()

            for i, cls in enumerate(classes):
                if int(cls) == 0:  # Class 0 = Person
                    people_count += 1
                    x1, y1, x2, y2 = boxes[i].astype(int)

                    # Draw bounding box
                    cv2.rectangle(
                        frame, (x1, y1), (x2, y2), (0, 255, 0), 2
                    )

                    cv2.putText(
                        frame, "Person", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
                    )

        return frame, people_count

    except Exception as e:
        print("Detection error:", e)
        return frame, 0


# -------------------------------
# Optional Camera Test
# -------------------------------

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not found!")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame, count = detect_people(frame)
        cv2.putText(
            processed_frame, f"People Detected: {count}",
            (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
        )

        cv2.imshow("Live Detection", processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()