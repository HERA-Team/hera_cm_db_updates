#! /usr/bin/env python
import sys
sys.path.insert(1, '../hera_cm')
import signal_chain

hera = signal_chain.Update(sys.argv[0])

ser_num = {'node': 4}
node = 7

ant = [81, 82, 98, 99, 100, 116, 117, 118, 119, 137, 138]
feed = [26, 27, 28, 29, 30, 31, 32, 33, 34, 49, 47]
fem = [17, 51, 50, 52, 48, 14, 15, 53, 13, 49, 47]
nbp_port = [1, 2, 7, 8, 4, 9, 10, 11, 5, 12, 6]

for i in range(len(ant)):
    hera.add_antenna_to_node(ant[i], feed[i], fem[i], node, nbp_port[i], cdate='2019/10/02', ctime=['10:00', '11:00'], ser_num=ser_num)

hera.done()
