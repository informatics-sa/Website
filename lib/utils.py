import os, json

ROOT_DIR = './root/'
LANGS = ['ar', 'en']
BLOCKED_FLAGS = ['se']

def load_json(filename):
    with open(f'{ROOT_DIR}data/{filename}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

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

def flag_emoji(country_code):
    if country_code == 'online':
        return '🌐'
    if country_code in BLOCKED_FLAGS:
        return ''
    country_code = country_code.upper()
    flag = chr(ord(country_code[0]) + 127397) + chr(ord(country_code[1]) + 127397)
    return flag

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
        elif type(val) is bool:
            res += " " * indent + str(key) + ": " + str(val).lower() + "\n"
        elif type(val) is int:
            res += " " * indent + str(key) + ": " + str(val) + "\n"
        else:
            res += " " * indent + str(key) + ": \"" + str(val) + "\"\n"
    return res


def write_file(filename: str, vals: dict):
    filename = ROOT_DIR + filename
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write(write_yml(vals))
        f.write("---\n")
