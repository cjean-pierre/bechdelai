import pandas as pd
import plotly.express as px


def fn_create_sequence_id(x):
    return (1 - (x == x.shift(1))).cumsum() - 1


def fn_timeline(x):

    try:
        x = x.tolist()
    except:
        pass
    
    seq_id = 0
    seq_ids = []
    
    for i in range(len(x) - 1):
        seq_ids.append(seq_id)
        if (x[i+1] - x[i]) > 1:
            seq_id += 1
            
    # Add last element
    seq_ids.append(seq_id)
    return seq_ids




def convert_to_timeline(df,description_col,frame_col = "frame_id",sequence_col = "sequence_id",time_between_frames = 1,show = True,xaxis_time = True):

    timeline = df.copy().sort_values(frame_col)

    timeline = timeline.groupby([description_col,sequence_col]).agg({frame_col:["min","max"]})[frame_col].reset_index()
    timeline["max"] += 1

    if xaxis_time:
        timeline["start"] = timeline["min"].map(lambda x : pd.Timedelta(seconds = x * time_between_frames))
        timeline["end"] = timeline["max"].map(lambda x : pd.Timedelta(seconds = x * time_between_frames))
        timeline["duration"] = timeline["end"] - timeline["start"]
        start_date = pd.to_datetime("2022-01-01")
        timeline["start"] = start_date + timeline["start"]
        timeline["end"] = start_date + timeline["end"]
    else:
        timeline["start"] = timeline["min"]
        timeline["end"] = timeline["max"]
        timeline["duration"] = timeline["end"] - timeline["start"]

    if show:
        fig = px.timeline(timeline,x_start = "start",x_end = "end",color = description_col,y = description_col,color_discrete_sequence = px.colors.qualitative.Alphabet)
        return fig
    else:
        return timeline