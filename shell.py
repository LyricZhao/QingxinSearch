import logging

from sqldb import SQLDB
from importer import Importer

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s: [%(levelname)s] %(message)s')
db = SQLDB('./qingxin.db', False)
# importer = Importer(db)
# importer.from_dir('collection', True)
db.search_init()

if __name__ == "__main__":
    while True:
        cmd = input('Qingxin Shell: ')
        if cmd == 'exit':
            db.flush()
            break
        try:
            cmd, arg = cmd.split()
        except:
            pass
        else:
            if cmd == 'search':
                db.search(arg)
            elif cmd == 'fromd':
                importer.from_dir(arg, False)
            elif cmd == 'fromdm':
                importer.from_dir(arg, True)
            db.commit(False)
        