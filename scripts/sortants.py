def doit(fn):
    ants = {}
    with open(fn, 'r') as fp:
        for line in fp:
            data = line.split()
            ano = int(data[0][2:])
            ana = data[0]
            E = float(data[1])
            N = float(data[2])
            lng = float(data[3])
            lat = float(data[4])
            ants[ano] = [ana, E, N, lng, lat]
    sak = sorted(list(ants.keys()))
    # with open(fn, 'w') as fp:
    #     for k in sak:
    #         x = ants[k]
    #         s = '{:5s}  {:.2f} {:.2f} {:.4f} {:.4f}\n'.format(x[0], x[1], x[2], x[3], x[4])
    #         fp.write(s)

    num_per_row = 15
    with open('listants.txt', 'w') as fp:
        for i in range(0, len(sak), num_per_row):
            s = ' '.join(['{:>3s}'.format(str(x)) for x in sak[i: i + num_per_row]])
            print(s)
            fp.write(s + '\n')
