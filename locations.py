from models import Locations
from sqlalchemy import or_
import urllib2
import json
import math
import re


class CodeException(Exception):
    pass


def postal_dist(postalcode, measure, results):
    response = urllib2.urlopen(''.join([
        'http://geocoder.ca/?postal=',
        postalcode,
        '&geoit=xml&json=1'
    ]))
    redict = json.loads(response.read())
    if u'error' in redict:
        raise CodeException
    user_latitude = float(redict[u'latt'])
    user_longitude = float(redict[u'longt'])
    user_latitude_trunc = int(redict[u'latt'][:2])
    user_longitude_trunc = int(redict[u'longt'][:3])
    locations = Locations.query.filter(or_(
        Locations.latitude.like(''.join([str(user_latitude_trunc-1), '%'])),
        Locations.latitude.like(''.join([str(user_latitude_trunc+1), '%'])),
        Locations.latitude.like(''.join([str(user_latitude_trunc), '%'])),
        Locations.longitude.like(''.join([str(user_longitude_trunc-1), '%'])),
        Locations.longitude.like(''.join([str(user_longitude_trunc+1), '%'])),
        Locations.longitude.like(''.join([str(user_longitude_trunc), '%'])),
    )).all()
    locations_close = []
    for location in locations:
        location.distance_deg = math.pow(
            math.pow(
                location.latitude - user_latitude,
                2
            ) + math.pow(
                location.longitude - user_longitude,
                2
            ),
            .5
        )
        location.measure = measure
        if location.measure == 'miles':
            distance_multiplier = 69
        else:
            distance_multiplier = 111.04446
        location.distance = '%.1f' % round(
            location.distance_deg * distance_multiplier,
            1
        )
        if location.distance_deg < float(results) / distance_multiplier:
            locations_close.append(location)
    if len(locations_close) == 0:
        return locations_close
    sorted_locations = sorted(
        locations_close,
        key=lambda location: location.distance_deg
    )
    return sorted_locations
