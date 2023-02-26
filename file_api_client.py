import requests

class FileApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def list_files(self, dir_path='/'):
        url = self.base_url + '/api/list-files'
        params = {'dir': dir_path}
        response = requests.get(url, params=params)
        if response.ok:
            return response.json()['files']
        else:
            raise Exception('Failed to list files')

    def upload_file(self, file_path, dir_path='/'):
        url = self.base_url + '/api/upload'
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'dir': dir_path}
            response = requests.post(url, files=files, data=data)
        if not response.ok:
            raise Exception('Failed to upload file')

    def create_folder(self, folder_name, dir_path='/'):
        url = self.base_url + '/api/create-folder'
        data = {'name': folder_name, 'dir': dir_path}
        response = requests.post(url, data=data)
        if not response.ok:
            raise Exception('Failed to create folder')

    def download_file(self, filename, output_dir='.', dir_path='/'):
        url = self.base_url + '/api/download/' + filename
        params = {'dir': dir_path}
        response = requests.get(url, params=params)
        if response.ok:
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'wb') as f:
                f.write(response.content)
        else:
            raise Exception('Failed to download file')

    def delete_file(self, filename):
        url = self.base_url + '/api/delete/' + filename
        response = requests.delete(url)
        if not response.ok:
            raise Exception('Failed to delete file')
