import requests

test_sent = '省级住房和城乡建设、水利、财政部门应建立对示范城市的日常跟踪及监督检查机制'
print('Sentence', test_sent)

x = requests.post('http://127.0.0.1:8001/segment', json={'sentence': test_sent})
print('segment', x.json())

x = requests.post('http://127.0.0.1:8001/ner', json={'sentence': test_sent})
print('NER', x.json())

print('-'*50)
