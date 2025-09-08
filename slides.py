import yt_dlp
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images

# # STEP 1: Download YouTube video as MP4
# url = "https://www.youtube.com/watch?v=WEyYaIWIUp0"
# url = "https://www.youtube.com/watch?v=tutujWOdWwg"
# url = "https://www.youtube.com/watch?v=9SOSfRNCQZQ"
# url = "https://www.youtube.com/watch?v=FnENJbHKE54"
# url = "https://www.youtube.com/watch?v=8NQzcpWvq4g"
url = "https://www.youtube.com/watch?v=oG8DKnNIZHY"
video_filename = "tehreem.mp4"
# video_filename = "video3.mp4"   # local file name
# video_filename = "coursera.mp4"

ydl_opts = {
    "outtmpl": video_filename,
    "format": "bestvideo+bestaudio/best",  # highest quality mp4
    "merge_output_format": "mp4"
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print(f"Video downloaded as {video_filename}")

# STEP 2: Run PySceneDetect to extract slides
# output_dir = "slides2"
output_dir = "tehreem"

video_manager = VideoManager([video_filename])
scene_manager = SceneManager()
scene_manager.add_detector(ContentDetector(threshold=1.0))  # adjust threshold if needed

video_manager.set_downscale_factor(1)  # speeds up detection
video_manager.start()

# Detect slide/scene changes
scene_manager.detect_scenes(video_manager, frame_skip=1)
scene_list = scene_manager.get_scene_list()

print("Slides detected:", len(scene_list))

# Save one representative frame per scene (actual slide images)
save_images(
    scene_list,
    video_manager,
    num_images=1,                # one frame per slide
    image_name_template="$SCENE_NUMBER",
    output_dir=output_dir
)

print(f"Slides saved in folder: {output_dir}")

for i, scene in enumerate(scene_list):
    start, end = scene
    print(f"Slide {i+1}: Start {start.get_seconds()}s - End {end.get_seconds()}s")