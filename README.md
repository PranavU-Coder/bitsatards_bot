![License](https://img.shields.io/github/license/PranavU-Coder/bitsatards_bot)
![Python Version](https://img.shields.io/badge/python-3.14-blue)
![Package Manager](https://img.shields.io/badge/manager-uv-purple)
![Linter](https://img.shields.io/badge/linter-ruff-red)
![Status](https://img.shields.io/badge/Status-Stable-success)

# Introducing Bitsatards-Bot

This src aims to be the discord bot for r/Bitsatards server, this bot serves the purpose of predicting cutoffs for upcoming bitsat examinations on basis of past-year trends (taking account from 2013) and can supports all of the commands which was planned in the second release (9/1/26):

| Category | Command | Usage Example | Description |
| :--- | :--- | :--- | :--- |
| **Data Viz** | `!!plot` | `!!plot Pilani` | Generates a trend plot for all branches in a specific campus. |
| | `!!plot-branch` | `!!plot-branch CSE Pilani` | Plots historical cutoffs for a specific branch at a specific campus. |
| | `!!select` | `!!select 2024 Goa` | Fetches and displays a snapshot of cutoffs for a specific year. |
| **Predictions** | `!!predict` | `!!predict Pilani worst` | Returns 2026 predictions based on Worst, Best, or Most-Likely scenarios. |
| **Exam Info** | `!!sy` | `!!sy` | Provides the official BITSAT syllabus PDF link. |
| | `!!da` | `!!da` | Displays important dates for BITSAT 2026 Session 1 & 2. |
| | `!!resources` | `!!resources` | Links to the Reddit wiki and curated Discord resource channels. |
| **Tracking** | `!!time` | `!!time` | Shows a countdown to your saved exam date. |
| | `!!time -s` | `!!time -s 15-04-2026` | Sets/Updates your personal BITSAT exam date. |
| | `!!time -r` | `!!time -r` | Resets your saved exam date from the database. |
| **Misc** | `!!ypt` | `!!ypt` | Shares the Yeolpumta (YPT) study group link and password. |

Currently the bot is deployed through my second laptop which doubles as a server purely to run programs 24/7 to avoid any middleman (cloud service providers) and charges.

## Results Thus Far!

![campus-trend](results/Pilani_Trend.png)

*Pilani campus plot from 2013*

------------------------------------------------------------------------------

![branch-trend](results/Pilani_CSE_Trend.png)

*CSE plot for Pilani from 2013*

------------------------------------------------------------------------------

![most-likely-predictions](results/Pilani_Most_Likely.png)

*probable values for Pilani campus in 2026*

The model in effect for prediction is a polynomial-regression of degree:2, this approach provided the lowest mean squared error compared to other linear/ensemble approaches.

> [!NOTE]
> I would like to clarify that this acts more as a statistical-validator than a plain machine-learning model as not much variance factors and features have been computed yet (discussed below).

## Tech Stack

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.6.4-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![UV](https://img.shields.io/badge/Package_Manager-UV-8A2BE2?style=for-the-badge&logo=astral&logoColor=white)](https://github.com/astral-sh/uv)
[![Pandas](https://img.shields.io/badge/Pandas-3.0.0-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.8.0-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10.8-ffffff?style=for-the-badge&logo=matplotlib&logoColor=black)](https://matplotlib.org/)
[![Numpy](https://img.shields.io/badge/Numpy-2.4.2-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.46-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Ruff](https://img.shields.io/badge/Linter-Ruff-D7FF64?style=for-the-badge&logo=ruff&logoColor=black)](https://github.com/astral-sh/ruff)
[![Pytest](https://img.shields.io/badge/Testing-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)

## Future Plans

There are plans to experiment by finding causation and co-relations with cutoffs of other entrance examinations such as: JEE however I don't think I will be able to complete it in time of announcement of this project.

The dataset is as follows for to work with: [dataset](!https://www.kaggle.com/datasets/pranavunni/bitsat-cutoff-dataset-2017-2025) for anyone willing to have their own spin-off to this.

By mid-february 2026:

1. a general-purpose website will be made public for everyone, in specific targetting people who prefer not using discord (We are almost there!)

After public-announcement & promotion, I will be back to implement various features and factors I have pinpointed thus far which can help in model-predictions more than anything.

> ## Contributing
> This project is developed hoping to be a community effort. If you'd like to improve the model or add features, please check our [CONTRIBUTING.md](./CONTRIBUTING.md) for general guidelines.
> 
> ---
> *Licensed under Apache 2.0*

<a href="https://star-history.com/#PranavU-Coder/bitsatards_bot&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=PranavU-Coder/bitsatards_bot&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=PranavU-Coder/bitsatards_bot&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=PranavU-Coder/bitsatards_bot&type=Date" />
 </picture>
</a>

Contributors till now:

<a href="https://github.com/PranavU-Coder/bitsatards_bot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=PranavU-Coder/bitsatards_bot" />
</a>

Made with [contrib.rocks](https://contrib.rocks).