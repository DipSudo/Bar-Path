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

    roi = cv2.selectROI("Tracking", frame, False)
    x, y, w, h = roi
    initial_point = (x + w // 2, y + h // 2)

    tracker = cv2.TrackerKCF_create()
    tracker.init(frame, roi)

    return cap, fps, tracker, initial_point

# Main function to track object in the video
def track_object(video_file):
    cap, fps, tracker, initial_point = initialize_tracker(video_file)
    if cap is None or fps is None or tracker is None:
        return

    frame_interval = int(1000 / fps)  # Interval between frames in milliseconds

    while cap.isOpened():  # Continue loop until the video ends
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read video frame.")
            break

        # Update tracker with the new frame
        ret, roi = tracker.update(frame)

        if ret:
            # Calculate the current point coordinates (centroid)
            x, y, w, h = roi
            current_point = (int(x + w // 2), int(y + h // 2))

            # Draw the point on the frame
            cv2.circle(frame, current_point, 5, (0, 255, 0), -1)
            cv2.putText(frame, "Tracking", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Lost", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display result
        cv2.imshow("Tracking", frame)

        # Adjust waitKey based on video frame rate
        if cv2.waitKey(frame_interval) & 0xFF == 27:  # Exit on 'Esc' key
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_file = "Squat - Trim.mp4"
    track_object(video_file)
