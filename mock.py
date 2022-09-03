import requests

x = requests.post('http://127.0.0.1:8001/segment',
        json={'sentence': '省级住房和城乡建设、水利、财政部门应建立对示范城市的日常跟踪及监督检查机制'})

print(x.json())
