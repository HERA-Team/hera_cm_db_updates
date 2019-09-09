This repository contains the csv files that transfer configuration management data between the main db and local copies.
It also contains the sqlite database.

The main db is the authoritative source, and this should be a one-way process.

The scripts directory contains shell scripts that are run on qmaster to update the main db.

The process flow is as follows:

On local machine -- hera_cm_updates:
1 - generate a script to run the hera_mc scripts with appropriate parameters and test locally
    this may be generated via cm_overview/cmov to update relative to the googlesheet at
    https://docs.google.com/spreadsheets/d/1kUbOpe3Ng3COYc11hd-tOWpUgM7U8gPQlw2hJoKoSaE/edit#gid=0
2 - `git push origin master`

On qmaster -- hera_cm_updates:
3 = `git pull origin master`
4 - run the bash script on qmaster
5 - run `cm_pack.py --go` to write out new csv files
6 - `git push origin master`
7 - `mc_publish_summary.py`

On local machine -- hera_cm_updates:
8 - `git pull origin master`
9 - `cm_init.py` to make sure things are synced
10 - `write_sqlite.py` (followed by the instructions it prints) to make the sqlite version
11 - `git push origin master` to push the sqlite version back up to repo

This has another option of (`--base`), so that you can set up a base copy to which you can revert if need be by including `--base` under `cm_pack.py`
This is largely deprecated, since Git has a history.

Note, if you want to update the site database (not recommended) you must set up a key when you pack and then init.
