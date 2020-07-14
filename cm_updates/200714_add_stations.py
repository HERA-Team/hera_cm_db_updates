#! /usr/bin/env python
"""Add antennas."""
import sys
from hera_cm import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)

# def add_antenna_station(self, stn, ser_num, cdate, ctime='10:00'):
#     """
#     Add an antenna station to the database.
#
#     Parameters
#     ----------
#     stn : string or int
#           antenna number (digits only)
#     ser_num : string or int
#               installation order number of antenna
#     cdate : string
#             YYYY/MM/DD format
#     ctime : string
#             HH:MM format
#     """

# stns = [278, 279, 263, 293, 294, 280, 364, 265, 276, 304, 305, 306, 307, 317, 318, 319, 277]
stns = [263, 264, 265, 280, 278, 279, 293, 294, 307, 276, 277, 306, 319, 305, 318, 304, 317]
sers = [284, 285, 289, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304]
# cdates = ['2020/06/29', '2020/06/29', '2020/06/25', '2020/06/30', '2020/06/30', '2020/06/26',
#           '2020/06/25', '2020/06/26', '2020/07/01', '2020/07/10', '2020/07/08', '2020/07/02',
#           '2020/06/30', '2020/07/10', '2020/07/08', '2020/07/03', '2020/07/01']
cdates = ['2020/06/25', '2020/06/25', '2020/06/26', '2020/06/26', '2020/06/29', '2020/06/29',
          '2020/06/30', '2020/06/30', '2020/06/30', '2020/07/01', '2020/07/01', '2020/07/02',
          '2020/07/03', '2020/07/08', '2020/07/08', '2020/07/10', '2020/07/10']

for stn, sn, cd in zip(stns, sers, cdates):
    hera.add_antenna_station(stn, sn, cd)

hera.done()
