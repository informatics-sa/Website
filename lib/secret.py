from .utils import load_secret_json
from datetime import date
from pathlib import Path
import shutil

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

def prepare_secret_images():
    vendor = Path("./lib/Database/secret-image-library/vendor")
    collections = Path("./lib/Database/secret-image-library/collections")
    public_imgs_dir = Path("./root/simg")
    public_collections_dir = Path("./root/scol")

    public_imgs_dir.mkdir(parents=True, exist_ok=True)
    public_collections_dir.mkdir(parents=True, exist_ok=True)

    for file in vendor.iterdir():
        shutil.copy(str(file), public_imgs_dir)
    for file in collections.iterdir():
        shutil.copy(str(file), public_collections_dir)
