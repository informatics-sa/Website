from lib import *
from lib.utils import *

members = get_members()


def update_participations():
    with open('./root/data/participations.json') as f:
        parts_str = f.read()
    for uid in members:
        if 'iid' in members[uid]:
            iid = members[uid]['iid']
            parts_str = parts_str.replace(f'"{uid}"', f'"{iid}"')
    write_text('./participations.2.json', parts_str)

def update_exams():
    with open('./root/data/exams.json') as f:
        parts_str = f.read()
    for k, v in members.items():
        id = v['id']
        iid = v['iid']
        parts_str = parts_str.replace(f'"{id}"', f'"{iid}"')
    write_text('./exams.2.json', parts_str)

update_exams()
#update_participations()