import base_sync
import paramiko
import logging
import os

class RemoteSync(base_sync.BaseSync):

    def __init__(self, master_fbs_path, address, path, username, password):
        self.master_fbs_path = master_fbs_path
        self.address = address
        self.path = path
        self.username = username
        self.password = password

    def wipe(self):
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.address, 22, self.username, self.password) # use port 22 for ssh
            # delete fbs folder
            command = 'rm -rf ' + self.path
            client.exec_command(command)
            # create empty fbs folder
            command = 'mkdir ' + self.path
            client.exec_command(command)

            client.close()

        except Exception as e:
            logging.warning(e)
            try:
                client.close()
            except:
                pass

    def synchronize(self):
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.address, 22, self.username, self.password) # use port 22 for ssh
            
            t = paramiko.Transport((self.address, 22))
            t.connect(
                username=self.username,
                password=self.password
            )
            
            sftp = paramiko.SFTPClient.from_transport(t)

            # get list of local fbs
            scanned_fbs = self.scantree(self.master_fbs_path)
            
            for fb in scanned_fbs:
                correct_path = fb.path.replace('\\', '/')
                dest_path = self.path + correct_path.replace(self.master_fbs_path, '')
                try:
                    dest_fb_stats = sftp.stat(dest_path)
                except FileNotFoundError:
                    # file does not exist on remote
                    self.force_put(sftp, correct_path, dest_path, self.path)
                else: 
                    if fb.stat().st_mtime > dest_fb_stats.st_mtime:
                        # local file is updated
                        sftp.put(correct_path, dest_path)

            client.close()
            t.close()

        except Exception as e:
            logging.warning(e)
            try:
                client.close()
                t.close()
            except:
                pass

    def scantree(self, path):
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from self.scantree(entry.path)
            else:
                yield entry

    def force_put(self, sftp, src, trgt, origin_path):
        # puts file and creates unexisting directories in its path
        try:
            sftp.put(src, trgt)
        except FileNotFoundError:
            dirs = trgt.replace(origin_path, '')
            dirs_list = dirs.split('/')
            extension = ''

            # attempts to create each parent directory of file
            for index, dir in enumerate(dirs_list):
                if index == len(dirs_list) - 1:
                    # last path element is not a dir
                    break

                extension += '/' + dir
                new_dir = origin_path + extension

                try:
                    sftp.mkdir(new_dir)
                except IOError:
                    # directory already exists
                    pass
                
        sftp.put(src, trgt)


    