import cv2
import numpy as np
from ultralytics import YOLO
from tracker import *
from twilio_notifier import TwilioNotifier

model = YOLO("yolo11n.pt")
model.fuse()
class_list = model.names

area1 = [(312, 388), (289, 390), (474, 469), (497, 462)]  
area2 = [(279, 392), (250, 397), (423, 477), (454, 469)]  

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        print([x, y])

cv2.namedWindow("Shop Counter")
cv2.setMouseCallback("Shop Counter", RGB)
cap = cv2.VideoCapture("outside_shop.mp4",cv2.CAP_FFMPEG)

count = 0
tracker = Tracker()
people_entering = {}
people_exiting = {}
entering = set()
exiting = set()

# Initialize Twilio notifier
notifier = TwilioNotifier()

print("🚀 People Counter with WhatsApp Notifications Started!")
print("Press 'ESC' to exit")
print("Press 'R' to reset notification tracking")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    count += 1
    
    frame = cv2.resize(frame, (1020, 500))

    results = model.predict(frame,verbose=False)
    boxes = results[0].boxes

    if boxes is not None and boxes.xyxy is not None:
        px = boxes.xyxy.cpu().numpy()
        classes = boxes.cls.cpu().numpy().astype(int)
        list = []

        # Collect persons
        for i, row in enumerate(px):
            x1, y1, x2, y2 = map(int, row)
            d = classes[i]
            c = class_list[d]
            if 'person' in c:
                list.append([x1, y1, x2, y2])

        bbox_ids = tracker.update(list)

        for bbox in bbox_ids:
            x3, y3, x4, y4, id = bbox
            res = cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False)
            if res >= 0:
                people_entering[id] = (x4, y4)
                cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)

            if id in people_entering:
                res_1 = cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False)
                if res_1 >= 0:
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
                    cv2.circle(frame, (x4, y4), 5, (255, 0, 255), -1)
                    cv2.putText(frame, str(id), (x3, y3), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 1)
                    
                    # Check if this is a new person entering
                    if id not in entering:
                        entering.add(id)
                        # Send WhatsApp notification
                        notifier.send_whatsapp_notification(id)
            
        ## People Exiting Code ###
            res2 = cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False)
            if res2 >= 0:
                people_exiting[id] = (x4, y4)
                cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)

            if id in people_exiting:
                res_3 = cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False)
                if res_3 >= 0:
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (255, 0, 255), 2)
                    cv2.circle(frame, (x4, y4), 5, (255, 0, 255), -1)
                    cv2.putText(frame, str(id), (x3, y3), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 1)
                    exiting.add(id)

    # Draw Polylines area near door
    cv2.polylines(frame, [np.array(area1, np.int32)], True, (255, 0, 0), 2)
    cv2.putText(frame, "1", (area1[0][0], area1[0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    cv2.polylines(frame, [np.array(area2, np.int32)], True, (255, 255, 0), 2)
    cv2.putText(frame, "2", (area2[0][0], area2[0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    print("People entered:", entering)
    print("People Exiting:", exiting)
    cv2.putText(frame, f"Entered: {len(entering)}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Exited: {len(exiting)}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Add notification status
    if notifier.client:
        cv2.putText(frame, "WhatsApp: ON", (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "WhatsApp: OFF", (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("People Counter", frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == 27:  # ESC key
        break
    elif key == ord('r') or key == ord('R'):  # R key to reset notifications
        notifier.reset_notifications()
        print("Notification tracking reset!")

cap.release()
cv2.destroyAllWindows()
