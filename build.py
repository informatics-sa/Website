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

def award_emoji(award):
    if award == 'gold':
        return '🥇'
    if award == 'silver':
        return '🥈'
    if award == 'bronze':
        return '🥉'
    if award == 'hounarablemention':
        return '📜'
    return ''

members = {}
members_j = load_json('people')
participations = load_json('participations')

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
                members[mem_id]['arname'] = "UNKNOWN"
                members[mem_id]['enname'] = "UNKNOWN"
                members[mem_id]['graduation'] = 0
                members[mem_id]['codeforces'] = "undefined"
            members[mem_id]['participations'][oly['name'] + '_' + oly['start'].split('/')[0]] = oly['participants'][mem_id]

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
        else:
            res += " " * indent + str(key) + ": " + str(val) + "\n"
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


        filename = oly['name'] + '_' + oly['start'].split('/')[0]
        parts = {}
        enparts = {}
        idx = 1
        awards = ''
        for mem_id, award in oly['participants'].items():
            parts[idx] = {'id': mem_id, 'name': members[mem_id]['arname'], 'award': award}
            enparts[idx] = {'id': mem_id, 'name': members[mem_id]['enname'], 'award': award}
            awards += award_emoji(award)
            idx += 1
        oly['awards'] = awards
        write_file(f'olympiads/{filename}.html', {
            'layout': 'olympiad',
            'lang': 'ar',
            'title': oly['name'].upper() + ' ' + oly['start'].split('/')[0],
            'olympiad': oly['name'],
            'start_date': oly['start'],
            'end_date': oly['end'],
            'country_arname': oly['country_arname'],
            'country_enname': oly['country_enname'],
            'participants_count': len(enparts),
            'participants': parts,
            'website': oly['website'] if 'website' in oly else None
        })
        write_file(f'en/olympiads/{filename}.html', {
            'layout': 'olympiad',
            'lang': 'en',
            'title': oly['name'].upper() + ' ' + oly['start'].split('/')[0],
            'olympiad': oly['name'],
            'country_arname': oly['country_arname'],
            'country_enname': oly['country_enname'],
            'start_date': oly['start'],
            'end_date': oly['end'],
            'participants_count': len(enparts),
            'participants': enparts,
            'website': oly['website'] if 'website' in oly else None
        })

def build_members():
    for memid, mem in members.items():
        participations = {}
        idx = 1
        for oly, award in mem['participations'].items():
            participations[idx] = {}
            participations[idx]['olympiad'] = oly
            participations[idx]['award'] = award
            idx += 1
        write_file(f'members/{memid}.html', {
            'layout': 'person',
            'title': mem['arname'],
            'lang': 'ar',
            'full_name': mem['arname'],
            'graduation': mem['graduation'],
            'codeforces': mem['codeforces'],
            'participations_count': len(participations),
            'participations': participations
        })
        write_file(f'en/members/{memid}.html', {
            'layout': 'person',
            'title': mem['enname'],
            'lang': 'en',
            'full_name': mem['enname'],
            'graduation': mem['graduation'],
            'codeforces': mem['codeforces'],
            'participations_count': len(participations),
            'participations': participations
        })

def build_olympiads_index():
    olympiads = {}
    yearidx = {}
    min_year = 3000
    max_year = 2000
    for oly in participations:
        year = oly['start'].split('/')[0]
        min_year = min(int(year), min_year)
        max_year = max(int(year), max_year)
        if year not in olympiads:
            olympiads[year] = {}
            yearidx[year] = 1

        olympiads[year][yearidx[year]] = oly
        del olympiads[year][yearidx[year]]['participants']
        yearidx[year] += 1
    
    for year in range(min_year, max_year+1):
        olympiads[str(year)]['count'] = yearidx[str(year)]-1

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
            'none': 0,
        }
        for oly, award in data['participations'].items():
            oly = oly.split('_')[0]
            if oly in official_olympiads:
                fame[memid][award] += 1
    
    sortedfame = sorted(fame.items(), key=lambda x: (-x[1]['gold'], -x[1]['silver'], -x[1]['bronze'], -x[1]['hounarablemention']))
    # TODO: should be printed to a file
    count = 0
    written = {}
    for it in sortedfame:
        mem = it[0]
        dic = it[1]
        if dic['gold'] + dic['silver'] + dic['bronze'] + dic['hounarablemention'] == 0:
            break
        count += 1
        written[count] = {
            'id': mem,
            'arname': members[mem]['arname'],
            'enname': members[mem]['enname'],
            'gold': dic['gold'],
            'silver': dic['silver'],
            'bronze': dic['bronze'],
            'hounarablemention': dic['hounarablemention'],
        }
    
    write_file('./hall-of-fame.html', {
        'layout': 'halloffame',
        'lang': 'ar',
        'title': 'لائحة الشرف',
        'list': written,
        'count': count
    })

    write_file('en/hall-of-fame.html', {
        'layout': 'halloffame',
        'lang': 'en',
        'title': 'Fame',
        'list': written,
        'count': count
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
    for mem in contact['maintainers']:
        mem['arname'] = members[mem['id']]['arname']
        mem['enname'] = members[mem['id']]['enname']
    for mem in contact['developers']:
        mem['arname'] = members[mem['id']]['arname']
        mem['enname'] = members[mem['id']]['enname']
    for mem in contact['admins']:
        mem['arname'] = members[mem['id']]['arname']
        mem['enname'] = members[mem['id']]['enname']
    written = {
        'layout': 'contact',
        'lang': 'ar',
        'title': 'تواصل',
        'maintainers': contact['maintainers'],
        'admins': contact['admins'],
        'developers': contact['developers']
    }
    write_file('./contact.html', written)
    written['lang'] = 'en'
    written['title'] = 'Contact'
    write_file('en/contact.html', written)


def test_utils():
    assert flag_emoji('sa') == '🇸🇦'
    assert countries['sa']['english_name'] == 'Saudi Arabia'
    assert write_yml({
        'Hi': 'Hello',
        'list': ['Hi', 'Hello'],
        'dict': {
            'sub1': 'sub2'
        }
    }) == """Hi: Hello
list:
  count: 2
  1: Hi
  2: Hello
dict:
  sub1: sub2
"""

def main():
    init_countries()
    init_members()

    test_utils()

    build_members()
    #build_members_index()
    build_olympiads()
    build_olympiads_index()
    build_hall_of_fame()
    build_images()
    build_contact()

main()