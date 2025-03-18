from lib import *
from lib.utils import * # target to remove this.

countries = get_countries()
members = get_members()
olympiads = get_olympiads()
participations = get_participations() # TODO: make get_participations function to resolve the mess in the function
translations = load_json('translations')


def build_participations():
    for oly in participations:
        filename = oly['name'] + '_' + oly['start'].split('/')[0]
        write_file(f'participations/{filename}.html', {
            'layout': 'participation',
            'lang': 'ar',
            'title': oly['name'].upper() + ' ' + oly['start'].split('/')[0],
            'olympiad': oly['name'],
            'olympiad_arname': oly['arname'],
            'start_date': oly['start'],
            'end_date': oly['end'],
            'country_arname': oly['country_arname'],
            'country_enname': oly['country_enname'],
            'participants': oly['ar_participants'],
            'website': oly['website']
        })
        write_file(f'en/participations/{filename}.html', {
            'layout': 'participation',
            'lang': 'en',
            'title': oly['name'].upper() + ' ' + oly['start'].split('/')[0],
            'olympiad': oly['name'],
            'olympiad_enname': oly['enname'],
            'country_arname': oly['country_arname'],
            'country_enname': oly['country_enname'],
            'start_date': oly['start'],
            'end_date': oly['end'],
            'participants': oly['en_participants'],
            'website': oly['website']
        })

def build_members():
    for memid, mem in members.items():
        write_file(f'members/{memid}.html', {
            'layout': 'person',
            'lang': 'ar',
            'title': mem['arname'],
            'full_name': mem['arname'],
            'graduation': mem['graduation'],
            'codeforces': mem['codeforces'],
            'participations': mem['participations']
        })
        write_file(f'en/members/{memid}.html', {
            'layout': 'person',
            'lang': 'en',
            'title': mem['enname'],
            'full_name': mem['enname'],
            'graduation': mem['graduation'],
            'codeforces': mem['codeforces'],
            'participations': mem['participations']
        })

def build_participations_index():
    global participations
    olympiads = {}
    min_year = 3000
    max_year = 2000
    for oly in participations:
        year = oly['year']
        min_year = min(int(year), min_year)
        max_year = max(int(year), max_year)
        if oly['year'] not in olympiads:
            olympiads[year] = []

        olympiads[year].append(oly)

    written = {
        'layout': 'participations',
        'lang': 'ar',
        'title': translations['ar']['participations'],
        'start_year': min_year,
        'last_year': max_year
    }

    for year, list in olympiads.items():
        written[year] = list
    
    write_file("participations/index.html", written)

    written['lang'] = 'en'
    written['title'] = translations['en']['participations']

    write_file("en/participations/index.html", written)

def build_hall_of_fame():
    official_olympiads = []
    for id, oly in olympiads.items():
        if oly['official']:
            official_olympiads.append(id)
    fame = {}
    for memid, data in members.items():
        fame[memid] = {
            'gold': 0,
            'silver': 0,
            'bronze': 0,
            'hm': 0,
            None: 0,
        }
        for part in data['participations']:
            if part['olympiad'] in official_olympiads:
                fame[memid][part['award']] += 1
    
    filtered_fame = filter(lambda dic: dic[1]['gold'] + dic[1]['silver'] + dic[1]['bronze'] + dic[1]['hm'] > 0, fame.items())
    sorted_fame = sorted(filtered_fame, key=lambda x: (-x[1]['gold'], -x[1]['silver'], -x[1]['bronze'], -x[1]['hm']))

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
            'hm': dic['hm'],
        })
    
    write_file('./hall-of-fame.html', {
        'layout': 'halloffame',
        'lang': 'ar',
        'title': translations['ar']['hall_of_fame'],
        'list': written,
    })

    write_file('en/hall-of-fame.html', {
        'layout': 'halloffame',
        'lang': 'en',
        'title': translations['en']['hall_of_fame'],
        'list': written,
    })

def build_images():
    imgs = load_json('images')
    count = len(imgs)
    written = {
        'layout': 'images',
        'title': translations['ar']['images'],
        'lang': 'ar',
        'count': count
    }
    idx = 1
    for img in imgs:
        written[idx] = img
        idx += 1
    write_file('./images.html', written)
    written['lang'] = 'en'
    written['title'] = translations['en']['images']
    write_file('en/images.html', written)

def build_contact():
    contact = load_json('contact')
    realcontact = {
        'maintainers': [],
        'developers': [],
        'admins': [],
    }
    for mem in contact['maintainers']:
        person = {
            'id': members[mem]['id'],
            'arname': members[mem]['arname'],
            'enname': members[mem]['enname'],
            'email': members[mem]['email']
        }
        realcontact['maintainers'].append(person)

    for mem in contact['developers']:
        person = {
            'id': members[mem]['id'],
            'arname': members[mem]['arname'],
            'enname': members[mem]['enname'],
            'email': members[mem]['email']
        }
        realcontact['developers'].append(person)

    for mem in contact['admins']:
        person = {
            'id': members[mem]['id'],
            'arname': members[mem]['arname'],
            'enname': members[mem]['enname'],
            'email': members[mem]['email']
        }
        realcontact['admins'].append(person)

    written = {
        'layout': 'contact',
        'lang': 'ar',
        'title': translations['ar']['contact'],
        'maintainers': realcontact['maintainers'],
        'admins': realcontact['admins'],
        'developers': realcontact['developers']
    }
    write_file('./contact.html', written)
    written['lang'] = 'en'
    written['title'] = translations['en']['contact']
    write_file('en/contact.html', written)


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

def build_members_index():
    #constants = load_json('constants')
    members_list = members.values()
    levels = {1: [], 2: [], 3: [], 4: []}
    for mem in members_list:
        mem['participations_count'] = len(mem['participations'])
        if 1 <= mem['level'] <= 4:
            levels[mem['level']].append(mem)

    data = {
        'lang': 'ar',
        'title': translations['ar']['members_list'],
        'layout': 'members',
        'levels': levels
    }
    write_file("./members/index.html", data)
    data['lang'] = 'en'
    data['title'] = translations['en']['members_list']
    write_file("en/members/index.html", data)

def build_olympiads():
    write_file('./olympiads.html', {
        'title': translations['ar']['olympiads'],
        'layout': 'olympiads',
        'lang': 'ar',
        'olympiads': list(olympiads.values())
    })
    write_file('en/olympiads.html', {
        'title': translations['en']['olympiads'],
        'layout': 'olympiads',
        'lang': 'en',
        'olympiads': list(olympiads.values())
    })

def build_home():
    # Needs a discussion about official/nonofficial
    stats = {
        'gold': 0,
        'silver': 0,
        'bronze': 0,
        'hm': 0,
        'participations': 0,
        #'distinct_participants': 0,
        #'current_members': 0,
        #'historic_members': 0,
        #'trainers': 0,
        #'historic_camps': 0,
    }
    for oly in olympiads:
        stats['gold'] += oly['gold']
        stats['silver'] += oly['silver']
        stats['bronze'] += oly['bronze']
        stats['hm'] += oly['hm']
        stats['participations'] += oly['participations']

    write_file('./index.html', {
        'title': translations['ar']['website_name'],
        'description': translations['ar']['website_description'],
        'id': 'home',
        'lang': 'ar',
        'layout': 'home',
        'stats': stats
    })
    write_file('en/index.html', {
        'title': translations['en']['website_name'],
        'description': translations['en']['website_description'],
        'id': 'home',
        'lang': 'en',
        'layout': 'home',
        'stats': stats
    })

def main():
    test_utils()

    build_members()
    print("Built members")

    build_participations()
    print("Built participations")

    build_participations_index()
    print("Built participations index")

    build_hall_of_fame()
    print("Built hall of fame")

    build_images()
    print("Built participations index")

    build_olympiads()
    print("Built olympiads")

    build_members_index()
    print("Built members index")

    build_contact()
    print("Built contact")

    build_home()
    print("Built home")

    #build_tst_index()
    #print("Built TST index")

if __name__ == '__main__':
    main()
