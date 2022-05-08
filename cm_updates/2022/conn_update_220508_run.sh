#! /bin/bash 
# Adding missing parts
add_part.py -p FEM769 -r A -t front-end -m FEM769 --date 2022/05/01 --time 02:30
add_part.py -p FEM312 -r A -t front-end -m FEM312 --date 2022/05/01 --time 02:30
add_part.py -p FDV317 -r A -t feed -m FDV317 --date 2022/05/01 --time 02:30
add_part.py -p FEM702 -r A -t front-end -m FEM702 --date 2022/05/01 --time 02:30
add_part.py -p PAM331 -r A -t post-amp -m PAM331 --date 2022/05/01 --time 02:30
add_part.py -p FDV276 -r A -t feed -m FDV276 --date 2022/05/01 --time 02:30
add_part.py -p FEM321 -r A -t front-end -m FEM321 --date 2022/05/01 --time 02:30
add_part.py -p FEM327 -r A -t front-end -m FEM327 --date 2022/05/01 --time 02:30
add_part.py -p FDV287 -r A -t feed -m FDV287 --date 2022/05/01 --time 02:30
add_part.py -p PAM328 -r A -t post-amp -m PAM328 --date 2022/05/01 --time 02:30
add_part.py -p FDV328 -r A -t feed -m FDV328 --date 2022/05/01 --time 02:30
add_part.py -p PAM325 -r A -t post-amp -m PAM325 --date 2022/05/01 --time 02:30
add_part.py -p FDV349 -r A -t feed -m FDV349 --date 2022/05/01 --time 02:30
add_part.py -p FDV273 -r A -t feed -m FDV273 --date 2022/05/01 --time 02:30
add_part.py -p PAM327 -r A -t post-amp -m PAM327 --date 2022/05/01 --time 02:30
add_part.py -p PAM326 -r A -t post-amp -m PAM326 --date 2022/05/01 --time 02:30
add_part.py -p PAM330 -r A -t post-amp -m PAM330 --date 2022/05/01 --time 02:30
add_part.py -p PAM329 -r A -t post-amp -m PAM329 --date 2022/05/01 --time 02:30
# Stopping connections
stop_connection.py -u FDV197 --uprev A --upport terminals -d FEM231 --dnrev A --dnport input --date 2022/05/01 --time 06:33
stop_connection.py -u PAM207 --uprev A --upport e -d SNPC000081 --dnrev A --dnport e6 --date 2022/05/01 --time 06:35
stop_connection.py -u PAM207 --uprev A --upport n -d SNPC000081 --dnrev A --dnport n4 --date 2022/05/01 --time 06:35
stop_connection.py -u NBP02 --uprev A --upport e11 -d PAM207 --dnrev A --dnport e --date 2022/05/01 --time 06:33
stop_connection.py -u NBP02 --uprev A --upport n11 -d PAM207 --dnrev A --dnport n --date 2022/05/01 --time 06:33
stop_connection.py -u NBP03 --uprev A --upport e8 -d PAM128 --dnrev A --dnport e --date 2022/05/01 --time 06:33
stop_connection.py -u NBP03 --uprev A --upport n8 -d PAM128 --dnrev A --dnport n --date 2022/05/01 --time 06:33
stop_connection.py -u PAM103 --uprev A --upport e -d SNPC000040 --dnrev A --dnport e10 --date 2022/05/01 --time 06:35
stop_connection.py -u PAM103 --uprev A --upport n -d SNPC000040 --dnrev A --dnport n8 --date 2022/05/01 --time 06:35
stop_connection.py -u NBP04 --uprev A --upport e12 -d PAM103 --dnrev A --dnport e --date 2022/05/01 --time 06:33
stop_connection.py -u NBP04 --uprev A --upport n12 -d PAM103 --dnrev A --dnport n --date 2022/05/01 --time 06:33
stop_connection.py -u PAM123 --uprev A --upport e -d SNPC000018 --dnrev A --dnport e6 --date 2022/05/01 --time 06:35
stop_connection.py -u PAM123 --uprev A --upport n -d SNPC000018 --dnrev A --dnport n4 --date 2022/05/01 --time 06:35
stop_connection.py -u NBP05 --uprev A --upport e11 -d PAM123 --dnrev A --dnport e --date 2022/05/01 --time 06:33
stop_connection.py -u NBP05 --uprev A --upport n11 -d PAM123 --dnrev A --dnport n --date 2022/05/01 --time 06:33
stop_connection.py -u PAM148 --uprev A --upport e -d SNPC000045 --dnrev A --dnport e10 --date 2022/05/01 --time 06:35
stop_connection.py -u PAM148 --uprev A --upport n -d SNPC000045 --dnrev A --dnport n8 --date 2022/05/01 --time 06:35
stop_connection.py -u NBP10 --uprev A --upport e12 -d PAM148 --dnrev A --dnport e --date 2022/05/01 --time 06:33
stop_connection.py -u NBP10 --uprev A --upport n12 -d PAM148 --dnrev A --dnport n --date 2022/05/01 --time 06:33
stop_connection.py -u FDV259 --uprev A --upport terminals -d FEM302 --dnrev A --dnport input --date 2022/05/01 --time 06:33
stop_connection.py -u FEM231 --uprev A --upport e -d NBP19 --dnrev A --dnport e1 --date 2022/05/01 --time 06:33
stop_connection.py -u FEM231 --uprev A --upport n -d NBP19 --dnrev A --dnport n1 --date 2022/05/01 --time 06:33
stop_connection.py -u PAM128 --uprev A --upport e -d SNPC000037 --dnrev A --dnport e6 --date 2022/05/01 --time 06:35
stop_connection.py -u PAM128 --uprev A --upport n -d SNPC000037 --dnrev A --dnport n4 --date 2022/05/01 --time 06:35
stop_connection.py -u FEM302 --uprev A --upport e -d NBP21 --dnrev A --dnport e2 --date 2022/05/01 --time 06:33
stop_connection.py -u FEM302 --uprev A --upport n -d NBP21 --dnrev A --dnport n2 --date 2022/05/01 --time 06:33
# Adding missing connections
add_connection.py -u FEM702 --uprev A --upport e -d NBP21 --dnrev A --dnport e2 --date 2022/05/01 --time 16:35
add_connection.py -u FEM702 --uprev A --upport n -d NBP21 --dnrev A --dnport n2 --date 2022/05/01 --time 16:35
add_connection.py -u A320 --uprev H --upport focus -d FDV349 --dnrev A --dnport input --date 2022/05/01 --time 16:35
add_connection.py -u FDV349 --uprev A --upport terminals -d FEM231 --dnrev A --dnport input --date 2022/05/01 --time 16:35
add_connection.py -u PAM330 --uprev A --upport e -d SNPC000037 --dnrev A --dnport e6 --date 2022/05/01 --time 16:35
add_connection.py -u PAM330 --uprev A --upport n -d SNPC000037 --dnrev A --dnport n4 --date 2022/05/01 --time 16:35
add_connection.py -u A321 --uprev H --upport focus -d FDV287 --dnrev A --dnport input --date 2022/05/01 --time 16:35
add_connection.py -u FDV287 --uprev A --upport terminals -d FEM302 --dnrev A --dnport input --date 2022/05/01 --time 16:35
add_connection.py -u PAM328 --uprev A --upport e -d SNPC000081 --dnrev A --dnport e6 --date 2022/05/01 --time 16:35
add_connection.py -u PAM328 --uprev A --upport n -d SNPC000081 --dnrev A --dnport n4 --date 2022/05/01 --time 16:35
add_connection.py -u A322 --uprev H --upport focus -d FDV328 --dnrev A --dnport input --date 2022/05/01 --time 16:35
add_connection.py -u FDV328 --uprev A --upport terminals -d FEM312 --dnrev A --dnport input --date 2022/05/01 --time 16:35
add_connection.py -u FEM312 --uprev A --upport e -d NBP05 --dnrev A --dnport e11 --date 2022/05/01 --time 16:35
add_connection.py -u FEM312 --uprev A --upport n -d NBP05 --dnrev A --dnport n11 --date 2022/05/01 --time 16:35
add_connection.py -u PAM327 --uprev A --upport e -d SNPC000018 --dnrev A --dnport e6 --date 2022/05/01 --time 16:35
add_connection.py -u PAM327 --uprev A --upport n -d SNPC000018 --dnrev A --dnport n4 --date 2022/05/01 --time 16:35
add_connection.py -u A323 --uprev H --upport focus -d FDV273 --dnrev A --dnport input --date 2022/05/01 --time 16:35
add_connection.py -u FDV273 --uprev A --upport terminals -d FEM321 --dnrev A --dnport input --date 2022/05/01 --time 16:35
add_connection.py -u FEM321 --uprev A --upport e -d NBP02 --dnrev A --dnport e12 --date 2022/05/01 --time 16:35
add_connection.py -u FEM321 --uprev A --upport n -d NBP02 --dnrev A --dnport n12 --date 2022/05/01 --time 16:35
add_connection.py -u PAM329 --uprev A --upport e -d SNPC000081 --dnrev A --dnport e10 --date 2022/05/01 --time 16:35
add_connection.py -u PAM329 --uprev A --upport n -d SNPC000081 --dnrev A --dnport n8 --date 2022/05/01 --time 16:35
add_connection.py -u A324 --uprev H --upport focus -d FDV317 --dnrev A --dnport input --date 2022/05/01 --time 16:35
add_connection.py -u FDV317 --uprev A --upport terminals -d FEM327 --dnrev A --dnport input --date 2022/05/01 --time 16:35
add_connection.py -u FEM327 --uprev A --upport e -d NBP04 --dnrev A --dnport e12 --date 2022/05/01 --time 16:35
add_connection.py -u FEM327 --uprev A --upport n -d NBP04 --dnrev A --dnport n12 --date 2022/05/01 --time 16:35
add_connection.py -u PAM331 --uprev A --upport e -d SNPC000040 --dnrev A --dnport e10 --date 2022/05/01 --time 16:35
add_connection.py -u PAM331 --uprev A --upport n -d SNPC000040 --dnrev A --dnport n8 --date 2022/05/01 --time 16:35
add_connection.py -u A325 --uprev H --upport focus -d FDV276 --dnrev A --dnport input --date 2022/05/01 --time 16:35
add_connection.py -u FDV276 --uprev A --upport terminals -d FEM769 --dnrev A --dnport input --date 2022/05/01 --time 16:35
add_connection.py -u FEM769 --uprev A --upport e -d NBP09 --dnrev A --dnport e7 --date 2022/05/01 --time 16:35
add_connection.py -u FEM769 --uprev A --upport n -d NBP09 --dnrev A --dnport n7 --date 2022/05/01 --time 16:35
add_connection.py -u PAM325 --uprev A --upport e -d SNPC000013 --dnrev A --dnport e2 --date 2022/05/01 --time 16:35
add_connection.py -u PAM325 --uprev A --upport n -d SNPC000013 --dnrev A --dnport n0 --date 2022/05/01 --time 16:35
add_connection.py -u PAM326 --uprev A --upport e -d SNPC000045 --dnrev A --dnport e10 --date 2022/05/01 --time 16:35
add_connection.py -u PAM326 --uprev A --upport n -d SNPC000045 --dnrev A --dnport n8 --date 2022/05/01 --time 16:35
# Adding partial connections
add_connection.py -u NBP02 --uprev A --upport e12 -d PAM329 --dnrev A --dnport e --date 2022/05/01 --time 16:35
add_connection.py -u NBP02 --uprev A --upport n12 -d PAM329 --dnrev A --dnport n --date 2022/05/01 --time 16:35
add_connection.py -u NBP09 --uprev A --upport e7 -d PAM325 --dnrev A --dnport e --date 2022/05/01 --time 16:35
add_connection.py -u NBP09 --uprev A --upport n7 -d PAM325 --dnrev A --dnport n --date 2022/05/01 --time 16:35
# Adding different connections
add_connection.py -u NBP02 --uprev A --upport e11 -d PAM328 --dnrev A --dnport e --date 2022/05/01 --time 16:35
add_connection.py -u NBP02 --uprev A --upport n11 -d PAM328 --dnrev A --dnport n --date 2022/05/01 --time 16:35
add_connection.py -u NBP03 --uprev A --upport e8 -d PAM330 --dnrev A --dnport e --date 2022/05/01 --time 16:35
add_connection.py -u NBP03 --uprev A --upport n8 -d PAM330 --dnrev A --dnport n --date 2022/05/01 --time 16:35
add_connection.py -u NBP04 --uprev A --upport e12 -d PAM331 --dnrev A --dnport e --date 2022/05/01 --time 16:35
add_connection.py -u NBP04 --uprev A --upport n12 -d PAM331 --dnrev A --dnport n --date 2022/05/01 --time 16:35
add_connection.py -u NBP05 --uprev A --upport e11 -d PAM327 --dnrev A --dnport e --date 2022/05/01 --time 16:35
add_connection.py -u NBP05 --uprev A --upport n11 -d PAM327 --dnrev A --dnport n --date 2022/05/01 --time 16:35
add_connection.py -u NBP10 --uprev A --upport e12 -d PAM326 --dnrev A --dnport e --date 2022/05/01 --time 16:35
add_connection.py -u NBP10 --uprev A --upport n12 -d PAM326 --dnrev A --dnport n --date 2022/05/01 --time 16:35
add_connection.py -u FDV259 --uprev A --upport terminals -d FEM702 --dnrev A --dnport input --date 2022/05/01 --time 16:35
add_connection.py -u FEM231 --uprev A --upport e -d NBP03 --dnrev A --dnport e8 --date 2022/05/01 --time 16:35
add_connection.py -u FEM231 --uprev A --upport n -d NBP03 --dnrev A --dnport n8 --date 2022/05/01 --time 16:35
add_connection.py -u FEM302 --uprev A --upport e -d NBP02 --dnrev A --dnport e11 --date 2022/05/01 --time 16:35
add_connection.py -u FEM302 --uprev A --upport n -d NBP02 --dnrev A --dnport n11 --date 2022/05/01 --time 16:35
# Adding missing parts
# Adding different parts
