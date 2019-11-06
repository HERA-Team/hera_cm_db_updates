#! /usr/bin/env python
import sys
sys.path.insert(1, '../hera_cm')
import signal_chain

hera = signal_chain.Update(sys.argv[0])

ser_num = {'node': 6}
node = 4

ant = [40, 41, 42, 54, 55, 56, 57, 69, 70, 71, 72]
feed = [800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810]
fem = [900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910]
nbp_port = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

for i in range(len(ant)):
    hera.add_antenna_to_node(ant[i], feed[i], fem[i], node, nbp_port[i], cdate='2019/10/31', ctime=['12:00', '13:00'], ser_num=ser_num)

hera.done()
