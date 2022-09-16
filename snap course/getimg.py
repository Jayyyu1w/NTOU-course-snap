import os
import requests
os.chdir(os.path.dirname(__file__))
os.makedirs('./img/',exist_ok=True)
url="https://ais.ntou.edu.tw/pic.aspx?TYPE=PWD"
for i in range(0,300):
    r=requests.get(url,verify=False)
    with open(f'./img/pic{i}.jpg','wb') as f:
        f.write(r.content)