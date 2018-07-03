import csv
import json
import requests
from flask import Flask, request, render_template
from itertools import combinations
from math import sqrt, cos, asin
from logging import getLogger
LOGGER = getLogger(__name__)


MS_BING_MAPS_KEY = 'Aijo43UEi9YeOJ8V3-NfYwHf3V4THXfksacyugubXSwIC2ncRblRPG7_4oYYWetG'
URL_TMPL = 'http://dev.virtualearth.net/REST/v1/Locations/{longitude},{latitude}?o=json&key={key}'
R = 6.378e3  # Earth's radius

app = Flask(__name__)


def get_place_name(longitude, latitude):
    url = URL_TMPL.format(
        longitude=longitude,
        latitude=latitude,
        key=MS_BING_MAPS_KEY
    )
    return json.loads(requests.get(url).content)['resourceSets'][0]['resources'][0]['name']


def haversin(a):
    return (1.0 - cos(a)) / 2.0


def get_distance(p_1, p_2):
    teta_1, phi_1 = p_1[0], p_1[1]
    teta_2, phi_2 = p_2[0], p_2[1]
    dist = 2.0 * R * asin(sqrt(haversin(teta_1 - teta_2 + cos(teta_1) * cos(teta_2) * haversin(phi_1 - phi_2))))
    return dist


@app.route('/get_addresses', methods=['POST', 'GET'])
def get_addresses():
    if request.method == 'POST':
        ret = {'points': list()}
        original_data = dict()
        links = list()
        stream = iter(request.files['data'].stream)

        for line in csv.reader(stream):
            try:
                point_name, longitude, latitude = line
                original_data[point_name] = (float(longitude), float(latitude))
                address = get_place_name(longitude, latitude)
                ret['points'].append({
                    'name': point_name,
                    'address': address
                })
            except:
                pass

        for point_1, point_2 in combinations(original_data, 2):
            try:

                links.append({
                    'name': point_1 + point_2,
                    'distance': get_distance(original_data[point_1], original_data[point_2])
                })
                ret['links'] = links
            except Exception as e:
                print 'Bad data:\n{}\n'.format(e)

        return json.dumps(ret)
    elif request.method == 'GET':
        return render_template('upload_form.html')
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
