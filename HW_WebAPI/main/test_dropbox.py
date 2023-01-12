from requests import post
from json import dumps


class TestDropBox:
    def __init__(self, access_token, file_to_upload, relative_path_to_file):
        self.access_token = access_token
        self.file_to_upload = file_to_upload
        self.relative_path_to_file = relative_path_to_file

    def file_upload(self):
        url = 'https://content.dropboxapi.com/2/files/upload'
        headers = {'Authorization': f'Bearer {self.access_token}',
                   'Dropbox-API-Arg': dumps({'mode': 'add',
                                             'autorename': True,
                                             'mute': False,
                                             'strict_conflict': False,
                                             'path': f'/{self.file_to_upload}'}),
                   'Content-Type': 'application/octet-stream'}
        with open(self.relative_path_to_file, 'rb') as file:
            data_file = file.read()
            return post(url=url, headers=headers, data=data_file)

    def file_get_metadata(self):
        url = 'https://api.dropboxapi.com/2/files/alpha/get_metadata'
        headers = {'Authorization': f'Bearer {self.access_token}',
                   'Content-Type': 'application/json'}
        data = dumps({'path': f'/{self.file_to_upload}'})
        return post(url=url, headers=headers, data=data)

    def file_delete(self):
        url = 'https://api.dropboxapi.com/2/files/delete'
        headers = {'Authorization': f'Bearer {self.access_token}',
                   'Content-Type': 'application/json'}
        data = dumps({'path': f'/{self.file_to_upload}'})
        return post(url, headers=headers, data=data)
