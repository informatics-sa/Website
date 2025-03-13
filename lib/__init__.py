from .utils import *

def default_person(id: str):
    return {
        'participations': {},
        'arname': id,
        'enname':  id,
        'graduation': None,
        'codeforces': None
    }

def get_countries():
    countries = {}
    for country in load_json('countries'):
        code = country['alpha2_code'].lower()
        country['emoji'] = flag_emoji(code)
        countries[code] = country

    countries['online'] = {}
    countries['online']['arabic_name'] = 'عن بعد'
    countries['online']['english_name'] = 'Online'
    countries['online']['emoji'] = flag_emoji('online')

    return countries

def get_members():
    members = {}
    for mem in load_json('people'):
        members[mem['id']] = mem
        members[mem['id']]['participations'] = {}

    for oly in load_json('participations'):
        for mem_id in oly['participants']:
            if mem_id not in members:
                print(f"[WARN ⚠️] {mem_id} participant of {oly['name']} ({oly['year']}), doesn't exist in people.json")
                members[mem_id] = default_person(mem_id)
            members[mem_id]['participations'][oly['name'] + '_' + str(oly['year'])] = oly['participants'][mem_id]

    return members
    
def get_olympiads():
    olympiads = {}
    for oly in load_json('olympiads'):
        olympiads[oly['id']] = oly
        olympiads[oly['id']]['gold'] = 0
        olympiads[oly['id']]['silver'] = 0
        olympiads[oly['id']]['bronze'] = 0
        olympiads[oly['id']]['hm'] = 0
        olympiads[oly['id']]['participations'] = 0

    for participation in load_json('participations'):
        olympiads[participation['name']]['participations'] += 1
        for award in participation['participants'].values():
            if award != None:
               olympiads[participation['name']][award] += 1
                
    return olympiads
