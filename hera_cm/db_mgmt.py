"""
Methods to check and update the database files for csv and sqlite
"""
from hera_mc import mc, cm_table_info
import os.path

use_later = cm_table_info.cm_tables  # but for now be safe...mainly about order and cm_version
csv_init_table_list = ['apriori_antenna', 'connections', 'geo_location',
                       'part_info', 'parts', 'station_type', 'part_rosetta']


psql_table_dump_list = ['apriori_antenna', 'cm_version', 'connections',
                        'geo_location', 'part_info', 'parts', 'station_type',
                        'part_rosetta']


cm_table_hash_filename = 'cm_table_file_hash.txt'


def check_table_hash_info(hash_dict, hash_filename=cm_table_hash_filename):
    cm_csv_path = mc.get_cm_csv_path(None)
    current_hash_dict = get_table_hash_info(table_list=csv_init_table_list)
    previous_hash_dict = {}
    fnfp = os.path.join(cm_csv_path, hash_filename)
    if not os.path.exists(fnfp):
        return False
    with open(fnfp, 'r') as fp:
        for line in fp:
            data = line.strip().split(',')
            if len(data) == 2:
                previous_hash_dict[data[0]] = data[1]
    current_set = set(current_hash_dict.keys())
    if current_set != set(previous_hash_dict.keys()):
        return False
    for key in current_set:
        if current_hash_dict[key] != previous_hash_dict[key]:
            return False
    return True


def get_table_hash_info(table_list=csv_init_table_list):
    """Writes the hash of the csv data-files to cm_table_file_hash.csv"""
    cm_csv_path = mc.get_cm_csv_path(None)
    hash_dict = {}
    for table in table_list:
        fn = "initialization_{}.csv".format(table)
        fnfp = os.path.join(cm_csv_path, fn)
        hash_dict[fn] = hash_file(fnfp)
    return hash_dict


def write_table_hash_info(table_list=csv_init_table_list, hash_filename=cm_table_hash_filename):
    """Writes the hash of the csv data-files to cm_table_file_hash.csv"""
    cm_csv_path = mc.get_cm_csv_path(None)
    with open(os.path.join(cm_csv_path, hash_filename), 'w') as fp:
        for table in table_list:
            fn = "initialization_{}.csv".format(table)
            x = hash_file(fn)
            print("{},{}".format(fn, x), file=fp)


def hash_file(filename):
    import hashlib
    """This function returns the MD5 hash of the file passed into it"""
    h = hashlib.md5()
    with open(filename, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()


def update_sqlite(table_dump_list=psql_table_dump_list):
    import subprocess
    cm_csv_path = mc.get_cm_csv_path(None)

    subprocess.call('pg_dump -s hera_mc > schema.sql', shell=True)
    dump = ('pg_dump --inserts --data-only hera_mc -t {} > inserts.sql'
            .format(' -t '.join(table_dump_list)))
    subprocess.call(dump, shell=True)

    schema = ''
    creating_table = False
    with open('schema.sql', 'r') as f:
        for line in f:
            modline = line.replace('public.', '')
            if 'CREATE TABLE' in modline:
                creating_table = True
                schema += modline
                continue
            if creating_table:
                if 'DEFAULT' in modline:
                    dat = modline.split()
                    schema += (dat[0] + ' ' + dat[1] + '\n')
                else:
                    schema += modline
                if ');' in modline:
                    creating_table = False

    inserts = ''
    with open('inserts.sql', 'r') as f:
        for line in f:
            modline = line.replace('public.', '')
            if 'INSERT' in modline:
                inserts += modline

    sqlfile = os.path.join(cm_csv_path, 'cm_hera.sql')
    dbfile = os.path.join(cm_csv_path, 'hera_mc.db')
    with open(sqlfile, 'w') as f:
        f.write(schema)
        f.write(inserts)
        f.write(".save {}\n".format(dbfile))
    subprocess.call('sqlite3 < {}'.format(sqlfile), shell=True)

    subprocess.call('rm -f schema.sql', shell=True)
    subprocess.call('rm -f inserts.sql', shell=True)
    subprocess.call('rm -f {}'.format(sqlfile), shell=True)
