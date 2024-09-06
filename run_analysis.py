from process import *
from summary import *
from dlc_runner import *
import concurrent.futures
from joblib import Parallel, delayed
import sys

sys.path.append("./preprocess/")
from FourChamber_split_resize import *


def main():

    # Ask the user to select subfolder to process
    root = tk.Tk()
    root.withdraw()

    # input the path to the experiment folder
    experiment_folder = select_folder()

    # split and resize the 4chamber recordings
    # FourChamber_split_resize(experiment_folder, fulres=True)

    experiment_name = os.path.basename(experiment_folder)
    parent_folder = os.path.dirname(experiment_folder)
    analysis_folder = os.path.join(parent_folder, f"{experiment_name}_analysis")

    # generate the list of recordings to be processed
    recording_list = get_recording_list([analysis_folder])

    # generate the list of trans_resize.avi videos to pass to deeplabcut
    body_videos = [
        os.path.join(recording,'trans_resize.avi') for recording in recording_list
    ]

    # run deeplabcut
    run_deeplabcut(dlc_config_path, body_videos)

    # now that done with DLC tracking, start process the recordings
    print(f"In total {len(recording_list)} videos to be processed: ")
    print(f"{[os.path.basename(recording) for recording in recording_list]}")

    # # Process the videos iteratively
    # for video in video_list:
    #     process_video(video, exp_folder, features_folder)

    # Get the number of available CPU cores
    num_workers = os.cpu_count() - 2 if os.cpu_count() > 2 else 1

    # Use joblib for parallel processing
    Parallel(n_jobs=num_workers)(
        delayed(process_recording_wrapper)(recording) for recording in recording_list
    )

    # generate summary csv from the processed videos
    #time_bins = ((0, 1), (1, 2), (2, 3), (3, -1), (0, -1))
    #0-30 bins every minute
    # time_bins = ((0,-1),(25,-1),(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23), (23, 24), (24, 25), (25, 26), (26, 27), (27, 28), (28, 29), (29, 30))
    time_bins = ((0,-1),)
    # time_bins = ((0, -1),(0,5))
    generate_summary_csv(analysis_folder, time_bins)


if __name__ == "__main__":
    import tkinter as tk

    main()
