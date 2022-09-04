import requests


base_url = 'http://127.0.0.1:8001'

for test_sent in [
    '国务院关税税则委员会按程序决定，对相关商品延长排除期限。',
    '省级住房和城乡建设、水利、财政部门应建立对示范城市的日常跟踪及监督检查机制',
    '省级财政部门应建立对示范城市的日常跟踪及监督检查机制',
    '公安部门依法打击利用黑客手段提供有偿“刷课”服务违法犯罪活动',
    '公安部门依法打击利用黑客手段的违法犯罪活动',
    # '他们的审核结论，主要依据长丰街道办审核的情况作出。一般情况下，街道办社会事务办初审后，',
    # '跟着日本人混不靠谱，而国军又投不得也就只能投八路了。结合以上的三点原因，谢宝庆不投都不行了，',
]:
    print('Sentence', test_sent)

    x = requests.post(base_url + '/segment', json={'sentence': test_sent})
    print('TASK1: SEG', x.json())

    x = requests.post(base_url + '/ner', json={'sentence': test_sent})
    print('TASK2: NER', x.json())

    x = requests.post(base_url + '/dep', json={'sentence': test_sent})
    print('TASK3: DEP', x.json())

    print('-'*50)
