import cv2 

video_file = "Squat - Trim.mp4"  #video to track 

#various openCV tracking packages 
trackers = { 
            "csrt": cv2.legacy.TrackerCSRT_create,
            "mosse":cv2.legacy.TrackerMOSSE_create,
            "kcf":cv2.legacy.TrackerKCF_create,
            "medianflow":cv2.legacy.TrackerMedianFlow_create,
            "mil":cv2.legacy.TrackerMIL_create,
            "tld":cv2.legacy.TrackerTLD_create,
            "boosting":cv2.legacy.TrackerBoosting_create
            }

#selection of tracker 
tracker_key = "csrt"
roi = None
tracker = trackers[tracker_key]()

# selecting video 
cap = cv2.VideoCapture(video_file)

# read the first frame
ret, frame = cap.read()
if not ret:
    print("Failed to open video file")
    exit()
    
# select region of interest 
roi = cv2.selectROI("Tracking", frame)
tracker.init(frame, roi)

centroid_path = [] # list to store centroid's coordinates 

while True:   
    frame = cap.read()[1]   # open and read video 
    if frame is None:       # break if video cannot be read 
        break
    
    if roi is not None:        
        success,box = tracker.update(frame)    # selectng region of interest 

        if success:
            x,y,w,h = [int(c) for c in box]   # coordinates of bounding box 
        
            # calculate centroid of bounding box 
            cx = x + w // 2
            cy = y + h // 2
            
            centroid_path.append((cx,cy))  # append centroid coordinates to list above 
                        
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)  # draw bounding box 
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)  # draw centroid in bounding box 
            
            # drawing centroid path 
            for i in range(1,len(centroid_path)):
                cv2.line(frame,centroid_path[i-1],centroid_path[i],(0,255,0),2)
            
        else:   # if tracking failed at a frame, select tracking again  
            print ("Tracking has failed")   
            roi = None
            tracker = trackers[tracker_key]() 
        
    cv2.imshow("Tracking",frame)
    k = cv2.waitKey(60)
    

    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()

