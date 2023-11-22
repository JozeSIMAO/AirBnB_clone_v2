#!/usr/bin/python3
"""Creates a unique FileStorage instance/engine for our application"""

from os import getenv


storage_type = getenv('HBNB_TYPE_STORAGE', 'file')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
