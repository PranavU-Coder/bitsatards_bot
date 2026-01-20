# Written on: 25/12/2025

## Contributions

I think this goes without saying but still, you need to have a GitHub account to make any sort of contributions to this codebase which also applies to creating issues as well.

If this is your time using GitHub or making code-contributions to open-source projects, no worries! again I am listing how you can still contribute to this project:

1. proceed to fork this [repository](https://github.com/PranavU-Coder/bitsatards_bot)
2. please navigate repositories listed under your profile where you should be able to find this codebase listed as a 'fork', clone that repository under **YOUR** profile and start working on it locally.
3. install all necessary dependencies by running:

   ```bash
   pip install -r requirements.txt
    ```

4. once any changes are made to the codebase from your end, make sure to 'commit' those changes to your forked repository, once the codebase you have modified seems aptly ready for being pushed to main codebase (the one which is under mine) proceed to create a 'pull-request'.

**PLEASE NOTE** that a pull-request will be accepted only and only if the code changes have been tested and were successful locally otherwise it will be **CLOSED**, please remove comments and any irrelevant statements that would be asked in template.md at time of creation of pull-request

<img width="690" height="253" alt="image" src="https://github.com/user-attachments/assets/9f1af6c1-7d73-4f94-89f4-4b1cc84f6496" />

at the moment, I alone am the codeowner of this codebase hence mostly it will be reviewing the pull-requests and approve if it fits with the existing codebase, assuming the scope of this project increases, I'm more than happy to give ownership of this codebase to any enthusiastic contributor who is willing to do code-reviews.

please make sure that you are adding docstrings underneath your functions or any classes if you are planning to define as it will be easier for other developers to read and understand, similarly apply strong type annotations wherever possible, although again honestly at the time of writing this, I myself am guilty of not doing this so I will be working on this as well.

There are plans of integrating unit-tests using pytest to ensure any code-change can handle edge-cases regardless of what the diffs would be.

## Features & Bug Reports

Starting with a pretty obvious phase of development, which is what features or problems will this project be undertaking so to put it shortly, please check the [roadmap](https://github.com/users/PranavU-Coder/projects/9) page to get an idea of what is being actively worked on and what would be worked on in the future.

if you want any feature to be implemented please state **explicitly why exactly it is important** under the [issues](https://github.com/PranavU-Coder/bitsatards_bot/issues) tab by creating an issue under the same mentioned, similarly in bug-related issues please state where exactly is the bug occurring and how to reproduce from the developer's side so it can be worked upon to fix it.

![issues](https://github.com/user-attachments/assets/66934dc7-b137-4469-a8f5-6272a7681f38)

**PLEASE NOTE**:

(1) any issue with website's ui or functionality shouldn't be raised and as such any issues raised on that request will **NOT** be reviewed and closed as this codebase is independent from the one in which the website is going to be made in.

(2) discord bot being inactive at some portions of the day, now the reason why I chose to clear this up right now is because **I AM NOT USING ANY THIRD-PARTY CLOUD SERVICE PROVIDER** for the continuous deployment and execution of the discord bot and am rather using my old laptop as a full-time server to run my programs 24/7 out of which this bot is one of them, once I return back to hostel there would be issues of running this bot particularly given how bad my hostel wifi is (since it frequently goes out) and as such if I'm not available when this occurs there is no way for me to fix it immediately.

there is a fix to the second issue by adopting good MLOps principles and orchestrating deployment of a backup service provider when one goes out, however at the time of writing this I'm not skilled enough to navigate through this and implement it.

## Pipeline

The idea of execution-workflow will be greatly discussed in the second-version/iteration of this bot to ensure other open-source maintainers who might not be traditionally from an ML or a DS background can still maintain this codebase actively without much external help/assistance.

## Discussions

You can engage in discussions with other developers on any particular matter of this codebase in detail, right now it is being used by me to publish my developer logs and updates and any reasoning to the above mentioned.

### Author

* PranavU-Coder
