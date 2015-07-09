#! /usr/bin/python
# -*- coding: utf-8 -*-


import json


schools_json = json.load(file('juniorschool.json'))

schools_json_new = {}
schools_json_new['version'] = schools_json['version'] 
schools_json_new['schools'] = []

for city_one in schools_json['schools']:
    city_one_new = {}
    city_one_new['id']   = city_one['id']
    city_one_new['name'] = city_one['name'].encode('utf-8')
    city_one_new['data'] = []

    for county_one in city_one['data']:
        county_one_new = {}
        county_one_new['name'] = county_one['name'].encode('utf-8')
        county_one_new['id']   = county_one['id'][-6:]
        county_one_new['schoollist'] = []

        school_cnt = 0
        for school_one in county_one['schoollist']:
            school_cnt += 1
            school_one_new = {}
            school_one_new['name'] = school_one.encode('utf-8')
            school_one_new['id']   = "%s%03d" %(county_one['id'][-6:], school_cnt)

            county_one_new['schoollist'].append(school_one_new)


        city_one_new['data'].append(county_one_new)

    schools_json_new['schools'].append(city_one_new)

json.dump(schools_json_new, file('juniorschool_new.json','w'),ensure_ascii=False)


