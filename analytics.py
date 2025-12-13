import pandas as pd
import seaborn as sns

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

import os
import glob

data = glob.glob(os.path.join('data/', '*.csv'))
df = pd.concat([pd.read_csv(f) for f in data], ignore_index=True)

df.columns = df.columns.str.strip()

def plot_marks_by_campus(campus_name):

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
    campus_name = campus_name.strip().lower()
    branch = branch.strip().lower()
    
    filtered_df = df[
        (df['campus'].str.lower() == campus_name) &
        (df['branch'].str.lower() == branch)
    ]

    plt.figure(figsize=(12, 7))
    sns.lineplot(data=filtered_df, x='year', y='marks')
    plt.title(f"Marks Trend for {branch.title()} in {campus_name.title()}")
    plt.xlabel('Year')
    plt.ylabel('Marks')
    plt.tight_layout()
    
    safe_branch = branch.replace(' ', '_').replace('.', '')
    filename = f"{campus_name}_{safe_branch}_marks_trend.png"
    
    plt.savefig(filename)
    plt.close()
    
    return filename

# I am removing the help func temporarily as it is pointless with discord bot since the printed strings are returned to console logs to me and not to the user directly

def get_predictions(limit=25, campus_filter=None):

    headers = ["Campus", "Branch", "Marks"]
    
    # hardcoded data (Campus, Branch, Marks) from predictions_2026.csv since this is easier to compute and fetch for the bot.
    
    data = [
        ["Pilani", "B.E. Computer Science", 317],
        ["Pilani", "B.E. Mathematics and Computing", 286],
        ["Goa", "B.E. Computer Science", 278],
        ["Pilani", "B.E. Electrical & Communication", 272],
        ["Hyderabad", "B.E. Computer Science", 272],
        ["Goa", "B.E. Mathematics and Computing", 271],
        ["Hyderabad", "B.E. Mathematics and Computing", 262],
        ["Pilani", "B.E. Electrical & Electronics", 260],
        ["Goa", "B.E. Electronics & Communication", 257],
        ["Hyderabad", "B.E. Electronics & Communication", 254],
        ["Pilani", "B.E. Electronics & Instrumentation", 252],
        ["Pilani", "M.Sc. Economics", 251],
        ["Goa", "B.E. Electronics and Computer", 249],
        ["Hyderabad", "B.E. Electrical & Electronics", 244],
        ["Goa", "B.E. Electrical & Electronics", 243],
        ["Goa", "M.Sc. Economics", 243],
        ["Hyderabad", "M.Sc. Economics", 240],
        ["Pilani", "B.E. Mechanical", 238],
        ["Goa", "B.E. Electronics & Instrumentation", 238],
        ["Pilani", "M.Sc. Semiconductor", 237], 
        ["Pilani", "M.Sc. Mathematics", 237],
        ["Pilani", "M.Sc. Physics", 237],
        ["Hyderabad", "B.E. Electronics & Instr.", 234], 
        ["Goa", "M.Sc. Physics", 228],
        ["Goa", "M.Sc. Mathematics", 228],
        ["Goa", "B.E. Mechanical", 228],
        ["Goa", "M.Sc. Semiconductor", 228],
        ["Hyderabad", "M.Sc. Semiconductor", 225],
        ["Hyderabad", "M.Sc. Mathematics", 225],
        ["Hyderabad", "B.E. Mechanical", 225],
        ["Pilani", "B.E. Chemical", 224],
        ["Hyderabad", "M.Sc. Physics", 223],
        ["Pilani", "M.Sc. Chemistry", 221],
        ["Pilani", "B.E. Manufacturing", 219],
        ["Goa", "B.E. Chemical", 215],
        ["Hyderabad", "B.E. Chemical", 214],
        ["Pilani", "B.E. Civil", 213],
        ["Hyderabad", "M.Sc. Chemistry", 212],
        ["Goa", "M.Sc. Chemistry", 212],
        ["Pilani", "M.Sc. Bio Sciences", 211],
        ["Hyderabad", "B.E. Civil", 210],
        ["Goa", "M.Sc. Bio Sciences", 202],
        ["Goa", "B.E. Environmental", 202],
        ["Hyderabad", "M.Sc. Bio Sciences", 199],
        ["Pilani", "B. Pharm", 164],
        ["Hyderabad", "B. Pharm", 152]
    ]

    if campus_filter:
        target = campus_filter.strip().lower()
        filtered_data = [row for row in data if row[0].lower() == target]
        
        if not filtered_data:
            return None 
            
        filename = f"pred_2026_{target}.png"
    else:
        filtered_data = data
        filename = "pred_2026_all.png"

    top_rows = filtered_data[:limit]
    
    fig_height = len(top_rows) * 0.4 + 1.2
    
    fig, ax = plt.subplots(figsize=(10, fig_height))
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(
        cellText=top_rows,
        colLabels=headers,
        cellLoc='center',
        loc='center',
        colColours=["#40466e"] * 3
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