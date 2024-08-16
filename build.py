import os
import json
import countryinfo

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
    if country_code in ['sw']: # Blocked flags list
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


def write_file(filename: str, vals: dict):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("---\n")
        for key, value in vals.items():
            if type(value) is dict:
                f.write(f"{key}:\n")
                for key2, value2 in value.items():
                    if type(value2) is dict:
                        f.write(f"  {key2}:\n")
                        for key3, value3 in value2.items():
                            f.write("    " + key3 + ": " + str(value3) + "\n")
                    else:
                        f.write("  " + key2 + ": " + str(value2) + "\n")
            else:
                f.write(key + ": " + str(value) + "\n")
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
            'participants': parts
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
            'participants': enparts
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
            'lang': 'ar',
            'full_name': mem['arname'],
            'graduation': mem['graduation'],
            'codeforces': mem['codeforces'],
            'participations_count': len(participations),
            'participations': participations
        })
        write_file(f'en/members/{memid}.html', {
            'layout': 'person',
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
    
    write_file("olympiads/idx.html", written)

    written['lang'] = 'en'
    written['title'] = 'Olympiads'

    write_file("en/olympiads/idx.html", written)

def main():
    init_countries()
    init_members()
    build_members()
    build_olympiads()
    build_olympiads_index()

main()