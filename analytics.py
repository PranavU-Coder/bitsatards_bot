import pandas as pd
import seaborn as sns

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.font_manager as fm

import os
import glob
import io

import concurrent.futures
from functools import lru_cache

# seaborn typesettings for more visually-pleasing plots
sns.set_style("whitegrid")
sns.set_context("notebook", font_scale=1.1)


def load_custom_font(font_dir="fonts", font_name="JetBrainsMono-Regular.ttf"):
    font_path = os.path.join(font_dir, font_name)
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        prop = fm.FontProperties(fname=font_path)
        return prop.get_name()
    return None


custom_font = load_custom_font()
if custom_font:
    plt.rcParams["font.family"] = custom_font


# loading so many csv files at once can cause slow startups so parallelizing loadups
def load_data_parallel(path_pattern):
    files = glob.glob(path_pattern)
    if not files:
        print(f"warning: no files found matching {path_pattern}")
        return pd.DataFrame(columns=["campus", "branch", "marks", "year"])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(pd.read_csv, files))

    return pd.concat(results, ignore_index=True)


# branch-aliasing for better ux
def load_branch_mappings(filepath="branch_names.txt"):
    alias_to_actual = {}
    actual_to_alias = {}
    if not os.path.exists(filepath):
        return {}, {}
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if ":" in line:
                full_name, alias = line.split(":", 1)
                full_name = full_name.strip()
                alias = alias.strip()
                alias_to_actual[alias.lower()] = full_name
                actual_to_alias[full_name.lower()] = alias
    return alias_to_actual, actual_to_alias


def normalize_branch_name(user_input, alias_to_full):
    user_input = user_input.strip().lower()
    if user_input in alias_to_full:
        return alias_to_full[user_input]
    for alias, full_name in alias_to_full.items():
        if full_name.lower() == user_input:
            return full_name
    return None


data_path = os.path.join("data", "analysis_data", "*.csv")
df = load_data_parallel(data_path)

alias_to_actual, actual_to_alias = load_branch_mappings("branch_names.txt")

PREDICTIONS = {}
_pred_files = {
    "worst": "predict/worst_case.csv",
    "most-likely": "predict/most_likely_case.csv",
    "best": "predict/best_case.csv",
}
for key, filepath in _pred_files.items():
    if os.path.exists(filepath):
        try:
            p_df = pd.read_csv(filepath)
            if "campus" in p_df.columns:
                p_df["campus"] = p_df["campus"].str.title()
            PREDICTIONS[key] = p_df
        except Exception as e:
            print(f"error loading {filepath}: {e}")


# this for returning raw bytes
def _tabulate_to_bytes(data, headers, limit=25):
    top_rows = data[:limit]
    num_columns = len(headers)

    header_color = "#40466e"
    row_colors = ["#f8f9fa", "#ffffff"]
    edge_color = "black"
    text_color = "#333333"
    header_text_color = "#ffffff"

    row_height = 0.5
    fig_height = (len(top_rows) + 1) * row_height + 0.5

    fig, ax = plt.subplots(figsize=(10, fig_height))
    ax.axis("off")
    ax.axis("tight")

    col_widths = [0.15, 0.6, 0.15, 0.1]
    if len(col_widths) != num_columns:
        col_widths = [1.0 / num_columns] * num_columns

    table = ax.table(
        cellText=top_rows,
        colLabels=headers,
        cellLoc="center",
        loc="center",
        colWidths=col_widths,
    )

    table.auto_set_font_size(False)
    table.set_fontsize(16)
    table.scale(1, 2.0)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor(edge_color)
        cell.set_linewidth(1)
        if row == 0:
            cell.set_facecolor(header_color)
            cell.set_text_props(weight="bold", color=header_text_color)
            cell.set_height(0.08)
        else:
            cell.set_facecolor(row_colors[row % 2])
            cell.set_text_props(color=text_color)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(
        buf,
        format="png",
        bbox_inches="tight",
        dpi=150,
        facecolor="white",
        pad_inches=0.1,
    )
    plt.close()
    return buf.getvalue()


# using LRU-Caching techniques for faster generation if command has been accessed prior
@lru_cache(maxsize=32)
def _get_campus_plot_bytes(campus_name):
    campus_name = campus_name.strip().lower()
    filtered_df = df[df["campus"].str.lower() == campus_name]

    if filtered_df.empty:
        return None

    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)
    sns.lineplot(
        data=filtered_df,
        x="year",
        y="marks",
        hue="branch",
        marker="o",
        markersize=6,
        linewidth=2.5,
        palette="tab10",
        ax=ax,
    )
    sns.despine()
    ax.set_title(
        f"Cutoff Trends: {campus_name.title()}",
        loc="left",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    ax.set_xlabel("Year", fontsize=12, labelpad=10)
    ax.set_ylabel("Marks", fontsize=12, labelpad=10)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend(title="Branch", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", bbox_inches="tight", facecolor="white")
    plt.close()
    return buf.getvalue()


@lru_cache(maxsize=64)
def _get_branch_plot_bytes(campus_name, branch_name):
    normalized_branch = normalize_branch_name(branch_name, alias_to_actual)
    if not normalized_branch:
        return None

    campus_name = campus_name.strip().lower()
    filtered_df = df[
        (df["campus"].str.lower() == campus_name)
        & (df["branch"].str.lower() == normalized_branch.lower())
    ]
    if filtered_df.empty:
        return None

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    sns.lineplot(
        data=filtered_df,
        x="year",
        y="marks",
        marker="o",
        markersize=9,
        linewidth=3,
        color="#2E86AB",
        ax=ax,
    )
    sns.despine()
    min_marks = filtered_df["marks"].min()
    max_marks = filtered_df["marks"].max()
    ax.set_ylim(min_marks - 15, max_marks + 15)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.text(
        x=0,
        y=1.02,
        s=f"{campus_name.title()} Campus",
        transform=ax.transAxes,
        fontsize=12,
        color="gray",
    )
    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel("Marks", fontsize=11)

    if len(filtered_df) > 0:
        ax.axhline(y=min_marks, color="#e63946", linestyle="--", alpha=0.5, linewidth=1)
        ax.axhline(y=max_marks, color="#2a9d8f", linestyle="--", alpha=0.5, linewidth=1)
        bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9)
        ax.text(
            filtered_df["year"].min(),
            max_marks,
            f"Max: {max_marks:.0f}",
            va="center",
            ha="right",
            fontsize=10,
            color="#2a9d8f",
            fontweight="bold",
            bbox=bbox_props,
        )
        ax.text(
            filtered_df["year"].min(),
            min_marks,
            f"Min: {min_marks:.0f}",
            va="center",
            ha="right",
            fontsize=10,
            color="#e63946",
            fontweight="bold",
            bbox=bbox_props,
        )

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", bbox_inches="tight", facecolor="white")
    plt.close()
    return buf.getvalue()


@lru_cache(maxsize=32)
def _get_select_table_bytes(year, campus_filter, limit):
    target_df = df[df["year"] == year]
    if target_df.empty:
        return None

    if campus_filter:
        target_campus = campus_filter.strip().lower()
        target_df = target_df[target_df["campus"].str.lower() == target_campus]
        if target_df.empty:
            return None

    target_df = target_df.sort_values(by="marks", ascending=False)

    table_data = target_df[["campus", "branch", "marks", "year"]].copy()
    table_data["campus"] = table_data["campus"].str.title()
    final_data = table_data.values.tolist()
    headers = ["Campus", "Course", "Marks", "Year"]

    return _tabulate_to_bytes(final_data, headers, limit=limit)


@lru_cache(maxsize=32)
def _get_prediction_bytes(situation, campus_filter, limit):
    df_pred = PREDICTIONS.get(situation.lower())
    if df_pred is None:
        return None

    target_df = df_pred.copy()

    if campus_filter:
        target = campus_filter.strip().title()
        if "campus" in target_df.columns:
            target_df = target_df[target_df["campus"] == target]
        if target_df.empty:
            return None

    if "marks" in target_df.columns:
        target_df = target_df.sort_values(by="marks", ascending=False)

    table_data = target_df.values.tolist()
    headers = [h.title() for h in target_df.columns.tolist()]

    return _tabulate_to_bytes(table_data, headers, limit=limit)


# these are for recieving cached bytes
def plot_marks_by_campus(campus_name):
    img_bytes = _get_campus_plot_bytes(campus_name)
    if img_bytes is None:
        return None
    return io.BytesIO(img_bytes)


def plot_marks_by_branch(campus_name, branch):
    normalized = normalize_branch_name(branch, alias_to_actual)
    if not normalized:
        return None

    img_bytes = _get_branch_plot_bytes(campus_name, normalized)
    if img_bytes is None:
        return None
    return io.BytesIO(img_bytes)


def select(limit=25, year=None, campus_filter=None):
    if year is None:
        return None

    # the cache key MUST BE HASHABLE
    img_bytes = _get_select_table_bytes(year, campus_filter, limit)
    if img_bytes is None:
        return None
    return io.BytesIO(img_bytes)


def get_predictions(limit=25, campus_filter=None, situation="most-likely"):
    img_bytes = _get_prediction_bytes(situation, campus_filter, limit)
    if img_bytes is None:
        return None
    return io.BytesIO(img_bytes)


# this is for discord-CDNs
URL_CACHE = {}


def get_cached_url(key):
    return URL_CACHE.get(key)


def save_url_to_cache(key, url):
    URL_CACHE[key] = url
