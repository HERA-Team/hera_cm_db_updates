This repository contains the csv files that transfer configuration management data between the main db and local copies.

The main db is the authoritative source, and this should be a one-way process.

The scripts directory contains shell scripts that are run on qmaster to update the main db.

The process flow is as follows:

On local machine -- hera_cm_updates:
1 - write a python script to generate a bash script to run the hera_mc scripts with appropriate parameters and test locally
2 - `git push origin master`

On qmaster -- hera_cm_updates:
3 = `git pull origin master`
4 - run the bash script on qmaster
4 - run `cm_pack.py --go` to write out new csv files
5 - `git push origin master`

On local machine -- hera_cm_updates:
6 - `git pull origin master`
7 - `cm_init.py` to make sure things are synced
8 - `write_sqlite.py` (followed by the instructions it prints) to make the sqlite version
9 - `git push origin master` to push the sqlite version back up to repo
