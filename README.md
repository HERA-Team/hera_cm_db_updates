This repository contains the csv files and sqlite database that transfer configuration
management data between the main db and local copies.  It also contains scripts generated
to update the production database and code to interface to the configuration googlesheet.

<<<The main db is the authoritative source, and this should be a one-way process.>>>

# Directories

0.  <root> - csv and db files, along with setup.py etc
1.  <cm_updates> - scripts used to update the postgres database.
2.  <hera_cm> - some base methods/classes to help update the postgres database.
3.  <scripts> - general scripts to support the cm_updates.
