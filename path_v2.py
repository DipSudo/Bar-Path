import cv2
import matplotlib.pyplot as plt

def drawRectangle(frame, bbox):
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

def displayRectangle(frame, bbox): 
    plt.figure(figsize=(20, 10))
    if frame is not None:
        frameCopy = frame.copy()
        drawRectangle(frameCopy, bbox)
        frameCopy = cv2.cvtColor(frameCopy, cv2.COLOR_BGR2RGB)
        plt.imshow(frameCopy)
        plt.axis("off")
        plt.show()

def drawText(frame, txt, location, color=(50, 170, 50)):
    cv2.putText(frame, txt, location, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

tracker = cv2.TrackerKCF_create()

video_input_file_name = "Squat - Trim.mp4"
video = cv2.VideoCapture(video_input_file_name)

if not video.isOpened():
    print("Error: Unable to open video file.")

ok, frame = video.read()
bbox = (1300, 405, 160, 120)

displayRectangle(frame, bbox)

ok = tracker.init(frame, bbox)

while True: 
    ok, frame = video.read()
    if not ok:
        break
    
    timer = cv2.getTickCount()
    
    ok, bbox = tracker.update(frame)
    
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    
    if ok: 
        drawRectangle(frame, bbox)
    else:
        drawText(frame, "Tracking Failed", (80, 140), (0, 0, 255))
        
    drawText(frame, "FPS: " + str(int(fps)), (80, 100))
    
    cv2.imshow("Tracking", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("27"):
        break

video.release()
cv2.destroyAllWindows()
