#! /usr/bin/env python
import sys
sys.path.insert(1, '../hera_cm')
import signal_chain

hera = signal_chain.Update(sys.argv[0])

hera.update_connection('add', ['PAM042', 'A', '@slot'], ['PCH02', 'A', '@slot7'], '2019/08/15', '10:00')
hera.add_part_info('PAM042', 'A', 'Seems to be broken, so swapped slots with PAM041', '2019/08/15', '10:00')
hera.update_part('add', ['NCMPre1', 'A', 'node-control-module', 'NCMPre1'], '2018/7/18', '11:00')
hera.update_part('add', ['NCMPro2', 'A', 'node-control-module', 'NCMPro2'], '2019/5/14', '12:00')
print("""
Edit psql hera_mc:
    update connections set upstream_part='NCMPre1' where upstream_part='NCM1';
    update connections set upstream_part='NCMPro2' where upstream_part='NCMC000196';
    delete from parts where hpn='NCM1';
    delete from parts where hpn='NCMC000196';
""")

hera.add_part_info('N03', 'A', 'Has full set of air curtains.  Fan pipe has extra bends into ground.', '2019/11/13', '11:00')
hera.add_part_info('N04', 'A', 'Has full set of air curtains.', '2019/11/13', '11:00')
hera.add_part_info('N05', 'A', 'Has full set of air curtains.', '2019/11/13', '11:00')
hera.add_part_info('N07', 'A', 'No air curtains and fan pipe has extra bends into ground.', '2019/11/13', '11:00')
hera.add_part_info('N08', 'A', 'No air curtains.', '2019/11/13', '11:00')
hera.add_part_info('N09', 'A', 'No air curtains.', '2019/11/13', '11:00')

hera.done()
