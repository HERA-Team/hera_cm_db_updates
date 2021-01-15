#! /bin/bash
echo "210114_connupd_2122" >> scripts.log 
# Adding missing parts
add_part.py -p FDV164 -r A -t feed -m FDV164 --date 2021/01/14 --time 21:17
add_part.py -p FDV142 -r A -t feed -m FDV142 --date 2021/01/14 --time 21:17
add_part.py -p FDV161 -r A -t feed -m FDV161 --date 2021/01/14 --time 21:17
add_part.py -p FDV157 -r A -t feed -m FDV157 --date 2021/01/14 --time 21:17
add_part.py -p FEM196 -r A -t front-end -m FEM196 --date 2021/01/14 --time 21:17
add_part.py -p FDV145 -r A -t feed -m FDV145 --date 2021/01/14 --time 21:17
add_part.py -p FEM192 -r A -t front-end -m FEM192 --date 2021/01/14 --time 21:17
add_part.py -p FEM195 -r A -t front-end -m FEM195 --date 2021/01/14 --time 21:17
add_part.py -p FDV158 -r A -t feed -m FDV158 --date 2021/01/14 --time 21:17
add_part.py -p FDV144 -r A -t feed -m FDV144 --date 2021/01/14 --time 21:17
add_part.py -p FEM189 -r A -t front-end -m FEM189 --date 2021/01/14 --time 21:17
add_part.py -p FDV163 -r A -t feed -m FDV163 --date 2021/01/14 --time 21:17
add_part.py -p FEM187 -r A -t front-end -m FEM187 --date 2021/01/14 --time 21:17
add_part.py -p FEM185 -r A -t front-end -m FEM185 --date 2021/01/14 --time 21:17
add_part.py -p FEM193 -r A -t front-end -m FEM193 --date 2021/01/14 --time 21:17
add_part.py -p FDV143 -r A -t feed -m FDV143 --date 2021/01/14 --time 21:17
add_part.py -p FEM191 -r A -t front-end -m FEM191 --date 2021/01/14 --time 21:17
add_part.py -p FEM190 -r A -t front-end -m FEM190 --date 2021/01/14 --time 21:17
add_part.py -p FDV146 -r A -t feed -m FDV146 --date 2021/01/14 --time 21:17
add_part.py -p FEM194 -r A -t front-end -m FEM194 --date 2021/01/14 --time 21:17
# Adding missing connections
add_connection.py -u A7 --uprev H --upport focus -d FDV146 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FDV146 --uprev A --upport terminals -d FEM187 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FEM187 --uprev A --upport e -d NBP02 --dnrev A --dnport e1 --date 2021/01/14 --time 21:22
add_connection.py -u FEM187 --uprev A --upport n -d NBP02 --dnrev A --dnport n1 --date 2021/01/14 --time 21:22
add_connection.py -u A8 --uprev H --upport focus -d FDV145 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FDV145 --uprev A --upport terminals -d FEM191 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FEM191 --uprev A --upport e -d NBP02 --dnrev A --dnport e2 --date 2021/01/14 --time 21:22
add_connection.py -u FEM191 --uprev A --upport n -d NBP02 --dnrev A --dnport n2 --date 2021/01/14 --time 21:22
add_connection.py -u A9 --uprev H --upport focus -d FDV144 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FDV144 --uprev A --upport terminals -d FEM193 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FEM193 --uprev A --upport e -d NBP02 --dnrev A --dnport e3 --date 2021/01/14 --time 21:22
add_connection.py -u FEM193 --uprev A --upport n -d NBP02 --dnrev A --dnport n3 --date 2021/01/14 --time 21:22
add_connection.py -u A10 --uprev H --upport focus -d FDV158 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FDV158 --uprev A --upport terminals -d FEM189 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FEM189 --uprev A --upport e -d NBP02 --dnrev A --dnport e6 --date 2021/01/14 --time 21:22
add_connection.py -u FEM189 --uprev A --upport n -d NBP02 --dnrev A --dnport n6 --date 2021/01/14 --time 21:22
add_connection.py -u A19 --uprev H --upport focus -d FDV161 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FDV161 --uprev A --upport terminals -d FEM185 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FEM185 --uprev A --upport e -d NBP02 --dnrev A --dnport e4 --date 2021/01/14 --time 21:22
add_connection.py -u FEM185 --uprev A --upport n -d NBP02 --dnrev A --dnport n4 --date 2021/01/14 --time 21:22
add_connection.py -u A20 --uprev H --upport focus -d FDV163 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FDV163 --uprev A --upport terminals -d FEM195 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FEM195 --uprev A --upport e -d NBP02 --dnrev A --dnport e5 --date 2021/01/14 --time 21:22
add_connection.py -u FEM195 --uprev A --upport n -d NBP02 --dnrev A --dnport n5 --date 2021/01/14 --time 21:22
add_connection.py -u A21 --uprev H --upport focus -d FDV142 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FDV142 --uprev A --upport terminals -d FEM194 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FEM194 --uprev A --upport e -d NBP02 --dnrev A --dnport e7 --date 2021/01/14 --time 21:22
add_connection.py -u FEM194 --uprev A --upport n -d NBP02 --dnrev A --dnport n7 --date 2021/01/14 --time 21:22
add_connection.py -u A31 --uprev H --upport focus -d FDV157 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FDV157 --uprev A --upport terminals -d FEM190 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FEM190 --uprev A --upport e -d NBP02 --dnrev A --dnport e8 --date 2021/01/14 --time 21:22
add_connection.py -u FEM190 --uprev A --upport n -d NBP02 --dnrev A --dnport n8 --date 2021/01/14 --time 21:22
add_connection.py -u A32 --uprev H --upport focus -d FDV143 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FDV143 --uprev A --upport terminals -d FEM196 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FEM196 --uprev A --upport e -d NBP02 --dnrev A --dnport e9 --date 2021/01/14 --time 21:22
add_connection.py -u FEM196 --uprev A --upport n -d NBP02 --dnrev A --dnport n9 --date 2021/01/14 --time 21:22
add_connection.py -u A33 --uprev H --upport focus -d FDV164 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FDV164 --uprev A --upport terminals -d FEM192 --dnrev A --dnport input --date 2021/01/14 --time 21:22
add_connection.py -u FEM192 --uprev A --upport e -d NBP02 --dnrev A --dnport e10 --date 2021/01/14 --time 21:22
add_connection.py -u FEM192 --uprev A --upport n -d NBP02 --dnrev A --dnport n10 --date 2021/01/14 --time 21:22
# Adding missing parts
