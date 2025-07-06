from .utils import *


def get_countries():
    countries = {}
    for country in load_json('countries'):
        code = country['alpha2_code'].lower()
        country['emoji'] = flag_emoji(code)
        countries[code] = country
    return countries

def get_exams():
    exams = load_json('exams')
    # TODO: Check for duplicate exam IDs
    return exams

def get_members():
    members = {}
    for person in load_json('people'):
        person['iid'] = str(person['iid'])
        members[str(person['iid'])] = person
        members[str(person['iid'])]['participations'] = []
        members[str(person['iid'])]['exams'] = []
        if 'codeforces' not in members[str(person['iid'])]:
            members[str(person['iid'])]['codeforces'] = None
        if 'graduation' not in members[str(person['iid'])]:
            members[str(person['iid'])]['graduation'] = None

    for participation in load_json('participations'):
        for member_id in participation['participants']:
            if member_id not in members:
                print(f"[WARN ⚠️] {member_id} participant of {participation['name']} ({participation['year']}), doesn't exist in people.json")
                members[member_id] = default_person(member_id)

            members[member_id]['participations'].append({
                'olympiad': participation['name'],
                'year': str(participation['year']),
                'award': participation['participants'][member_id]
            })

    for eid, exam in get_exams().items():
        for member_id, scores in exam['participants'].items():
            members[member_id]['exams'].append(scores)
    
    return members
    
def get_olympiads():
    olympiads = {}
    for olympiad in load_json('olympiads'):
        olympiads[olympiad['id']] = olympiad
        olympiads[olympiad['id']]['gold'] = 0
        olympiads[olympiad['id']]['silver'] = 0
        olympiads[olympiad['id']]['bronze'] = 0
        olympiads[olympiad['id']]['hm'] = 0
        olympiads[olympiad['id']]['participations'] = 0

    for participation in load_json('participations'):
        olympiads[participation['name']]['participations'] += 1
        for award in participation['participants'].values():
            if award != None:
               olympiads[participation['name']][award] += 1
                
    return olympiads

def get_participations():
    participations = load_json('participations')
    olympiads = get_olympiads()
    countries = get_countries()
    members = get_members()
    for participation in participations:
        participation['country_arname'] = f"{countries[participation['country']]['arabic_name']} {flag_emoji(participation['country'])}"
        participation['country_enname'] = f"{countries[participation['country']]['english_name']} {flag_emoji(participation['country'])}"

        participation['arname'] = olympiads[participation['name']]['arname']
        participation['enname'] = olympiads[participation['name']]['enname']

        parts = []
        enparts = []
        awards = ''
        for mem_id, award in participation['participants'].items():
            parts.append({'id': mem_id, 'name': members[mem_id]['arname'], 'award': award_emoji(award, dashing_none=True)})
            enparts.append({'id': mem_id, 'name': members[mem_id]['enname'], 'award': award_emoji(award, dashing_none=True)})
            awards += award_emoji(award)
        participation['awards'] = awards
        participation['ar_participants'] = parts
        participation['en_participants'] = enparts
    return participations

