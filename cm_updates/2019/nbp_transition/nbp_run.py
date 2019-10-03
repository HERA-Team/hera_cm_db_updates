from astropy.time import Time
import json


def run_it(fdat):
    add_blanks = '                     '
    stop_blanks = '                      '
    with open(fdat['fnjson'], 'r') as fpjson:
        jdat = json.load(fpjson)
    fpadd = open(fdat['add'], 'w')
    fpstp = open(fdat['stop'], 'w')

    for pol in ['e', 'n']:
        for hpn, val in jdat.items():
            data = val.split(':')

            tim = data[0].split('_')
            t0 = tim[1]
            t1 = tim[2]

            pos = data[1].split(',')
            nbp_hpn = "NBP{:02d}".format(int(pos[0]))
            nbp_portno = pos[1]

            if hpn[0] == 'F':
                up_port = pol
                up = [hpn, 'A', up_port]
                nbp_port = "{}{}a".format(pol, pos[1])
                dn = [nbp_hpn, 'A', nbp_port]
            else:
                nbp_port = "{}{}b".format(pol, pos[1])
                up = [nbp_hpn, 'A', nbp_port]
                dn_port = "{}a".format(pol)
                dn = [hpn, 'A', dn_port]

            Time_object_0 = Time(int(t0), format='gps')
            Time_str_0 = str(Time_object_0.isot)
            dt0 = Time_str_0.split('T')[0].replace('-', '/')
            hr0 = ':'.join(Time_str_0.split('T')[1].split(':')[:2])
            s = "{}[['{}', '{}', '{}'], ['{}', '{}', '{}'], '{}', '{}'],".format(add_blanks, up[0], up[1], up[2], dn[0], dn[1], dn[2], dt0, hr0)
            print('+', s)
            fpadd.write(s + '\n')
            if '12' in t1:
                Time_object_1 = Time(int(t1), format='gps')
                Time_str_1 = str(Time_object_1.isot)
                dt1 = Time_str_1.split('T')[0].replace('-', '/')
                hr1 = ':'.join(Time_str_1.split('T')[1].split(':')[:2])
                s = "{}[['{}', '{}', '{}'], ['{}', '{}', '{}'], '{}', '{}'],".format(stop_blanks, up[0], up[1], up[2], dn[0], dn[1], dn[2], dt0, hr0)
                print('-', s)
                fpstp.write(s + '\n')


upfile = {'fnjson': 'crfup_edited.json',
          'add': 'up_add.txt',
          'stop': 'up_stop.txt'}

dnfile = {'fnjson': 'crfdn_edited.json',
          'add': 'dn_add.txt',
          'stop': 'dn_stop.txt'}

x = run_it(dnfile)
x = run_it(upfile)
