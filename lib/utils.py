import os, json

ROOT_DIR = './root'
LANGS = ['ar', 'en']
BLOCKED_FLAGS = ['se']


def award_emoji(award, dashing_none=False):
    if award == 'gold':
        return '🥇'
    if award == 'silver':
        return '🥈'
    if award == 'bronze':
        return '🥉'
    if award == 'hm':
        return '📜'
    return '-' if dashing_none else ''

def default_person(id: str):
    return {
        'id': id,
        'participations': [],
        'arname': id,
        'enname': id.replace('_', ' '), # TODO: split undersc
        'level': -4,
        'graduation': None,
        'codeforces': None
    }

def flag_emoji(country_code):
    if country_code == 'online':
        return '🌐'
    if country_code in BLOCKED_FLAGS:
        return ''
    country_code = country_code.upper()
    flag = chr(ord(country_code[0]) + 127397) + chr(ord(country_code[1]) + 127397)
    return flag

def format_yml(data: dict, indent_level: int = 0) -> str:
    res = ""
    indent = " " * indent_level

    for key, val in data.items():
        if type(val) is dict:
            res += indent + f"{str(key)}:\n"
            res += format_yml(val, indent_level + 2)
        elif type(val) is list:
            res += indent + f"{str(key)}:\n"
            res += indent + f"  count: {len(val)}\n"
            for i in range(len(val)):
                res += format_yml({i + 1: val[i]}, indent_level + 2)
        elif val is None:
            res += indent + f"{str(key)}: null\n"
        elif type(val) is bool or type(val) is int:
            res += indent + f"{str(key)}: {str(val).lower()}\n"
        else:
            res += indent + f"{str(key)}: \"{str(val)}\"\n"

    return res

def load_json(filename):
    with open(f'{ROOT_DIR}/data/{filename}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def write_text(filename: str, txt: str):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(txt)

def write_file(filename: str, data: dict):
    filename = f"{ROOT_DIR}/{filename}"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write(format_yml(data))
        f.write("---\n")

def write_page(lang: str, filename: str, data: dict):
    if lang not in LANGS:
        print(f"Invalid language '{lang}' for page: {filename}")
        exit(1)
    data['lang'] = lang
    
    if lang == LANGS[0]:
        write_file('./' + filename, data)
    else:
        write_file(lang + '/' + filename, data)

def test_utils(log: bool = True):
    assert flag_emoji('sa') == '🇸🇦'
    assert award_emoji('gold') == '🥇'
    assert format_yml({
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
    
    if log: print("Utils test passed.")
