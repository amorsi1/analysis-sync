import os
import pandas as pd
import cv2
import tkinter as tk


def select_folder():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()

    # Ask the user to select subfolder to process

    folder = filedialog.askdirectory(
        parent=root,
        title="Select a subfolder to process",
    )

    return folder
def test_cv2(ftir_fpath):
    ftir_video = cv2.VideoCapture(
        ftir_fpath)
    fps = int(ftir_video.get(cv2.CAP_PROP_FPS))
    frame_count = int(ftir_video.get(cv2.CAP_PROP_FRAME_COUNT))
    return fps, frame_count

# Ask the user to select subfolder to process
#root = tk.Tk()
#root.withdraw()

# input the path to the experiment folder
# input the path to the experiment folder
#video_folder = select_folder()
video_folder = '/mnt/hd0/02.07_secretoneurin/videos' 


ftir_files = [os.path.join(video_folder, file) for file in os.listdir(video_folder) if file.endswith("ftir.avi")]
df = pd.DataFrame({
    "ftir": ftir_files,
    "fps": [None]*len(ftir_files),
    "frame_count": [None]*len(ftir_files)

})

for index, row in df.iterrows():
    fps, frame_count = test_cv2(row["ftir"])
    df.at[index, "fps"] = fps
    df.at[index, "frame_count"] = frame_count

print(df)
print("fps >0")
print(df[df['fps'] != 0])
print("body")
print(df[df['ftir'].str.endswith("body.avi")])
