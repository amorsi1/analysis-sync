import os
import pandas as pd
import cv2
import tkinter as tk


video_folder = '/mnt/hd0/02.07_secretoneurin/videos'
ftir_files = [os.path.join(video_folder, file) for file in os.listdir(video_folder) if file.endswith("ftir.avi")]
for file in ftir_files:
    print(file)
    cap = cv2.VideoCapture(file)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"video length is {frame_count / fps / 60} mins")
    for i in range(frame_count):
        frame = cap.read()[1]  # Read the next frame
        if frame is None:
            print(f"frame {i} is None")
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscal


    cap.release()