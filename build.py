#!/bin/python

import os
import json

def load_json(filename):
    with open(f'data/{filename}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

countries = {}
def init_countries():
    cj = load_json('countries')
    for country in cj:
        countries[country['alpha2_code'].lower()] = country
    countries['online'] = {}
    countries['online']['arabic_name'] = 'عن بعد'
    countries['online']['english_name'] = 'Online'

def flag_emoji(country_code):
    if country_code == 'online':
        return '🌐'
    if country_code in ['se']: # Blocked flags list
        return ''
    country_code = country_code.upper()
    flag = chr(ord(country_code[0]) + 127397) + chr(ord(country_code[1]) + 127397)
    return flag

def award_emoji(award, dashing_none=False):
    if award == 'gold':
        return '🥇'
    if award == 'silver':
        return '🥈'
    if award == 'bronze':
        return '🥉'
    if award == 'hounarablemention':
        return '📜'
    return '-' if dashing_none else ''

members = {}
members_j = load_json('people')
participations = load_json('participations')
olympiads_j = load_json('olympiads')
olympiads = {}

def init_members():
    global members
    for mem in members_j:
        members[mem['id']] = mem
        members[mem['id']]['participations'] = {}

    for oly in participations:
        #print(oly['participants'])
        for mem_id in oly['participants']:
            if mem_id not in members:
                members[mem_id] = {}
                members[mem_id]['participations'] = {}
                members[mem_id]['arname'] = mem_id
                members[mem_id]['enname'] = mem_id
                members[mem_id]['graduation'] = None
                members[mem_id]['codeforces'] = None
            members[mem_id]['participations'][oly['name'] + '_' + oly['start'].split('/')[0]] = oly['participants'][mem_id]

def init_olympiads():
    for oly in olympiads_j:
        olympiads[oly['id']] = oly

def write_yml(data: dict, indent: int = 0) -> str:
    res = ""
    for key, val in data.items():
        if type(val) is dict:
            res += " " * indent + str(key) + ":\n"
            res += write_yml(val, indent + 2)
        elif type(val) is list:
            res += " " * indent + str(key) + ":\n"
            res += " " * (indent+2) + f"count: {len(val)}\n"
            for i in range(len(val)):
                mp = {str(i+1): val[i]}
                res += write_yml(mp, indent + 2)
        elif val is None:
            res += " " * indent + str(key) + ": null\n"
        else:
            res += " " * indent + str(key) + ": \"" + str(val) + "\"\n"
    return res


def write_file(filename: str, vals: dict):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write(write_yml(vals))
        f.write("---\n")

def build_olympiads():
    for oly in participations:
        oly['country_arname'] = countries[oly['country']]['arabic_name'] + ' ' + flag_emoji(oly['country'])
        oly['country_enname'] = countries[oly['country']]['english_name'] + ' ' + flag_emoji(oly['country'])

        oly['arname'] = olympiads[oly['name']]['arname']
        oly['enname'] = olympiads[oly['name']]['enname']

        filename = oly['name'] + '_' + oly['start'].split('/')[0]
        parts = []
        enparts = []
        awards = ''
        for mem_id, award in oly['participants'].items():
            parts.append({'id': mem_id, 'name': members[mem_id]['arname'], 'award': award_emoji(award, dashing_none=True)})
            enparts.append({'id': mem_id, 'name': members[mem_id]['enname'], 'award': award_emoji(award, dashing_none=True)})
            awards += award_emoji(award)

        oly['awards'] = awards
        write_file(f'olympiads/{filename}.html', {
            'layout': 'olympiad',
            'lang': 'ar',
            'title': oly['name'].upper() + ' ' + oly['start'].split('/')[0],
            'olympiad': oly['name'],
            'olympiad_arname': oly['arname'],
            'start_date': oly['start'],
            'end_date': oly['end'],
            'country_arname': oly['country_arname'],
            'country_enname': oly['country_enname'],
            'participants': parts,
            'website': oly['website']
        })
        write_file(f'en/olympiads/{filename}.html', {
            'layout': 'olympiad',
            'lang': 'en',
            'title': oly['name'].upper() + ' ' + oly['start'].split('/')[0],
            'olympiad': oly['name'],
            'olympiad_enname': oly['enname'],
            'country_arname': oly['country_arname'],
            'country_enname': oly['country_enname'],
            'start_date': oly['start'],
            'end_date': oly['end'],
            'participants': enparts,
            'website': oly['website']
        })

def build_members():
    for memid, mem in members.items():
        participations = []
        for oly, award in mem['participations'].items():
            olymp = {}
            olymp['olympiad'] = oly.split("_")[0]
            olymp['year'] = oly.split("_")[1]
            olymp['arname'] = olympiads[olymp['olympiad']]['arname']
            olymp['enname'] = olympiads[olymp['olympiad']]['enname']
            olymp['award'] = award
            
            participations.append(olymp)

        write_file(f'members/{memid}.html', {
            'layout': 'person',
            'title': mem['arname'],
            'lang': 'ar',
            'full_name': mem['arname'],
            'graduation': mem['graduation'],
            'codeforces': mem['codeforces'],
            'participations': participations
        })
        write_file(f'en/members/{memid}.html', {
            'layout': 'person',
            'title': mem['enname'],
            'lang': 'en',
            'full_name': mem['enname'],
            'graduation': mem['graduation'],
            'codeforces': mem['codeforces'],
            'participations': participations
        })

def build_olympiads_index():
    olympiads = {}
    min_year = 3000
    max_year = 2000
    for oly in participations:
        year = oly['start'].split('/')[0]
        min_year = min(int(year), min_year)
        max_year = max(int(year), max_year)
        if year not in olympiads:
            olympiads[year] = []

        del oly["participants"]
        olympiads[year].append(oly)

    written = {
        'layout': 'participations',
        'lang': 'ar',
        'title': 'الأولمبيادات',
        'start_year': min_year,
        'last_year': max_year
    }

    for year, list in olympiads.items():
        written[year] = list
    
    write_file("olympiads/index.html", written)

    written['lang'] = 'en'
    written['title'] = 'Olympiads'

    write_file("en/olympiads/index.html", written)

# Generate a medals count list only in official olympiads 
# Sort it by gold/silver/bronze/hounarablemention
# Print the list in a table
def build_hall_of_fame():
    official_olympiads = ['ioi', 'apio']
    fame = {}
    for memid, data in members.items():
        fame[memid] = {
            'gold': 0,
            'silver': 0,
            'bronze': 0,
            'hounarablemention': 0,
            None: 0,
        }
        for oly, award in data['participations'].items():
            oly = oly.split('_')[0]
            if oly in official_olympiads:
                fame[memid][award] += 1
    
    filtered_fame = filter(lambda dic: dic[1]['gold'] + dic[1]['silver'] + dic[1]['bronze'] + dic[1]['hounarablemention'] > 0, fame.items())
    sorted_fame = sorted(filtered_fame, key=lambda x: (-x[1]['gold'], -x[1]['silver'], -x[1]['bronze'], -x[1]['hounarablemention']))
    # TODO: should be printed to a file

    written = []
    for it in sorted_fame:
        mem = it[0]
        dic = it[1]
        written.append({
            'id': mem,
            'arname': members[mem]['arname'],
            'enname': members[mem]['enname'],
            'gold': dic['gold'],
            'silver': dic['silver'],
            'bronze': dic['bronze'],
            'hounarablemention': dic['hounarablemention'],
        })
    
    write_file('./hall-of-fame.html', {
        'layout': 'halloffame',
        'lang': 'ar',
        'title': 'لائحة الشرف',
        'list': written,
    })

    write_file('en/hall-of-fame.html', {
        'layout': 'halloffame',
        'lang': 'en',
        'title': 'Fame',
        'list': written,
    })

def build_images():
    imgs = load_json('images')
    count = len(imgs)
    written = {
        'layout': 'images',
        'title': "مكتبة الصور",
        'lang': 'ar',
        'count': count
    }
    idx = 1
    for img in imgs:
        written[idx] = img
        idx += 1
    write_file('./images.html', written)
    written['lang'] = 'en'
    written['title'] = 'Image library'
    write_file('en/images.html', written)

def build_contact():
    contact = load_json('contact')
    realcontact = {
        'maintainers': [],
        'developers': [],
        'admins': [],
    }
    for mem in contact['maintainers']:
        try:
            del members[mem]['participations_count']
        except:
            ...
        try:
            del members[mem]['graduation']
        except:
            ...
        try:
            del members[mem]['codeforces']
        except:
            ...
        try:
            del members[mem]['level']
        except:
            ...
        realcontact['maintainers'].append(members[mem])
        if members[mem]['email'] == None:
            exit(1)

    for mem in contact['developers']:
        try:
            del members[mem]['participations_count']
        except:
            ...
        try:
            del members[mem]['graduation']
        except:
            ...
        try:
            del members[mem]['codeforces']
        except:
            ...
        try:
            del members[mem]['level']
        except:
            ...
        realcontact['developers'].append(members[mem])
        if members[mem]['email'] == None:
            exit(1)

    for mem in contact['admins']:
        try:
            del members[mem]['participations_count']
        except:
            ...
        try:
            del members[mem]['graduation']
        except:
            ...
        try:
            del members[mem]['codeforces']
        except:
            ...
        try:
            del members[mem]['level']
        except:
            ...
        realcontact['admins'].append(members[mem])
        if members[mem]['email'] == None:
            exit(1)

    written = {
        'layout': 'contact',
        'lang': 'ar',
        'title': 'تواصل',
        'maintainers': realcontact['maintainers'],
        'admins': realcontact['admins'],
        'developers': realcontact['developers']
    }
    write_file('./contact.html', written)
    written['lang'] = 'en'
    written['title'] = 'Contact'
    write_file('en/contact.html', written)

def build_members_index():
    members_list = members.values()
    levels = {1: [], 2: [], 3: [], 4: []}
    for mem in members_list:
        mem['participations_count'] = len(mem['participations'])
        del mem['participations']
        if 1 <= mem['level'] <= 4:
            levels[mem['level']].append(mem)

    data = {
        'lang': 'ar',
        'title': 'قائمة الأعضاء',
        'layout': 'members',
        'levels': levels
    }
    write_file("./members/index.html", data)
    data['lang'] = 'en'
    data['title'] = 'Members list'
    write_file("en/members/index.html", data)

def test_utils():
    assert flag_emoji('sa') == '🇸🇦'
    assert countries['sa']['english_name'] == 'Saudi Arabia'
    assert write_yml({
        'Hi': 'Hello',
        'list': ['Hi', 'Hello'],
        'dict': {
            'sub1': 'sub2'
        },
        'nullval': None
    }) == """Hi: "Hello"
list:
  count: 2
  1: "Hi"
  2: "Hello"
dict:
  sub1: "sub2"
nullval: null
"""

def main():
    init_countries()
    init_members()
    init_olympiads()

    test_utils()

    # Pls don't change the order
    build_members()
    build_olympiads()
    build_olympiads_index()
    build_hall_of_fame()
    build_images()
    # build_calendar()
    build_members_index() 
    build_contact()

main()