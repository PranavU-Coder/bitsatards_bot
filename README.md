# First Look At The Bitsatards Bot

This src aims to be the discord bot for r/Bitsatards server, this bot serves the purpose of predicting cutoffs for upcoming bitsat examinations and can support the following commands as of writing this (13/12/2025) :

1. plot < campus > - plots the scores of past years cutoffs across diff campuses.
2. plot < campus >, < branch > - plots the cutoff values wrt a branch of a campus that is required by the end-user.
3. predict < campus (optional) > - sends the user the predicted cutoff values for branches of all campuses (truncated due constraints) or specific campus.
4. resources - sends user resources for preparation of this examination.
5. help - shows all possible commands that are available with example implementation in event that output is not available to the user for some unforseen reason.

Currently the bot is deployed through my second laptop which doubles as a server purely to run programs 24/7 to avoid any middleman (cloud service providers) and charges.

## Future Plans

Since there is so much to experiment with this bot, we openly encourage people to contribute to this and make it as efficient as useful as possible thus making the src open-source.

The dataset is as follows for to work with: https://www.kaggle.com/datasets/pranavunni/bitsat-cutoff-dataset-2017-2025

Some personal plans for the bot I have include :

1. creating a general-purpose website to make the same predictions for people who don't intend to use discord
2. adding a parameter "difficulty" to determine values for best-case and worst-case scenarios
3. general guideline and documentation to contribute to this repository without breaking src

## Apache 2.0 License

Since this repository is licensed under Apache 2.0 license, again we welcome people to contribute under the guideline which will be published with the next release of this bot.
