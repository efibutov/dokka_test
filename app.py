import csv
import json
import requests
from flask import Flask, flash, request, redirect, url_for, render_template
from itertools import combinations
from math import sin, pi


MS_BING_MAPS_KEY = 'Aijo43UEi9YeOJ8V3-NfYwHf3V4THXfksacyugubXSwIC2ncRblRPG7_4oYYWetG'
URL_TMPL = 'http://dev.virtualearth.net/REST/v1/Locations/{longitude},{latitude}?o=json&key={key}'

app = Flask(__name__)


def get_place_name(longitude, latitude):
    url = URL_TMPL.format(
        longitude=longitude,
        latitude=latitude,
        key=MS_BING_MAPS_KEY
    )
    return json.loads(requests.get(url).content)['resourceSets'][0]['resources'][0]['name']


def get_distance(point_1, point_2):
    # print(point_1)
    # print(point_2)
    return 0


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        ret = {'points': list()}
        original_data = dict()
        links = list()
        stream = iter(request.files['data'].stream)
        next(stream)

        for line in csv.reader(stream):

            try:
                point_name, longitude, latitude = line
                original_data[point_name] = (longitude, latitude)
                address = get_place_name(longitude, latitude)
                ret['points'].append({
                    'name': point_name,
                    'address': address
                })
            except:
                pass

        for point_1, point_2 in combinations(original_data, 2):

            links.append({
                'name': point_1 + point_2,
                'distance': get_distance(original_data[point_1], original_data[point_2])
            })
            ret['links'] = links

        return json.dumps(ret)
    elif request.method == 'GET':
        return render_template('upload_form.html')
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
