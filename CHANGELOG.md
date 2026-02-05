# Changelog

## 0.1.0 (2026-02-05)


### Features

* 10: established a data-pipeline using bs4, requests and pandas to generate csv-files for cutoffs each year without manual-labour, refactored send-image file in main.py to a generalized display() func for modularity & updated requirements.txt ([e2edacd](https://github.com/PranavU-Coder/bitsatards_bot/commit/e2edacddba015c1a9744661a8a74585c52de49c9))
* 12: added necessary functions such as exam-dates, syllabus and other social links to expand beyond original project's scope for the server, updated resources function. ([b71d23d](https://github.com/PranavU-Coder/bitsatards_bot/commit/b71d23da8682ab3fbcdcb006f475a856ecda4366))
* 15: using SQLAlchemy as ORM for storing user-records in a postgres database, sends user reminder if the record exists in database ([4255013](https://github.com/PranavU-Coder/bitsatards_bot/commit/4255013535bf78f04d39656ad0ed7bd229ed5b05))
* 5: creating rudimentary tests using pytest & unittest library to assess code-quality before pushing & merging to main codebase branch. ([10d9a4a](https://github.com/PranavU-Coder/bitsatards_bot/commit/10d9a4a14cec40ed1d1020569c88e8173e096ed4))


### Bug Fixes

* 5: dummy-env key for testing purposes & a .env.example file hinting all required keys for running this bot at its full functionality. ([3ff90dc](https://github.com/PranavU-Coder/bitsatards_bot/commit/3ff90dc5e1b31229849b4d769df724600a97d06b))
* corrected bot command name in !!time ([ebd0768](https://github.com/PranavU-Coder/bitsatards_bot/commit/ebd07685c6faf6d16d1a93da7afbe09d5e13c73d))
* formatted services/reminder.py message ([aef8913](https://github.com/PranavU-Coder/bitsatards_bot/commit/aef8913ffd9de39f7b43ef04b6741f859a296d48))


### Documentation

* updating README.md, CONTRIBUTING.md for the latest release, added source-code link to discord-bot ([882dbe5](https://github.com/PranavU-Coder/bitsatards_bot/commit/882dbe53fd168702621344cbb894886a6c49867a))
