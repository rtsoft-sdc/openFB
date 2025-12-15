import getpass
import logging
import base_sync, remote_sync, local_sync


class FBSync():

    def __init__(self, path, strategy):
        self.master_fbs_path = path
        self.strategy = strategy

    def synchronize(self, dinasore):
        if 'address' not in dinasore or \
            'dinasore-path' not in dinasore:
            logging.warning('Can\'t synchronize without dinasore path.')
            return
        
        address = dinasore.get('address')
        dinasore_path = dinasore.get('dinasore-path') + '/resources/function_blocks'

        sync_obj = None

        if address == 'localhost' or\
            address == '127.0.0.1':
            sync_obj = local_sync.LocalSync(self.master_fbs_path, dinasore_path)
        else:
            username = getpass.getuser() if 'username' not in dinasore else dinasore.get('username')
            password = None if 'password' not in dinasore else dinasore.get('password')
            sync_obj = remote_sync.RemoteSync(self.master_fbs_path, address, dinasore_path, username, password)

        strategies = self.strategy.split(' ')
        if 'wipe' in strategies:
            sync_obj.wipe()
        
        sync_obj.synchronize()

        

