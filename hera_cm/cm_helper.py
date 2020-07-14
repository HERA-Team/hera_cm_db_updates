from datetime import datetime
from hera_mc import cm_active


def installed_stations(stype='H'):
    ageo = cm_active.ActiveData()
    ageo.load_geo()
    ageo.load_parts()
    dated_geo = {}
    for key in ageo.geo.keys():
        ageo.geo[key].gps2Time()
        dt = ageo.geo[key].created_date.datetime
        nkey = '{}{:02d}{:02d}{}'.format(dt.year, dt.month, dt.day, key)
        dated_geo[nkey] = ageo.geo[key]
    mfg_dict = {}
    for key in sorted(dated_geo.keys()):
        station_name = dated_geo[key].station_name
        if station_name.startswith(stype):
            dt = datetime.strptime(key[:8], '%Y%m%d')
            dt = datetime.strftime(dt, '%Y/%m/%d')
            if stype == 'H':
                ak = 'A{}:H'.format(station_name[2:])
            elif stype == 'N':
                ak = 'N{}:A'.format(station_name[2:])
            mfg = ageo.parts[ak].manufacturer_number
            mfg_dict[mfg] = (station_name, dt)
            print("{}   {}   {}".format(dt, station_name, mfg))
    return mfg_dict


def installed_parts(ptype='H'):
    apart = cm_active.ActiveData()
    apart.load_parts()
    dated_part = {}
    for key in apart.parts.keys():
        apart.parts[key].gps2Time()
        dt = apart.parts[key].start_date.datetime
        nkey = '{}{:02d}{:02d}{}'.format(dt.year, dt.month, dt.day, key)
        dated_part[nkey] = apart.parts[key]
    for key in sorted(dated_part.keys()):
        part_name = dated_part[key].hpn
        if part_name.startswith(ptype):
            dt = datetime.strptime(key[:8], '%Y%m%d')
            dt = datetime.strftime(dt, '%Y/%m/%d')
            print("{}   {}".format(dt, part_name))
