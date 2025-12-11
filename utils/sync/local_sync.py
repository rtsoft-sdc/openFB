import base_sync
from dirsync import syncer
import shutil
import os


class LocalSync(base_sync.BaseSync):

    def __init__(self, master_fbs_path, path):
        self.master_fbs_path = master_fbs_path
        self.path = path

    def wipe(self):
        # remove fbs folder
        shutil.rmtree(self.path)
        # create empty fbs folder
        os.mkdir(self.path)

    def synchronize(self):
        copier = syncer.Syncer(self.master_fbs_path, self.path, 'sync')
        copier.do_work()
        return set(copier._changed).union(copier._added).union(copier._deleted)

