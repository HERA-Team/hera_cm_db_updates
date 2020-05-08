This repository contains the csv files and sqlite database that transfer configuration management data between the main db and local copies.  It also contains scripts generated to update the production database and code to interface to the <a href="https://docs.google.com/spreadsheets/d/1kUbOpe3Ng3COYc11hd-tOWpUgM7U8gPQlw2hJoKoSaE/edit#gid=0">configuration googlesheet</a>


### Directories
* **root** - csv and db files, along with setup.py etc
* **cm_updates** - scripts used to update the postgres database and two helper scripts to concatenate automated updates (`connupd.py` and `infoupd.py`)
* **hera_cm** - some base methods/classes to help update the postgres database.
* **scripts** - general scripts to support the cm_updates.

### Cronjobs on `qmaster`
##### Update hera_mc config management from googlesheet
* `#35 * * * * /home/obs/anaconda/envs/HERA/bin/update_connect.py -n w --arc-path /home/obs/src/hera_cm_db_updates/cm_updates --script-path /home/obs/src/hera_cm_db_updates`
* `42 * * * * /home/obs/anaconda/envs/HERA/bin/update_info.py -n n --arc-path /home/obs/src/hera_cm_db_updates/cm_updates --script-path /home/obs/src/hera_cm_db_updates`
* `45 * * * * ~/src/hera_cm_db_updates/info_update.sh`
* `47 * * * * ~/src/hera_cm_db_updates/scripts/update_hera_mc_db_repo.sh > /dev/null 2>&1`

##### Publish hookup sumary to hera.today
* `0 15 * * * /home/obs/anaconda/envs/HERA/bin/mc_publish_summary.py`

##### Push the cminfo into redis
* `20 15 * * * /home/obs/anaconda/envs/HERA/bin/update_cminfo_in_redis.py`
