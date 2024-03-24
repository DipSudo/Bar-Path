import cv2

# Function to initialize the video capture and tracker
def initialize_tracker(video_file):
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return None, None, None

    fps = cap.get(cv2.CAP_PROP_FPS)
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read video frame.")
        return None, None, None

    bbox = cv2.selectROI("Tracking", frame, False)
    tracker = cv2.TrackerKCF_create()
    tracker.init(frame, bbox)

    return cap, fps, tracker

# Main function to track object in the video
def track_object(video_file):
    cap, fps, tracker = initialize_tracker(video_file)
    if cap is None or fps is None or tracker is None:
        return

    frame_interval = int(1000 / fps)  # Interval between frames in milliseconds

    while cap.isOpened():  # Continue loop until the video ends
        ret, frame = cap.read()
        if not ret:
            break


        ret, bbox = tracker.update(frame)
        if ret:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2)
            cv2.putText(frame, "Tracking", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Lost", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
 
        cv2.imshow("Tracking", frame) 

        # Adjust waitKey based on video frame rate
        if cv2.waitKey(frame_interval) & 0xFF == 27:  # Exit on 'Esc' key
            break


    cap.release()
    cv2.destroyAllWindows()


  

if __name__ == "__main__":
    video_file = "Squat - Trim.mp4"
    # video_file = "Squat.mp4"
    track_object(video_file)
