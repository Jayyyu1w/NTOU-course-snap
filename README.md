# NTOU-course-snap

在login.txt內輸入帳號密碼(各一行，帳號在上)
<br>
在course.txt內輸入課號
<br>
搶課結果會在result.txt內顯示

<b>注意：如果無法開啟，且嘗試更新瀏覽器的driver並重試一次</b>
<b>注意：教學務系統內的id可能會有變動，若找不到課程可能得更改</b>
<br>
```python
    driver.find_element(By.ID, 'Menu_TreeViewn30').click()  <-- 內部的 Menu_TreeView
    driver.find_element(By.ID, 'Menu_TreeViewt40').click()  <-- 
```

---------------------------------------------

目前問題: "本科目設有檢查人數下限。選本課程，在未達下限人數前時無法退選，確定加選?" 
的下一個 alert 無法正確抓取

---------------------------------------------

驗證碼判斷模組 [ddddocr](https://github.com/sml2h3/ddddocr)
搶課使用[selenium](https://www.selenium.dev/)