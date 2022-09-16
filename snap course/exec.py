import os
import time
import base64
import verify as vf
import selenium.webdriver.support.ui as ui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

os.chdir(os.path.dirname(__file__))
driver = webdriver.Edge(service=Service("msedgedriver.exe"))

def find_course(course):
    try:
        driver.find_element_by_id('Q_COSID').send_keys(course)
        driver.find_element_by_id('QUERY_COSID_BTN').click()
        return True
    except Exception as ex:
        print('Error!')
        print(ex)
        print(f'error at {time.ctime()}')
        return False

def getCourse():
    f = open('course.txt','r')
    fres = open('result.txt','w')
    while True:
        c = f.readline()
        if c == "":
            break
        fres.write(f'{time.ctime()}  ')
        if not find_course(c):
            fres.write('System Error!')
            break
        suc = snapCourse()
        if suc == 1:
            fres.write(f'{c} snapped!')
        elif suc == 2:
            fres.write(f'{c} snap failed QQ')
        elif suc == 3:
            fres.write('System Error!')
            break

def alert_info():
    try:
        Alert = driver.switch_to_alert()
        text = Alert.text
        return Alert, text
    except:
        return None, 'none'

def snapCourse():
    alert_message = ['本科目設有檢查人數下限。選本課程，在未達下限人數前時無法退選，確定加選?', '年級不可加選！', '衝堂不可選！', '該課程已達人數上限']
    try:
        driver.implicitly_wait(5)
        driver.find_element_by_id('DataGrid1_ctl02_edit').click()
        time.sleep(0.5)
        alert, text = alert_info()
        if text == alert_message[0]:
            alert.accept()
            time.sleep(0.5)
            alert, text = alert_info()
            if text == alert_message[1] or text == alert_message[2]:
                alert.accept()
                return 2
            else:
                return True
        elif text == alert_message[1] or text == alert_message[2]:
            alert.accept()
            return 2
        else:
            blk_text = text.split(':')
            alert.accept()
            if(len(blk_text) > 1):
                return 2
            else:
                return 1
    except Exception as ex:
        print('Error!')
        print(ex)
        print(f'error at {time.ctime()}')
        return 3

def get_verifyimg():
    i = driver.execute_async_script("""
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var img = document.querySelector('div.row img');
    canvas.height = img.naturalHeight;
    canvas.width = img.naturalWidth;
    context.drawImage(img, 0, 0);
    
    callback = arguments[arguments.length - 1];
    callback(canvas.toDataURL());
    """)
    imgret = base64.b64decode(i.split(',')[1])
    return imgret
    '''
    # 先將 data Url 前綴 (data:image/png;base64) 去除,再將 base64 資料轉為 bytes
    i = base64.b64decode(img.split(',')[1])
    # 因為 plt 讀取的是檔案，但我們不想存檔案於本地端，
    # 所以在記憶體中創建一個內容為 i 的 bytes 檔案，
    i = io.BytesIO(i)
    # 將 i 這個檔案以 PNG 的形式讀出,若不指定 format,imread 預設會以副檔名解析圖片,
    # 若無法從副檔名得知,則直接以 PNG 嘗試解析。
    # 這邊的情況是沒有副檔名,且有可能讀者遇到非 PNG 的圖片，
    # 因此特別展示可以使用 format 來指定圖片形式
    i = plt.imread(i, format='PNG')
    # 顯示驗證碼
    plt.imshow(i)
    plt.show()
    '''

#登入海大教學務系統
def link():
    try:
        f=open('login.txt','r')
        acnt=f.readline()
        psw=f.readline()
        driver.implicitly_wait(15)
        driver.get('https://ais.ntou.edu.tw/Default.aspx')
        verimg = get_verifyimg()     #取得驗證碼圖片
        codes = vf.vercode(verimg)
        driver.find_element_by_id('M_PW2').send_keys(codes)
        driver.find_element_by_id('M_PW').send_keys(psw)
        driver.find_element_by_id('M_PORTAL_LOGIN_ACNT').send_keys(acnt)
        driver.switch_to.frame(driver.find_element_by_name('menuFrame'))         #切換框架
        driver.find_element_by_id('Menu_TreeViewn1').click()
        driver.find_element_by_id('Menu_TreeViewn29').click()
        driver.find_element_by_id('Menu_TreeViewt39').click()
        driver.switch_to.default_content()          #回到初始框架
        driver.switch_to.frame(driver.find_element_by_name('mainFrame'))
        print(f'connected at {time.ctime()}')
        return True
    except Exception as ex:
        print('Error!')
        print(ex)
        print(f'error at {time.ctime()}')
        return False

def disconnect():
    driver.close()
    print('quit')