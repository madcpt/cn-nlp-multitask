import requests


base_url = 'http://127.0.0.1:8001'

x = requests.get(base_url + '/article?id=1')
print('Query id=1', x.json())

x = requests.post(base_url + '/insert',
                    json={
                        'title': 'this is a title',
                        'publish_date': '2022-04-15-10:04:00',
                        'content': 'this is content',
                    })
print('data inserted with id=', x.json())

x = requests.get(base_url + '/article?id=101')
print('Query id=101', x.json())
