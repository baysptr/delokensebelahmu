import requests

url = 'http://192.168.1.14/bagus/form_upload.php'
data = {'token':'lalskaldjlk', 'submit':'submit'}
files = {'file':('init_log.db', open('init_log.db', 'rb'))}
r = requests.post(url, data=data, files=files)

print(r.status_code)