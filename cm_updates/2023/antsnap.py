data_new = {}
data_old = {}


with open('hnew.txt', 'r') as fp:
    for line in fp:
        data = [x.strip() for x in line.split()]
        key = f"{data[0][2:]}{data[10][1:]}"
        data_new[key] = data


with open('hold.txt', 'r') as fp:
    for line in fp:
        data = [x.strip() for x in line.split()]
        key = f"{data[0][2:]}{data[10][1:]}"
        data_old[key] = data