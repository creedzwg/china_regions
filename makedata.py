# -*- coding:utf-8 -*-
import json
import codecs
from collections import OrderedDict


def make_data():
    source_file_list = [
        'area', 'area_object', 'city', 'city_object', 'province', 'province_object']
    for k in source_file_list:
        data = codecs.open('json/%s.json' % k, 'r', 'utf-8').read()
        js_data = 'let %s = ' % k + data + '\nexport {%s} ' % k
        out_js = codecs.open('js/%s.js' % k, 'w', 'utf-8')
        out_js.write(js_data)
        json_data = json.loads(data)
        mysql_data = ''
        if k == 'area':
            index = 0
            for p in sorted(json_data.keys()):
                for area in json_data[p]:
                    index += 1
                    mysql_data += "INSERT INTO area  VALUES ('%s', '%s', '%s', '%s');\n" % (index, area['name'], area['id'], p)  # noqa

        if k == 'province':
            for index, i in enumerate(json_data):
                mysql_data += "INSERT INTO province VALUES ('%s', '%s', '%s');\n" % (index + 1, i['name'], i['id'])  # noqa

        if k == 'city':
            index = 0
            for p in sorted(json_data.keys()):
                for city in json_data[p]:
                    index += 1
                    mysql_data += "INSERT INTO city VALUES ('%s', '%s', '%s', '%s');\n" % (index, city['id'], city['name'], p)  # noqa

        if k in ['province', 'city', 'area']:
            out_mysql = codecs.open('mysql/%s.sql' % k, 'w', 'utf-8')
            out_mysql.write(mysql_data)

            out_mysql = codecs.open('postgresql/%s.sql' % k, 'w', 'utf-8')
            out_mysql.write(mysql_data)


def pull_data():
    province_object_json = json.loads(
        codecs.open('json/province_object.json', 'r', 'utf-8').read())
    city_json = json.loads(codecs.open('src/city.json', 'r', 'utf-8').read())
    country_json = json.loads(codecs.open('src/country.json', 'r', 'utf-8').read())
    town_json = json.loads(codecs.open('src/town.json', 'r', 'utf-8').read())
    village_json = json.loads(codecs.open('src/village.json', 'r', 'utf-8').read())
    city_object_d = OrderedDict()
    city_d = OrderedDict()
    for c in city_json:
        parent_id = c['id'][0:2] + '0000000000'
        obj = {
            "province": province_object_json[parent_id]['name'],
            "name": c['name'],
            "id": c['id']
        }
        city_object_d[c['id']] = obj
        city_d.setdefault(parent_id, []).append(obj)

    out_city_object = codecs.open('json/city_object.json', 'w', 'utf-8')
    out_city = codecs.open('json/city.json', 'w', 'utf-8')
    out_city_object.write(json.dumps(
        city_object_d, ensure_ascii=False, indent=4))
    out_city.write(json.dumps(city_d, ensure_ascii=False, indent=4))

    country_object_d = OrderedDict()
    country_d = OrderedDict()

    for c in country_json:
        parent_id = c['id'][0:4] + '00000000'
        obj = {
            "city": city_object_d[parent_id]['name'],
            "name": c['name'],
            "id": c['id']
        }
        country_object_d[c['id']] = obj
        country_d.setdefault(parent_id, []).append(obj)

    out_country_object = codecs.open('json/country_object.json', 'w', 'utf-8')
    out_country = codecs.open('json/country.json', 'w', 'utf-8')
    out_country_object.write(json.dumps(
        country_object_d, ensure_ascii=False, indent=4))
    out_country.write(json.dumps(country_d, ensure_ascii=False, indent=4))

    town_object_d = OrderedDict()
    town_d = OrderedDict()

    for c in town_json:
        parent_id = c['id'][0:6] + '000000'
        obj = {
            "city": country_object_d[parent_id]['name'],
            "name": c['name'],
            "id": c['id']
        }
        town_object_d[c['id']] = obj
        town_d.setdefault(parent_id, []).append(obj)

    out_town_object = codecs.open('json/town_object.json', 'w', 'utf-8')
    out_town = codecs.open('json/town.json', 'w', 'utf-8')
    out_town_object.write(json.dumps(
        town_object_d, ensure_ascii=False, indent=4))
    out_town.write(json.dumps(town_d, ensure_ascii=False, indent=4))

    village_object_d = OrderedDict()
    village_d = OrderedDict()

    for c in village_json:
        parent_id = c['id'][0:9] + '000'
        obj = {
            "city": town_object_d[parent_id]['name'],
            "name": c['name'],
            "id": c['id']
        }
        village_object_d[c['id']] = obj
        village_d.setdefault(parent_id, []).append(obj)

    out_village_object = codecs.open('json/village_object.json', 'w', 'utf-8')
    out_village = codecs.open('json/village.json', 'w', 'utf-8')
    out_village_object.write(json.dumps(
        village_object_d, ensure_ascii=False, indent=4))
    out_village.write(json.dumps(village_d, ensure_ascii=False, indent=4))


def main():
    pull_data()
    # make_data()


if __name__ == '__main__':
    # print("please call main")
    main()
