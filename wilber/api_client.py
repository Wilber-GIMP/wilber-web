import requests

class WilberAPIClient(object):
    URL = 'http://127.0.0.1:8000'
    def __init__(self):
        self.token = None

    def headers(self):
        if self.token:
            return {'Authorization': 'Token %s' % self.token}
        return {}

    def request_get(self, uri):
        return requests.get(uri, headers=self.headers()).json()

    def request_post(self, url, data={}, headers={}):
        response = requests.post(url, data=data, headers=headers)
        print(response)
        return response.json()



    #API CREATE USER
    def create_user(self, username, password1, password2, email):
        url = self.URL + '/rest-auth/registration/'
        data = {'username': username,
            'password1': password1,
            'password2': password2,
            'email': email
            }
        response = self.request_post(url, data)
        print(response)
        return response

    #API LOGIN
    def login(self, username, password):
        url = self.URL+'/rest-auth/login/?format=json'
        data = {'username':username, 'password':password}

        response = self.request_post(url, data)
        if 'key' in response:
            self.token = response['key']
            return self.token
        else:
            print(r)

    #API GET ASSETS
    def get_assets(self, type=None):
        url = self.URL + '/api/assets/?format=json'
        if type:
            url += "&type=%s" % type
        return self.request_get(url)

    def put_asset(self, name, type, desc, image, file):
        url = self.URL + '/api/assets/'
        data = {'name':name,
            'description':desc,
            'type':type,
            }
        files = {
            'image':open(image, 'rb'),
            'file':open(file, 'rb'),
        }

        response = requests.post(url, data=data, files=files, headers=self.headers())
        print(response.content)
        return response



if __name__ == '__main__':
    client = WilberAPIClient()

    #client.create_user('test_user', 'test_pass888', 'test_pass888', 'test_email@test.com')

    #client.login('test_user', 'test_pass888')

    #print(client.get_assets())
    print(client.get_assets(type='pattern'))
    client.login('test_user', 'test_pass888')
    #client.put_asset('Name', 'pattern', 'Desc', 'IMAGE_PATH', 'FILE_PATH')
