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
    plt.savefig(f"{campus_name}_{branch}_marks_trend.png")
    plt.close()

plot_marks_by_campus('Pilani')
plot_marks_by_branch('Pilani', 'B.E. Computer Science')

def help():
    print(f"This bot is designed to make predictions for upcoming bitsat examination, Thanks for using!")
    print(f"These are the commands you can use presently (for branch-names try to write their exact names like 'B.E. Computer Science' etc.)")
    print(f".plot (campus-name)")
    print(f".plot-branch (campus-name) (branch-name)")

help()