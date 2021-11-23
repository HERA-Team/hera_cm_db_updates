This repository contains the csv files and sqlite database that transfer configuration management data between the main db and local copies.  It also contains scripts generated to update the production database and code to interface to the <a href="https://docs.google.com/spreadsheets/d/1kUbOpe3Ng3COYc11hd-tOWpUgM7U8gPQlw2hJoKoSaE/edit#gid=0">configuration googlesheet</a>


### Directories
* **root** - csv and db files, along with setup.py etc
* **cm_updates** - scripts used to update the postgres database and two helper scripts to concatenate automated updates (`connupd.py` and `infoupd.py`)
* **hera_cm** - some base methods/classes to help update the postgres database.
* **scripts** - general scripts to support the cm_updates.
