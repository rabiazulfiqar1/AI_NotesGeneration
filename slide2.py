import cv2
import os

video_path = "video3.mp4"
output_dir = "slides2"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
prev = None
frame_id = 0
saved = 0

# ROI: right side of board (adjust if needed)
x, y, w, h = 460, 80, 400, 400  

# Cooldown: only save once every N seconds
fps = cap.get(cv2.CAP_PROP_FPS)
cooldown_frames = int(fps * 3)  # 3 sec cooldown
last_saved_frame = -cooldown_frames

last_saved_crop = None  # store last board snapshot

while True:
    ret, frame = cap.read()
    if not ret:
        break

    board = frame[y:y+h, x:x+w]
    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)

    if prev is not None:
        diff = cv2.absdiff(gray, prev)
        score = diff.sum() / 255

        if frame_id % 30 == 0:
            print(f"Frame {frame_id}, Score={score}")

        # Save only if threshold is exceeded & cooldown passed
        if score > 3000 and (frame_id - last_saved_frame) > cooldown_frames:

            # Similarity check with last saved crop
            if last_saved_crop is not None:
                check_diff = cv2.absdiff(gray, last_saved_crop)
                check_score = check_diff.mean()
                if check_score < 5:  # almost identical
                    prev = gray
                    frame_id += 1
                    continue

            fname = os.path.join(output_dir, f"frame_{frame_id}.jpg")
            cv2.imwrite(fname, frame)
            saved += 1
            last_saved_frame = frame_id
            last_saved_crop = gray.copy()

    prev = gray
    frame_id += 1

cap.release()
print(f"Frames saved: {saved}")
