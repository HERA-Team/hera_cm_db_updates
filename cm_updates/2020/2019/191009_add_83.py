#! /usr/bin/env python
import sys
sys.path.insert(1, '../hera_cm')
import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)

ser_num = {'node': 4}
node = 7

ant = [83]
feed = [48]
fem = [37]
nbp_port = [3]

for i in range(len(ant)):
    hera.add_antenna_to_node(ant[i], feed[i], fem[i], node, nbp_port[i], cdate='2019/10/09', ctime=['10:00', '11:00'], ser_num=ser_num)

hera.done()
