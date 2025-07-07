import matplotlib.pyplot as plt
import pandas as pd

def plot_offset_chart(parsed_data):
    df = pd.DataFrame(parsed_data)
    fig, ax = plt.subplots()
    if "offset" in df:
        df = df.dropna(subset=["offset"])
        ax.plot(df["timestamp"], df["offset"].astype(float))
        ax.set_xlabel("Time")
        ax.set_ylabel("Offset (ns)")
        ax.set_title("PTP Offset Over Time")
    else:
        ax.text(0.5, 0.5, "No offset data", ha='center')
    return fig

def plot_state_changes(parsed_data):
    df = pd.DataFrame(parsed_data)
    fig, ax = plt.subplots()
    if "state" in df:
        df = df.dropna(subset=["state"])
        codes = {s: i for i, s in enumerate(df["state"].unique())}
        df['code'] = df['state'].map(codes)
        ax.step(df["timestamp"], df['code'], where='post')
        ax.set_yticks(list(codes.values()))
        ax.set_yticklabels(list(codes.keys()))
        ax.set_xlabel("Time")
        ax.set_title("PTP Clock State Changes Over Time")
    else:
        ax.text(0.5, 0.5, "No state data", ha='center')
    return fig
