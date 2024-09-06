import os
from summary_viz import *
import pandas as pd

# user input: load the summary.csv file
experiment_folder = "/mnt/hd0/gui_outputs/05.25_0min_recordings/6.06_trimmed"
test_df = os.path.join(experiment_folder, "MERGED_summary.csv")
test_df = pd.read_csv(test_df)

# --------------------------------
# user input for selecting columns to be included in the plot

# (a list of columns) -> user input for selecting columns to be included in the plot, default would be all numerical
# (features) columns except for the recording_time
selected_columns = [
    "distance_traveled (pixel)",
    "both_front_paws_lifted (ratio of time)",
    "average_hind_left_luminance",
    "average_hind_paw_luminance_ratio (r/l)",
    "average_standing_hind_paw_luminance_ratio (l/r)",
    "hind_left_paw_lifted_time (seconds)",


]

# (a boolean vector mask) -> user input for selecting rows (a subset of the recordings) to be included in the plot,
# default would be all recordings selected_rows = [True, True, True, True, True, True, True, True, True, True] user
# can select a subset of the recordings based on the values in the grouping variables (e.g., pain_model, treatment)
selected_rows = test_df["Timepoint"] == "0"
# user can manually select each row to be included in the plot via the user interface
# selected_rows = [True, False, True, False, True, False, True, False, True, False]

# (a string for the variable name) -> user input for selecting the grouping variable
group_variable = "PV: virus" #put in full column name

# (a True/False boolean value) -> user input for whether ranking the columns by statistical significance between groups
sort_by_significance = False

# --------------------------------

# preprocess the summary csv file for visualization with user inputs
df_plot = summary_viz_preprocess(
    df=test_df,
    rows_to_include=selected_rows,
    columns_to_include=selected_columns,
    group_variable=group_variable,
)


# generate the PairGrid plot
# generate_PairGrid_plot(
#     df=df_plot, group_variable=group_variable, diag_kind='reg',upper_kind='kde',lower_kind='kde', dest_path=os.path.join(experiment_folder,'pairplot.png'),sort_by_significance=sort_by_significance
# )

# generate the bar plots
generate_bar_plots(
    df=df_plot, group_variable=group_variable, dest_path=os.path.join(experiment_folder,'barplot.png'),sort_by_significance=sort_by_significance
)


# generate joint plot for a pair of columns
# user input for selecting a pair of columns to be included in the joint plot
g = sns.jointplot(
    data=df_plot,
    x="distance_traveled (pixel)",
    y="standing_on_two_hind_paws (ratio of time)",
    hue=group_variable,
)
