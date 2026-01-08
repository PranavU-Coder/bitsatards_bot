import pandas as pd
import seaborn as sns

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

import os
import glob

data = glob.glob(os.path.join('data/', '*.csv'))
df = pd.concat([pd.read_csv(f) for f in data], ignore_index=True)

def load_branch_mappings(filepath="branch_names.txt"):
    """
    load branch name mappings from 'branch_names' txt file.
    """
    
    alias_to_actual = {}
    actual_to_alias = {}

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                full_name, alias = line.split(':', 1)
                full_name = full_name.strip()
                alias = alias.strip()

                alias_to_actual[alias.lower()] = full_name
                actual_to_alias[full_name.lower()] = alias

    return alias_to_actual, actual_to_alias

def normalize_branch_name(user_input, alias_to_full):
    """
    convert user input (shorthand or full name) to the full branch name.
    returns the full name if found, otherwise None.
    """
    
    user_input = user_input.strip().lower()

    if user_input in alias_to_full:
        return alias_to_full[user_input]

    for alias, full_name in alias_to_full.items():
        if full_name.lower() == user_input:
            return full_name

    return None

alias_to_actual, actual_to_alias = load_branch_mappings('branch_names.txt')

def plot_marks_by_campus(campus_name):
    """
    plot all branches for a given campus 
    """
    
    campus_name = campus_name.strip().lower()

    filtered_df = df[df['campus'].str.lower() == campus_name]

    plt.figure(figsize=(12, 7))
    sns.lineplot(data=filtered_df, x='year', y='marks', hue='branch')
    plt.title(f'Marks Trend for {campus_name.title()}')
    plt.xlabel('Year')
    plt.ylabel('Marks')
    plt.legend(title='Branch', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f'{campus_name}_marks_trend.png')
    plt.close()

def plot_marks_by_branch(campus_name, branch):
    """
    plots marks of a particular branch in a specific BITS campus, uses comma as a separator to indicate respective fields.
    """

    campus_name = campus_name.strip().lower()
    
    normalized_branch = normalize_branch_name(branch, alias_to_actual)
   
    if normalized_branch is None:
        print(f"warning: unknown branch '{branch}'")
        return None

    filtered_df = df[
        (df['campus'].str.lower() == campus_name) &
        (df['branch'].str.lower() == normalized_branch.lower())
    ]

    if filtered_df.empty:
        return None

    plt.figure(figsize=(12, 7))
    sns.lineplot(data=filtered_df, x='year', y='marks')
    plt.title(f"Marks Trend for {normalized_branch.title()} in {campus_name.title()}")
    plt.xlabel('Year')
    plt.ylabel('Marks')
    plt.tight_layout()
    
    safe_branch = normalized_branch.replace(' ', '_').replace('.', '')
    filename = f"{campus_name}_{safe_branch}_marks_trend.png"
    
    plt.savefig(filename)
    plt.close()
    
    return filename

def get_predictions(limit=25, campus_filter=None, situation=None):
    """
    get predictions now based on hypothetical scenarios: "worst", "most-likely" and "best" case.
    instead of hardcoding data like previously done, we will just use values we obtained from predict/..csv files.
    by default we will consider difficulty: most-likely if user doesn't specify.
    by default we will assume top-entries in the file if user doesn't specify campus.
    """
    
        
    map = {
        'worst': 'predict/worst_case.csv',
        'most-likely': 'predict/most_likely_case.csv',
        'best': 'predict/best_case.csv'
    }
    
    if situation is None:
        situation = 'most-likely'

    csv_file = map.get(situation.lower())
    
    if csv_file is None:
        print(f"invalid usage, please use 'worst', 'most-likely' (or leave blank for this), or 'best'")
        return None
    
    try:
        df_pred = pd.read_csv(csv_file)
        headers = df_pred.columns.tolist()
        data = df_pred.values.tolist()
    except FileNotFoundError:
        print(f"file not found: {csv_file}")
        return None
    
    if campus_filter:
        target = campus_filter.strip().lower()
        filtered_data = [row for row in data if str(row[0]).lower() == target]
        
        if not filtered_data:
            return None
        
        filename = f"pred_2026_{target}_{situation}.png"
    else:
        filtered_data = data
        filename = f"pred_2026_all_{situation}.png"
    
    top_rows = filtered_data[:limit]
    
    fig_height = len(top_rows) * 0.4 + 1.2
    
    fig, ax = plt.subplots(figsize=(10, fig_height))
    ax.axis('tight')
    ax.axis('off')
    
    num_cols = len(headers)
    col_widths = [0.15, 0.55, 0.15, 0.15]  

    table = ax.table(
    cellText=top_rows,
    colLabels=headers,
    cellLoc='center',
    loc='center',
    colColours=["#40466e"] * num_cols,
    colWidths=col_widths  
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.8)
    
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
    
    plt.savefig(filename, bbox_inches='tight', dpi=150, pad_inches=0.1)
    plt.close()
    
    return filename
