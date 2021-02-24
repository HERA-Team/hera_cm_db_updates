#! /bin/bash
echo "210223_pamswap" >> scripts.log 
# Adding different connections

stop_connection.py -u NBP08 --uprev A --upport e12 -d PAM021 --dnrev A --dnport e --date 2021/02/23 --time 09:21
stop_connection.py -u NBP08 --uprev A --upport n12 -d PAM021 --dnrev A --dnport n --date 2021/02/23 --time 09:21
stop_connection.py -u PAM021 --uprev A --upport e -d SNPC000056 --dnrev A --dnport e10 --date 2021/02/23 --time 09:21
stop_connection.py -u PAM021 --uprev A --upport n -d SNPC000056 --dnrev A --dnport n8 --date 2021/02/23 --time 09:21
stop_connection.py -u PAM021 --uprev A --upport slot -d PCH03 --dnrev A --dnport slot12 --date 2021/02/23 --time 09:21
add_part_info.py -p PAM021 -r A -c 'PAM removed by staff during node 8 polish' -l "site staff" --date 2021/02/23 --time 10:00


stop_connection.py -u NBP02 --uprev A --upport e12 -d PAM208 --dnrev A --dnport e --date 2021/02/23 --time 09:21
stop_connection.py -u NBP02 --uprev A --upport n12 -d PAM208 --dnrev A --dnport n --date 2021/02/23 --time 09:21
stop_connection.py -u PAM208 --uprev A --upport e -d SNPC000081 --dnrev A --dnport e10 --date 2021/02/23 --time 09:21
stop_connection.py -u PAM208 --uprev A --upport n -d SNPC000081 --dnrev A --dnport n8 --date 2021/02/23 --time 09:21
stop_connection.py -u PAM208 --uprev A --upport slot -d PCH14 --dnrev A --dnport slot12 --date 2021/02/23 --time 09:21

add_connection.py -u NBP08 --uprev A --upport e12 -d PAM208 --dnrev A --dnport e --date 2021/02/23 --time 09:22
add_connection.py -u NBP08 --uprev A --upport n12 -d PAM208 --dnrev A --dnport n --date 2021/02/23 --time 09:22
add_connection.py -u PAM208 --uprev A --upport e -d SNPC000056 --dnrev A --dnport e10 --date 2021/02/23 --time 09:22
add_connection.py -u PAM208 --uprev A --upport n -d SNPC000056 --dnrev A --dnport n8 --date 2021/02/23 --time 09:22
add_connection.py -u PAM208 --uprev A --upport slot -d PCH03 --dnrev A --dnport slot12 --date 2021/02/23 --time 09:22

# Adding different parts
