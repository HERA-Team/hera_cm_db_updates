#! /usr/bin/env python
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)


wr = {'WR-len4p0': ['heraNode0wr', '2020/03/01'],
      'WRA000096': ['heraNode1wr', '2020/02/15'],
      'WRA000089': ['heraNode3wr', '2019/11/13'],
      'WR-unknown': ['heraNode4wr', '2019/10/31'],
      'WRA000084': ['heraNode5wr', '2019/10/31'],
      'WRA000028': ['heraNode7wr', '2019/08/02'],
      'WRA000086': ['heraNode8wr', '2019/08/02'],
      'WRA000083': ['heraNode9wr', '2019/05/15'],
      'WRA000093': ['heraNode10wr', '2019/11/13'],
      'WRA000091': ['heraNode12wr', '2020/01/31'],
      'WRA000094': ['heraNode13wr', '2020/01/31'],
      'WRA000097': ['heraNode14wr', '2020/01/31'],
      'WRA000006': ['heraNode15wr', '2020/01/28']
      }

rd = {'RD02': ['heraNode0', '2020/03/01'],
      'RD18': ['heraNode1', '2020/02/15'],
      'RD06': ['heraNode3', '2019/11/13'],
      'RD41': ['heraNode4', '2019/10/31'],
      'RD42': ['heraNode5', '2019/10/31'],
      'RD31': ['heraNode7', '2019/08/02'],
      'RD45': ['heraNode8', '2019/08/02'],
      'RD46': ['heraNode9', '2019/05/15'],
      'RD20': ['heraNode10', '2019/11/13'],
      'RD15': ['heraNode12', '2020/01/31'],
      'RD19': ['heraNode13', '2020/01/31'],
      'RD43': ['heraNode14', '2020/01/31'],
      'RD40': ['heraNode15', '2020/01/28']
      }

for w, r in zip(wr.keys(), rd.keys()):
    hera.update_part_rosetta(w, wr[w][0], wr[w][1])
    hera.update_part_rosetta(r, rd[r][0], rd[r][1])
