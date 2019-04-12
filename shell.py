import logging

from sqldb import SQLDB
from importer import Importer

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s: [%(levelname)s] %(message)s')
db = SQLDB('./qingxin.db', True)
importer = Importer(db)

if __name__ == "__main__":
    while True:
        cmd = input('Qingxin Shell: ')
        cmd, arg = cmd.split()
        if cmd == 'search':
            db.search(arg)
        elif cmd == 'fromd':
            importer.from_dir(arg, False)
        elif cmd == 'fromdm':
            importer.from_dir(arg, True)
        else:
            print('Invalid input.')
        db.commit(False)