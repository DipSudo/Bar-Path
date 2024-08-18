import cv2



def initialize_tracker(tracker_key):
    
    """
     Function to initialize the tracker with choosen tracker key (Currently using csrt as it works best )
    
    """
            
    trackers = { 
        "csrt": cv2.legacy.TrackerCSRT_create,
        "mosse": cv2.legacy.TrackerMOSSE_create,
        "kcf": cv2.legacy.TrackerKCF_create,
        "medianflow": cv2.legacy.TrackerMedianFlow_create,
        "mil": cv2.legacy.TrackerMIL_create,
        "tld": cv2.legacy.TrackerTLD_create,
        "boosting": cv2.legacy.TrackerBoosting_create
    }
    return trackers[tracker_key]()

def select_roi_tracker(cap, tracker):
    
    """
    Function to select the region of interest (ROI) in video and initialize the tracker 
    
    """
    
    ret, frame = cap.read()     # read the first frame
    if not ret:                 # error catching if video doesnt open 
        print("Failed to open video file")
        return None, None

    roi = cv2.selectROI("Tracking", frame)    # select region of interest 
    tracker.init(frame, roi)
    
    return roi, frame

def video_speed(video_file):
    # Open the video file
    cap = cv2.VideoCapture(video_file)
    
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Get the frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Calculate the delay in milliseconds
    # delay = int(1000 / fps)
    delay = int(2)   # works for some reason....???
    return delay 

def video_title(frame, title):
    """
    Function to overlay a title on the video frame.
    
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 255, 255)  # White color for text
    font_thickness = 2
    
    # Calculate text size to center it
    text_size = cv2.getTextSize(title, font, font_scale, font_thickness)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = (text_size[1] + 30)  # 30 pixels from the top of the frame
    
    # Overlay text
    cv2.putText(frame, title, (text_x, text_y), font, font_scale, font_color, font_thickness)
    return frame

def initialize_video_writer(video_file, output_file):
    
    """
    Function to get properties for output file 
    
    """
    
    cap = cv2.VideoCapture(video_file)
    
    if not cap.isOpened():
        raise Exception("Error opening video file")

    # Get the frame width, height, and frames per second (fps) of the video
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Define codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))
    
    return cap, out



def process_video(video_file, tracker_key, output_file,title):
    
    """
    Function to process the video
    
    """
    cap, out = initialize_video_writer(video_file, output_file)
    tracker = initialize_tracker(tracker_key)
    roi, frame = select_roi_tracker(cap, tracker)


    #relevent metrics 
    centroid_path = []      # list to store centroid's coordinates 
    rel_centroid_path = []  # list to store centroid's coordinates relative to the origin 
    time = []              # list to store time stamps

    origin = None

    while True:   
        frame = cap.read()[1]   # open and read video 
        if frame is None:       # break if video cannot be read 
            break

        if roi is not None:        
            success, box = tracker.update(frame)    # selecting region of interest 

            if success:
                x, y, w, h = [int(c) for c in box]   # coordinates of bounding box 

                # calculate centroid of bounding box 
                cx = x + w // 2
                cy = y + h // 2

                if origin is None:  # setting the initial centroid position as the origin 
                    origin = (cx, cy)

                # Calculate the position relative to the origin
                rel_cx = cx - origin[0]
                rel_cy = cy - origin[1]   

                # Get the current time in milliseconds and convert to seconds
                time_msec = cap.get(cv2.CAP_PROP_POS_MSEC)
                time_sec = time_msec / 1000.0

                # Store centroid coordinates and time
                centroid_path.append((cx, cy))
                rel_centroid_path.append((rel_cx, rel_cy))
                time.append(time_sec)

                # Add centroid coordinates as text on the video
                text = f"({rel_cx}, {rel_cy})"
                cv2.putText(frame, text, (cx - 100, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Draw bounding box and centroid
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

                # Draw centroid path 
                for i in range(1, len(centroid_path)):
                    cv2.line(frame, centroid_path[i - 1], centroid_path[i], (0, 255, 0), 2)

            else:  # if tracking failed at a frame, select tracking again  
                print("Tracking has failed")
                roi = None
                tracker = initialize_tracker(tracker_key)
                
         # Add title to the frame
        frame = video_title(frame, title)
          

        cv2.imshow("Tracking", frame)
        # k = cv2.waitKey(30)
        delay = video_speed(video_file)
        k = cv2.waitKey(delay) & 0xFF  

        if k == 27:  # Exit on ESC key (ASCII value for ESC is 27)
            break
        
       # Write the frame to the output video file
        out.write(frame)
        
    cap.release()
    cv2.destroyAllWindows()
    
    return rel_centroid_path, time 
