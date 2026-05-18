from .utils import load_secret_json
from datetime import date

__birthdays = load_secret_json('birthdays')
__birthdays = dict(map(lambda x: (x[0], date.fromisoformat(x[1])), __birthdays.items()))

def is_older(userid, date: date) -> bool:
    if userid not in __birthdays:
        print(f"[Warn ⚠️] {userid} not in birthdays while being queried.")
        return False
    return __birthdays[userid] < date

def is_younger(userid, date: date) -> bool:
    if userid not in __birthdays:
        print(f"[Warn ⚠️] {userid} not in birthdays while being queried.")
        return False
    return date < __birthdays[userid]

