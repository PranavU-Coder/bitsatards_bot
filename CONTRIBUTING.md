# Contributing to Bitsatards Bot

## Code-Contributions

### last written on 5/2/2026

Thank you for considering to contribute, Whether you are fixing a bug or adding a new feature, your help is appreciated highly. 

If you are new to open-source or GitHub, follow the steps below to get started ->

1.proceed to fork this [repository](https://github.com/PranavU-Coder/bitsatards_bot) and clone it locally:

```bash
git clone https://github.com/{replace with your username}/bitsatards_bot.git
cd bitsatards_bot
```

2.create a branch for your purpose of work: feat/fix:

```bash
git checkout -b feat/feat-name
# or
git checkout -b fix/bug-name
```

3.this project has **recently** migrated from pip to uv thus it is important to have uv installed on your system.

```bash
uv sync
```

This command will automatically create a virtual environment and install all required packages listed in the uv.lock file.

3.Dev Standards:

(1) Run

```bash
uv run ruff format . 
```

before committing.

(2) Ensure

```bash
uv run ruff check .
```

passes without errors.

(3) Run tests locally

```bash
uv run pytest
```

A passing build is required for any merge.

(4) Commit Messages: Conventional Commits Please, prefix your messages accordingly:

```text
    feat: for new features.
    fix: for bug fixes.
    docs: for documentation/non-code changes.
```

4.commit your changes to your branch.

push your changes to your fork.

open a Pull Request (PR) against the master branch of the original repository.

Wait for the automated tests to pass. Once reviewed they will be merged.

Make sure to appropriately add/remove lines of the PULL_REQUEST_TEMPLATE.md which align to your changes.

<img width="690" height="253" alt="image" src="https://github.com/user-attachments/assets/9f1af6c1-7d73-4f94-89f4-4b1cc84f6496" />

At the moment, I alone am the codeowner of this codebase hence mostly it will be reviewing the pull-requests and approve if it fits with the existing codebase, assuming the scope of this project increases, I'm more than happy to give ownership of this codebase to any enthusiastic contributor who is willing to do code-reviews.

More Recently, I have installed CodeRabbit on this repository to do code-reviews alongside me.

Feature Documentation:

Please add docstrings underneath any new functions or classes. While much of the code is still being documented, it would be a good precedent in terms of open-source projects.

Please consider using strong type hinting for all function signatures and variables. I am of the opinion and in the movement to make this project to be in the direction of 100%-type safe

## Features & Bug Reports

Before contributing, review the [Roadmap](https://github.com/users/PranavU-Coder/projects/9) first to understand current priorities and exisitng issues that are being worked on.

For raising issues, they must follow these criterias to be considered:

Feature Requests: You must explicitly justify why the feature is necessary to be implemented.

Bug Reports: You must provide a clear "Steps to Reproduce" section (check figure below). If the developer cannot replicate the bug based on your description, the issue will be marked as invalid.

Out of Scope (These will not be considered): Do **NOT** raise issues regarding the website's UI or functionality. This codebase is **NOT** a **MONO-REPO** and is hence independent of the web project; such issues will be closed without review.

![issues](https://github.com/user-attachments/assets/66934dc7-b137-4469-a8f5-6272a7681f38)

**PLEASE NOTE**:

This bot is currently self-hosted through my old laptop which doubles as a server rather than a third-party cloud-service provider which leads to uptime problems.

With hostel network dependencies, there is no way to resolve downtime-issues specially if I am not near the laptop which is hosting the bot.

**Possible Solution**: While orchestration for backup service providers is a goal (using good MLOps principles), it has not yet been implemented.

Please do **NOT** open issues regarding temporary bot inactivity. These are known infrastructure limitations, not code problems.

## Pipeline

The project follows a structured execution workflow designed for maintainability. Even without a massive background in Data Science, contributors can help updating the bot's by interacting with scripts:

### Data-Acquisition && Machine-Learning

**data_pipeline.py**: This scrapes official BITS-admission sites containing cutoff scores for particular years and converts raw data into standardized CSV files which can be then put in for model-training.

**helper_notebook.ipynb**: This contains code  for the "model"—currently focused on min-max scaling applications so ... it is more of a statistical-validator than a traditional machine-learning model to process cutoff trends.

**predictions.py**: This bridges between data-science and ML aspect of this repository with the production-aspect. It takes the constraints (user inputs) and applies the model logic to generate results. Note: This script is currently volatile and subject to change as the model logic matures.

### Production

**main.py**: Contains actual code for the bitsatards-discord-bot. It handles events, commands, and integrates with the prediction and database services.

analytics.py: Handles data visualization for the bot's features.

### Databases

/services and /database concerns with the time-tracking feature which is a misc. feature of this bot using postgres as its database and SQLAlchemy as ORM. There is quite a bit of work to do here, but that will be halted till 3.0.0 release.

**init_db.py** helps initializing database on your system with necessary columns.

How to contribute to the flow:

If you are adding a feature, identify where it sits. For example:

A new way to view/formulate data -> analytics.py.

Model-Improvement -> helper_notebook.ipynb

Bot Command -> Modify main.py.

## Discussions

You can engage in discussions with other developers on any particular matter of this codebase in detail, right now it is being used by me to publish my developer logs and updates and any reasoning to the above mentioned.

### Author

* PranavU-Coder
