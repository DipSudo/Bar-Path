from tracker import *
from plots import *


def main():
    # video_file = "Squat - Trim.mp4"
    video_file = "Squat 2.MP4"
    tracker_key = "csrt"
    output_file = "output_video.mp4"         #Output file name 
    video_title = ("Weight:160kg, Rep:1, RPE:9")
    process_video(video_file, tracker_key,output_file,video_title)
    plot_centroid_path(rel_centroid_path, time)

if __name__ == "__main__":
    main()
