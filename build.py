from lib import *
from lib.utils import * # target to remove this.
import datetime


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
            [id if oly['official'] else None for id, oly in olympiads.items()]
        )
    )
    all_olympiads = list(
        filter(lambda x: x is not None,
            [id for id, oly in olympiads.items()]
        )
    )

    fame = {}
    all_fame = {}
    for member_id, data in members.items():
        fame[member_id] = {
            'gold': 0,
            'silver': 0,
            'bronze': 0,
            'hm': 0,
            None: 0,
        }
        all_fame[member_id] = {
            'gold': 0,
            'silver': 0,
            'bronze': 0,
            'hm': 0,
            None: 0,
        }

        for participation in data['participations']:
            if participation['olympiad'] in official_olympiads:
                fame[member_id][participation['award']] += 1
            all_fame[member_id][participation['award']] += 1

    # list of people who got an award in an official olympiad, sorted lexicographically on awards.
    fame = sorted(
        filter(lambda person: person[1]['gold'] + person[1]['silver'] + person[1]['bronze'] + person[1]['hm'] > 0,
            fame.items()
        ),
        key=lambda person: (-person[1]['gold'], -person[1]['silver'], -person[1]['bronze'], -person[1]['hm'])
    )

    all_fame = sorted(
        filter(lambda person: person[1]['gold'] + person[1]['silver'] + person[1]['bronze'] + person[1]['hm'] > 0,
            all_fame.items()
        ),
        key=lambda person: (-person[1]['gold'], -person[1]['silver'], -person[1]['bronze'], -person[1]['hm'])
    )

    hof = []
    all_hof = []
    for member_id, stats in fame:
        hof.append({
            'id': member_id,
            'arname': members[member_id]['arname'],
            'enname': members[member_id]['enname'],
            'gold': stats['gold'],
            'silver': stats['silver'],
            'bronze': stats['bronze'],
            'hm': stats['hm'],
        })
    for member_id, stats in all_fame:
        all_hof.append({
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
        'hof': hof,
        'all_hof': all_hof
    })

    write_file('en/hall-of-fame.html', {
        'layout': 'halloffame',
        'lang': 'en',
        'title': translations['en']['hall_of_fame'],
        'hof': hof,
        'all_hof': all_hof
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
        'title': translations['ar']['images'],
        'images': images
    })
    write_file('en/images.html', {
        'layout': 'images',
        'lang': 'en',
        'title': translations['en']['images'],
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
            'participations': member['participations'],
            'exams': member['exams']
        })

def build_members_index():
    #constants = load_json('constants')
    levels = {1: [], 2: [], 3: [], 4: []}
    for member in members.values():
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
            'website': participation['website'],
            'online': participation['online'] if 'online' in participation else False
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
            'website': participation['website'],
            'online': participation['online'] if 'online' in participation else False
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

def build_tst_index():
    tsts = load_json('tsts')
    exams = load_json('exams')


    

    arname = {}
    enname = {}

    mn_year = 10000; mx_year = 0
    for year, tst in tsts.items():
        mn_year = min(mn_year, int(year))
        mx_year = max(mx_year, int(year))
        ar_exam_names = {}
        en_exam_names = {}
        tsts = {}
        for oly in list(tst.keys()):
            if oly[0] == '_':
                continue
            
            lists = {}

            tsts[oly] = {
                'exams': tst[oly]['exams'],
                'participants_count': olympiads[oly]['participants_count'],
                'lists': None,
            }

            exam_index = 0
            for eid in tst[oly]['exams']:
                exam_index += 1
                if eid not in exams:
                    continue
                ar_exam_names[eid] = exams[eid]['arname']
                en_exam_names[eid] = exams[eid]['enname']
                for uid, res in exams[eid]['participants'].items():
                    if uid in members:
                        # if members[uid]['level'] < 0:
                        #     continue
                        arname[uid] = members[uid]['arname']
                        enname[uid] = members[uid]['enname']
                    else:
                        print(f"Warning: {uid} doesn't exist in the database, but exists in {eid}")
                        continue
                        # arname[uid] = uid
                        # enname[uid] = uid
                    if uid not in lists:
                        lists[uid] = [0]*(len(tst[oly]['exams'])+1)
                    lists[uid][0] += sum(res)
                    lists[uid][exam_index] = sum(res)

            if 'female_only' in tst[oly] and tst[oly]['female_only'] == True:
                to_be_removed = []
                for uid in lists:
                    if uid not in members or 'female' not in members[uid] or members[uid]['female'] == False:
                        to_be_removed.append(uid)
                for uid in to_be_removed:
                    del lists[uid]

            if 'min_graduation' in tst[oly]:
                to_be_removed = []
                for uid in lists:
                    if uid not in members or 'graduation' not in members[uid]:
                        to_be_removed.append(uid)
                        continue
                    if members[uid]['graduation'] == None:
                        print(f"Warning: {uid} doesn't have graduation year")
                        to_be_removed.append(uid)
                        continue
                    if members[uid]['graduation'] == None or members[uid]['graduation'] < tst[oly]['min_graduation']:
                        to_be_removed.append(uid)
                for uid in to_be_removed:
                    del lists[uid]

            if 'execluded' in tst[oly]:
                for uid in tst[oly]['execluded']:
                    if uid in lists:
                        del lists[uid]
            if '_general_execluded' in tst:
                for uid in tst['_general_execluded']:
                    if uid in lists:
                        del lists[uid]
            lists = dict(sorted(lists.items(), key=lambda person: (-person[1][0])))

            tsts[oly]['lists'] = lists
        
        write_file(f'./tst/{year}.html', {
            'lang': 'ar',
            'layout': 'tst',
            'year': year,
            'title': translations['ar']['team_selection_tests'] + f' {year}',
            'olympiads': tsts,
            'names': arname,
            'exam_names': ar_exam_names
        })
        write_file(f'en/tst/{year}.html', {
            'lang': 'en',
            'layout': 'tst',
            'year': year,
            'title': translations['en']['team_selection_tests'] + f' {year}',
            'olympiads': tsts,
            'names': enname,
            'exam_names': en_exam_names
        })

    write_text('./root/_data/tst.yml', format_yml({
        'min_year': mn_year,
        'max_year': mx_year
    }))
    write_file('tst/index.html', {
        'lang': 'ar',
        'title': translations['ar']['team_selection_tests'],
        'layout': 'tstindex',
        'min_year': mn_year,
        'max_year': mx_year,
    })
    write_file('en/tst/index.html', {
        'lang': 'en',
        'title': translations['en']['team_selection_tests'],
        'layout': 'tstindex',
        'min_year': mn_year,
        'max_year': mx_year,
    })

def build_exams():
    exams = load_json('exams')
    for eid, exam in exams.items():
        arnames = {}; ennames = {}; sums = {}
        for uid, res in exam['participants'].items():
            if uid in members:
                arnames[uid] = members[uid]['arname']
                ennames[uid] = members[uid]['enname']
            else:
                arnames[uid] = ennames[uid] = str(uid)
                print(f"Warning: {uid} written on exams.json but doesn't exist in members.json")
            sums[uid] = sum(res)
        exam['participants'] = dict(sorted(exam['participants'].items(), key=lambda person: (-sum(person[1]))))
        write_file(f'exams/{eid}.html', {
            'lang': 'ar',
            'title': exam['name'],
            'layout': 'exam',
            'exam': exam,
            'names': arnames,
            'sums': sums
        })
        write_file(f'en/exams/{eid}.html', {
            'lang': 'en',
            'title': exam['name'],
            'layout': 'exam',
            'exam': exam,
            'names': ennames,
            'sums': sums
        })

import subprocess
def build_data_vairables():
    write_text('./root/_data/build.yml', format_yml({
        'last_update': datetime.datetime.now().strftime('%Y/%-m/%-d %-H:%-M:%-S'),
        'commit_index': subprocess.getoutput('git rev-list --count main'),
        'commit_id': subprocess.getoutput('git log --format="%H" -n 1'),
        'jekyll_version': subprocess.getoutput('bundle exec jekyll --version')
    }))

def main():
    test_utils()

    build_data_vairables()
    print("Built _data/build.yml")

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

    build_tst_index()
    print("Built TST index")

    build_exams()
    print("Built exams")

if __name__ == '__main__':
    main()
