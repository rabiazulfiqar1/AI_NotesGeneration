import cv2
import os

video_path = "video3.mp4"
output_dir = "slides_clean"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
prev = None
frame_id = 0
saved = 0

# Crop only the board (right side of the dividing line)
# Adjust x,y,w,h for your case. Example: line starts at x=450.
x, y, w, h = 900, 80, 900, 1000   # shift x → 600 instead of 450

fps = cap.get(cv2.CAP_PROP_FPS)
cooldown_frames = int(fps * 3)
last_saved_frame = -cooldown_frames

last_saved_crop = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    board = frame[y:y+h, x:x+w]  # take only the board region
    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)

    if prev is not None:
        diff = cv2.absdiff(gray, prev)
        score = diff.sum() / 255

        if frame_id % 30 == 0:
            print(f"Frame {frame_id}, Score={score}")

        if score > 15000 and (frame_id - last_saved_frame) > cooldown_frames:
            if last_saved_crop is not None:
                check_diff = cv2.absdiff(gray, last_saved_crop)
                check_score = check_diff.mean()
                if check_score < 5:
                    prev = gray
                    frame_id += 1
                    continue

            fname = os.path.join(output_dir, f"slide_{frame_id}.jpg")
            cv2.imwrite(fname, board)  # save ONLY the board region
            saved += 1
            last_saved_frame = frame_id
            last_saved_crop = gray.copy()

    prev = gray
    frame_id += 1

cap.release()
print(f"Slides saved: {saved}")
