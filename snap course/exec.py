import os
import time
import base64
import verify as vf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

os.chdir(os.path.dirname(__file__))
driver = webdriver.Edge(service=Service("msedgedriver.exe"))
ret_types = { 1 : '未找到課程', 2 : '課程不可選', 3 : '成功選取', 4 : '選取失敗', 5 : '人數已達上限', 6 : '系統錯誤'}

def find_course(course):
    try:
        driver.execute_script("""var crs = arguments[0];
                                document.getElementById('Q_COSID').value = crs""", course)
        driver.find_element(By.ID, 'QUERY_COSID_BTN').click()
        return True
    except Exception as ex:
        print('Error during find course')
        print(ex)
        print(f'error at {time.ctime()}')
        return False

def choose_course():
    try:
        driver.find_element(By.ID, 'DataGrid1_ctl02_edit').click()
        return True
    except Exception as ex:
        print('Error during choose course')
        print(ex)
        print(f'error at {time.ctime()}')
        return False

def snapCourse(c):
    if not find_course(c):
        return 1
    time.sleep(0.8)
    if not choose_course():
        return 2
    time.sleep(2.5)
    return snapAlert()

def alert_info():
    try:
        Alert = driver.switch_to.alert
        text = Alert.text
        return Alert, text
    except:
        return None, 'none'

def snapAlert():
    alert_message = ['本科目設有檢查人數下限。選本課程，在未達下限人數前時無法退選，確定加選?', '年級不可加選！', '衝堂不可選！']
    try:
        alert, text = alert_info()
        if text == alert_message[0]:
            alert.accept()
            time.sleep(0.5)
            alert, text = alert_info()
            if alert is not None:
                alert.accept()
                return 4
            else:
                return 3
        elif text == alert_message[1] or text == alert_message[2]:
            alert.accept()
            return 4
        else:
            blk_text = text.split('：')
            if alert is not None:
                alert.accept()
            if(len(blk_text) > 1):
                return 5
            else:
                return 3
    except Exception as ex:
        print('Error during snapping')
        print(ex)
        print(f'error at {time.ctime()}')
        return 6

def getCourse():
    f = open('course.txt','r')
    fres = open('result.txt','w')
    course = f.readlines()
    course = [c.strip() for c in course]    #去除換行符號
    for c in course:
        fres.write(f'{time.ctime()}\n')
        ret = snapCourse(c)
        if ret == 6:
            break
        else:
            fres.write(f'{c} {ret_types[ret]}\n')
        #driver.find_element(By.ID, 'QCLEAR_BTN1').click()

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
        verimg = get_verifyimg()                                                #取得驗證碼圖片
        codes = vf.vercode(verimg)
        driver.find_element(By.ID, 'M_PW2').send_keys(codes)
        driver.find_element(By.ID, 'M_PW').send_keys(psw)
        driver.find_element(By.ID, 'M_PORTAL_LOGIN_ACNT').send_keys(acnt)
        driver.switch_to.frame(driver.find_element(By.NAME, 'menuFrame'))       #切換框架
        driver.find_element(By.ID, 'Menu_TreeViewn1').click()
        driver.find_element(By.ID, 'Menu_TreeViewn30').click()
        driver.find_element(By.ID, 'Menu_TreeViewt40').click()
        driver.switch_to.default_content()                                      #回到初始框架
        driver.switch_to.frame(driver.find_element(By.NAME, 'mainFrame'))
        print(f'Connected at {time.ctime()}')
        return True
    except Exception as ex:
        print('Error during connecting')
        print(ex)
        print(f'error at {time.ctime()}')
        return False

def disconnect():
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.NAME, 'menuFrame'))
    driver.find_element(By.ID, 'Menu_TreeViewt26').click()
    driver.close()
    print('Quit')