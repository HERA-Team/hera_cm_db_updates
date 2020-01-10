from astropy.time import Time


def set_it_up(fdat):
    fpin = open(fdat['fnin'], 'r')
    #fpadd = open('crfup_add.out', 'w')
    #fpstp = open('crfup_stop.out', 'w')

    order = fdat['order']
    pamfem = set()
    for line in fpin:
        data = line.split('|')
        up = [data[0].strip(), data[1].strip(), data[4].strip()]
        dn = [data[2].strip(), data[3].strip(), data[5].strip()]
        t0 = data[6].strip()
        t1 = data[7].strip()
        if not len(t1):
            t1 = 'X'
        Time_object_0 = Time(int(t0), format='gps')
        Time_str_0 = str(Time_object_0.isot)
        dt0 = Time_str_0.split('T')[0].replace('-', '/')
        hr0 = ':'.join(Time_str_0.split('T')[1].split(':')[:2])
        if '12' in t1:
            Time_object_1 = Time(int(t1), format='gps')
            Time_str_1 = str(Time_object_0.isot)
            dt1 = Time_str_1.split('T')[0].replace('-', '/')
            hr1 = ':'.join(Time_str_1.split('T')[1].split(':')[:2])
        if order == 'is_down':
            is_pamfem = dn
            is_other = up
        else:
            is_pamfem = up
            is_other = dn
        s = "{}:{}_{}_{}".format(is_pamfem[0], is_other[0], t0, t1)
        if is_pamfem[0][3] == '7':
            print("Wrong PAM/FEM:  {}".format(is_pamfem[0]))
        else:
            pamfem.add(s)
    fpin.close()

    pamfem = sorted(pamfem)
    with open(fdat['fnjson'], 'w') as fpout:
        for _p in pamfem:
            porf, crf = _p.split(':')
            s = '    "{}": "{}",\n'.format(porf, crf)
            fpout.write(s)

    return pamfem


upfile = {'fnin': 'crfup.txt',
          'fnjson': 'crfup.json',
          'order': 'is_down'}

dnfile = {'fnin': 'crfdn.txt',
          'fnjson': 'crfdn.json',
          'order': 'is_up'}

one_to_use = dnfile
x = set_it_up(one_to_use)
