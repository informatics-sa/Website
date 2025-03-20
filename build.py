from lib import *
from lib.utils import * # target to remove this.


countries = get_countries()
members = get_members()
olympiads = get_olympiads()
participations = get_participations() # TODO: make get_participations function to resolve the mess in the function
translations = load_json('translations')


def build_contact():
    contact = load_json('contact')
    realcontact = {
        'maintainers': [],
        'developers': [],
        'admins': [],
    }

    for member_id in contact['maintainers']:
        person = {
            'id': member_id,
            'arname': members[member_id]['arname'],
            'enname': members[member_id]['enname'],
            'email': members[member_id]['email']
        }
        realcontact['maintainers'].append(person)

    for member_id in contact['developers']:
        person = {
            'id': member_id,
            'arname': members[member_id]['arname'],
            'enname': members[member_id]['enname'],
            'email': members[member_id]['email']
        }
        realcontact['developers'].append(person)

    for member_id in contact['admins']:
        person = {
            'id': member_id,
            'arname': members[member_id]['arname'],
            'enname': members[member_id]['enname'],
            'email': members[member_id]['email']
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

def build_hall_of_fame():
    official_olympiads = list(
        filter(lambda x: x is not None,
            map(lambda id, oly: id if oly['official'] else None, olympiads.items())
        )
    )

    fame = {}
    for member_id, data in members.items():
        fame[member_id] = {
            'gold': 0,
            'silver': 0,
            'bronze': 0,
            'hm': 0,
            None: 0,
        }

        for participation in data['participations']:
            if participation['olympiad'] in official_olympiads:
                fame[memid][part['award']] += 1

    # list of people who got an award in an official olympiad, sorted lexicographically on awards.
    fame = sorted(
        filter(lambda _, stats: stats['gold'] + stats['silver'] + stats['bronze'] + stats['hm'] > 0,
            fame.items()
        )
        key=lambda _, stats: (-stats['gold'], -stats['silver'], -stats['bronze'], -stats['hm'])
    )

    hall_of_fame = []
    for member_id, stats in fame:
        hall_of_fame.append({
            'id': member_id,
            'arname': members[member_id]['arname'],
            'enname': members[member_id]['enname'],
            'gold': stats['gold'],
            'silver': stats['silver'],
            'bronze': stats['bronze'],
            'hm': stats['hm'],
        })

    write_file('./hall-of-fame.html', {
        'layout': 'halloffame',
        'lang': 'ar',
        'title': translations['ar']['hall_of_fame'],
        'list': hall_of_fame,
    })

    write_file('en/hall-of-fame.html', {
        'layout': 'halloffame',
        'lang': 'en',
        'title': translations['en']['hall_of_fame'],
        'list': hall_of_fame,
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

    for olympiad in olympiads.values():
        stats['gold'] += olympiad['gold']
        stats['silver'] += olympiad['silver']
        stats['bronze'] += olympiad['bronze']
        stats['hm'] += olympiad['hm']
        stats['participations'] += olympiad['participations']

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

def build_images():
    images = load_json('images')

    write_file('./images.html', {
        'layout': 'images',
        'lang': 'ar',
        'title' translations['ar']['images'],
        'images': images
    })
    write_file('en/images.html', {
        'layout': 'images',
        'lang': 'en',
        'title' translations['en']['images'],
        'images': images
    })

def build_members():
    for member_id, member in members.items():
        write_file(f'members/{member_id}.html', {
            'layout': 'person',
            'lang': 'ar',
            'title': member['arname'],
            'full_name': member['arname'],
            'graduation': member['graduation'],
            'codeforces': member['codeforces'],
            'participations': member['participations']
        })

        write_file(f'en/members/{member_id}.html', {
            'layout': 'person',
            'lang': 'en',
            'title': member['enname'],
            'full_name': member['enname'],
            'graduation': member['graduation'],
            'codeforces': member['codeforces'],
            'participations': member['participations']
        })

def build_members_index():
    #constants = load_json('constants')
    levels = {1: [], 2: [], 3: [], 4: []}
    for member in members.value():
        if 1 <= member['level'] <= 4:
            levels[member['level']].append(member)

    write_file("./members/index.html", {
        'layout': 'members',
        'lang': 'ar',
        'title': translations['ar']['members_list'],
        'levels': levels
    })
    write_file("en/members/index.html", {
        'layout': 'members',
        'lang': 'en',
        'title': translations['en']['members_list'],
        'levels': levels
    } )

def build_olympiads():
    write_file('./olympiads.html', {
        'layout': 'olympiads',
        'lang': 'ar',
        'title': translations['ar']['olympiads'],
        'olympiads': list(olympiads.values())
    })
    write_file('en/olympiads.html', {
        'layout': 'olympiads',
        'lang': 'en',
        'title': translations['en']['olympiads'],
        'olympiads': list(olympiads.values())
    })

def build_participations():
    for participation in participations:
        filename = f"{participation['name']}_{participation['year']}"
        write_file(f'participations/{filename}.html', {
            'layout': 'participation',
            'lang': 'ar',
            'title': f"{participation['name'].upper()} {participation['year']}",
            'olympiad': participation['name'],
            'olympiad_arname': participation['arname'],
            'start_date': participation['start'],
            'end_date': participation['end'],
            'country_arname': participation['country_arname'],
            'country_enname': participation['country_enname'],
            'participants': participation['ar_participants'],
            'website': participation['website']
        })
        write_file(f'en/participations/{filename}.html', {
            'layout': 'participation',
            'lang': 'en',
            'title': f"{participation['name'].upper()} {participation['year']}",
            'olympiad': participation['name'],
            'olympiad_enname': participation['enname'],
            'start_date': participation['start'],
            'end_date': participation['end'],
            'country_arname': participation['country_arname'],
            'country_enname': participation['country_enname'],
            'participants': participation['en_participants'],
            'website': participation['website']
        })

def build_participations_index():
    olympiads = {}
    min_year = 3000
    max_year = 2000
    for participation in participations:
        year = participation['year']
        min_year = min(year, min_year)
        max_year = max(year, max_year)
        if year not in olympiads:
            olympiads[year] = []

        olympiads[year].append(participation)

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


def main():
    test_utils()

    build_contact()
    print("Built contact")

    build_hall_of_fame()
    print("Built hall of fame")

    build_home()
    print("Built home")

    build_images()
    print("Built participations index")

    build_members()
    print("Built members")

    build_members_index()
    print("Built members index")

    build_olympiads()
    print("Built olympiads")

    build_participations()
    print("Built participations")

    build_participations_index()
    print("Built participations index")


    #build_tst_index()
    #print("Built TST index")

if __name__ == '__main__':
    main()
