# First Look At The Bitsatards Bot

This src aims to be the discord bot for r/Bitsatards server, this bot serves the purpose of predicting cutoffs for upcoming bitsat examinations on basis of past-year trends (taking account from 2013) and can supports all of the commands which was planned in the second release (9/1/26):

1. plot < campus > - plots the scores of past years cutoffs across diff campuses.
2. plot < campus >, < branch > - plots the cutoff values wrt a branch of a campus that is required by the end-user.
3. predict < campus (optional) >, < scenario (optional) > - sends the user the predicted cutoff values for branches of all campuses (truncated due constraints) or specific campus based on worst, best or most-likely scenario.
4. resources - sends user resources for preparation of this examination.
5. help - shows all possible commands that are available with example implementation in event that output is not available to the user for some unforseen reason.

Currently the bot is deployed through my second laptop which doubles as a server purely to run programs 24/7 to avoid any middleman (cloud service providers) and charges.

## Future Plans

There are plans to experiment by finding causation and co-relations with cutoffs of other entrance examinations such as: JEE however I don't think I will be able to complete it in time of announcement of this project.

The dataset is as follows for to work with: https://www.kaggle.com/datasets/pranavunni/bitsat-cutoff-dataset-2017-2025 for anyone willing to have their own spin-off to this.

By mid-february 2026:

1. a general-purpose website will be made public for everyone, in specific targetting people who prefer not using discord.
2. rewriting wiki which explains the thought process, procedure and everything that went in to this project (which will go the working/ section of the website as well) and a reformat the existing wiki to CONTRIBUTIONS.md which will serve as a general guideline on contributing without breaking src.

## Apache 2.0 License

Since this repository is licensed under Apache 2.0 license, we welcome collaborations and any intentions to help the community grow.
