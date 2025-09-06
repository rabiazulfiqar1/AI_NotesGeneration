import cv2
import os
import yt_dlp

url = "https://www.youtube.com/watch?v=ntBWrcbAhaY"
video_path = "video3.mp4"

# ydl_opts = {
#     "outtmpl": video_path,
#     "format": "bestvideo+bestaudio/best",  # highest quality mp4
#     "merge_output_format": "mp4"
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     ydl.download([url])

# print(f"Video downloaded as {video_path}")

output_dir = "slides2"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
prev = None
frame_id = 0
saved = 0

# Define ROI (region of interest) for the board
# Adjust these values by printing frame.shape and trial-and-error
# x, y, w, h = 200, 100, 800, 400  # example crop rectangle
x, y, w, h = 460, 80, 400, 400  # x,y,w,h

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # crop to board region only
    board = frame[y:y+h, x:x+w]
    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)

    if prev is not None:
        diff = cv2.absdiff(gray, prev)
        score = diff.sum() / 255  # how much the board changed

        if frame_id % 30 == 0:  # print every second (30fps assumed)
            print(f"Frame {frame_id}, Score={score}")

        # threshold tuned for board (smaller than full frame)
        if score > 2000:  
            fname = os.path.join(output_dir, f"frame_{frame_id}.jpg")
            cv2.imwrite(fname, frame)  # save full frame, not cropped
            saved += 1

    prev = gray
    frame_id += 1

cap.release()
print(f"Frames saved: {saved}")