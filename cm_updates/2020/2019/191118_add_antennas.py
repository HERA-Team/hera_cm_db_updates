#! /usr/bin/env python
import sys
sys.path.insert(1, '../hera_cm')
import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)

ser_num = {}
node = 5

ant = [43, 44, 45, 46, 58, 59, 60, 73, 74, 75]
feed = [50, 59, 56, 57, 67, 66, 64, 60, 73, 62]
fem = [116, 109, 102, 110, 118, 103, 108, 122, 111, 115]
nbp_port = [8, 6, 1, 2, 5, 4, 7, 3, 9, 10]

for i in range(len(ant)):
    hera.add_antenna_to_node(ant[i], feed[i], fem[i], node, nbp_port[i], cdate='2019/11/16', ctime=['10:00', '11:00'], ser_num=ser_num)


node = 4

ant = [40, 41, 42, 54, 55, 56, 57, 69, 70, 71, 72]
feed = [58, 52, 53, 54, 23, 72, 71, 65, 55, 63, 61]
fem = [101, 104, 123, 120, 119, 105, 113, 121, 112, 114, 124]
nbp_port = [6, 10, 2, 3, 7, 4, 11, 5, 9, 8, 1]

for i in range(len(ant)):
    hera.add_antenna_to_node(ant[i], feed[i], fem[i], node, nbp_port[i], cdate='2019/11/16', ctime=['10:00', '11:00'], ser_num=ser_num)


hera.done()
