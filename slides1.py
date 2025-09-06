import cv2
import os

url = "https://www.youtube.com/watch?v=9SOSfRNCQZQ"
video_path = "PCA.mp4"

# ydl_opts = {
#     "outtmpl": video_path,
#     "format": "bestvideo+bestaudio/best",  # highest quality mp4
#     "merge_output_format": "mp4"
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     ydl.download([url])

# print(f"Video downloaded as {video_path}")

output_dir = "PCACV"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
prev = None
frame_id = 0
saved = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev is not None:
        diff = cv2.absdiff(gray, prev)
        score = diff.sum() / 255  # how much the frame changed

        # print score every 30 frames
        if frame_id % 30 == 0:
            print(f"Frame {frame_id}, Score={score}")

        if score > 2200:  # start with smaller threshold
            fname = os.path.join(output_dir, f"frame_{frame_id}.jpg")
            cv2.imwrite(fname, frame)
            saved += 1

    prev = gray
    frame_id += 1

cap.release()
print(f"Frames saved: {saved}")
