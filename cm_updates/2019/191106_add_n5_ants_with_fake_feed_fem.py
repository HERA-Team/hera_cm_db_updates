#! /usr/bin/env python
import sys
sys.path.insert(1, '../hera_cm')
import signal_chain

hera = signal_chain.Update(sys.argv[0])

ser_num = {'node': 7}
node = 5

ant = [43, 44, 45, 46, 58, 59, 60, 73, 74, 75, 76]
feed = [812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822]
fem = [912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922]
nbp_port = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

for i in range(len(ant)):
    hera.add_antenna_to_node(ant[i], feed[i], fem[i], node, nbp_port[i], cdate='2019/10/31', ctime=['12:00', '13:00'], ser_num=ser_num)

hera.done()
