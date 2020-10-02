"""
Make fake temperature data for the node sensors
"""

s = ('insert into node_sensor (time,node,top_sensor_temp,middle_sensor_temp,'
     'bottom_sensor_temp,humidity_sensor_temp,humidity) values ({});')

start = 1280000000

fp = open('add_test_temps.sql', 'w')
t, m, b, h, r = [], [], [], [], []
for i in range(100):
    gps = start + i * 10
    node = i % 11
    top = 20.0 + i % 20 - i % 5
    mid = 20.0 + i % 6 - i % 7
    bot = 20.0 + i % 3 - i % 15
    hum = 20.0 + i % 14 - i % 19
    rh = 80.0 + i % 20 - i % 5
    data = '{},{},{},{},{},{},{}'.format(gps, node, top, mid, bot, hum, rh)
    print(s.format(data), file=fp)
    t.append(top)
    m.append(mid)
    b.append(bot)
    h.append(hum)
    r.append(rh)
