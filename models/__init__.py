#!/usr/bin/python3
"""Initialize models package"""


from models.engine.file_storage import FileStorage

# create an instance of the desired storage type
storage = FileStorage()
# load saved objects from storage
storage.reload()
