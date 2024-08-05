
import requests
from bs4 import BeautifulSoup
import pymysql.cursors
import numpy as np
import time

try:   
    connection = pymysql.connect(host='localhost',user='mojtaba',password='1234',db='extractdata')
except:
    print("Ops... Can Not Connection to DataBase")

while True:

    # # دیوار فیلتر شده شخصی و منطقه 5
    # urld = "https://divar.ir/s/tehran/buy-apartment/south-shahran?districts=151%2C921%2C156%2C153%2C82%2C147%2C170%2C158%2C157%2C173%2C174%2C920%2C159%2C140%2C167%2C168%2C169%2C160%2C155%2C148%2C145%2C146&user_type=personal"
    indexphp = "http://localhost/SendTelegramPost/SendSheypoor.php"#.....#این متغییر وب پیچ ربات را بر میگرداند
    # شیپور شخصی شده
    # urlsh  = "https://www.sheypoor.com/%D8%AA%D9%87%D8%B1%D8%A7%D9%86/%D8%A7%D8%A8%D8%A7%D8%B0%D8%B1/%D8%A7%D9%85%D9%84%D8%A7%DA%A9/%D8%AE%D8%B1%DB%8C%D8%AF-%D9%81%D8%B1%D9%88%D8%B4-%D8%AE%D8%A7%D9%86%D9%87-%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86?nh[0]=883&nh[1]=4735&nh[2]=952&nh[3]=4718&nh[4]=974&nh[5]=5214&nh[6]=5211&nh[7]=1013&nh[8]=907&nh[9]=5217"
    urlsh  = "https://www.sheypoor.com/%D8%AA%D9%87%D8%B1%D8%A7%D9%86/%D8%A8%D9%84%D9%88%D8%A7%D8%B1-%D9%81%D8%B1%D8%AF%D9%88%D8%B3-%D8%B4%D8%B1%D9%82/%D8%A7%D9%85%D9%84%D8%A7%DA%A9/%D8%AE%D8%B1%DB%8C%D8%AF-%D9%81%D8%B1%D9%88%D8%B4-%D8%AE%D8%A7%D9%86%D9%87-%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86?nh[0]=952&nh[1]=4718&nh[2]=5214&nh[3]=5211&nh[4]=1013&nh[5]=5256&nh[6]=1122"
    #این چند خط کد برای اصلاح ریدایرکت های زیاد در شیپور هستش
    loc = urlsh
    seen = set()
    while True:
        r = requests.get(loc, allow_redirects=False)
        loc = r.headers['location']
        if loc in seen: break
        seen.add(loc)
        

    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    r = s.get(urlsh).text

    bs = BeautifulSoup(r ,'html.parser')

    findsh = bs.find_all("article",{"class:","serp-item list"})
    # find = bs.find_all("div",{"class:","content"},limit=1)

    Content = []
    for value in findsh:
        
        if (value.find("div",{"class:","shop-logo"}) in value.find("div",{"class:","content"})) == False:
        
            link = value.find("a")['href']#..................#لینک ساخته می شود 
            
            # ...# لینک که در بالا ساخته شد به خاطر گوه کاری شیپور مجبوریم که ریدایرکت رو دور بزنیم با کد ها زیر
            loc = link
            seen = set()
            while True:
                r = requests.get(loc, allow_redirects=False)
                loc = r.headers['location']
                if loc in seen: break
                seen.add(loc)
                
            s = requests.Session()
            s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
            scr = s.get(link).text#...........# سورس جدید برای باز کردن صفحات
        
            bs = BeautifulSoup(scr ,'html.parser')#........#بیوتیفول  میزنیم به همون سورس جدید
            findDs = bs.find("p",{"class:","description"})#.........#توضیحات رو میکشیم بیرون
            
            if "مشاور" in findDs.text or "کارشناس" in findDs.text or "مسکن" in findDs.text or "املاک" in findDs.text:
                continue
            else:
                Content.append(link)#..............#link
                Content.append(findDs.text)#.......#description
                
                #...#جهت پیدا کردن و تمیز کردن محل در این صفحه
                findmahal = bs.find("span",{"class:","small-text"}).text
                findmahal = findmahal.strip()
                Content.append(findmahal)#...........# mahal
                
                

            newarr = np.array_split(Content, len(Content)/3)#....#این تقسیم بر 9 که اینجا میبینید برای تعداد یک سطر است اگر تعداد یک سطر کمتر شد باید این عدد دوباره اصلاح گردد
            
            with connection.cursor() as cursor:#.......#تمام مقادیر مربوط به فقط لینک ها را استخراج میکنیم
                imp = "SELECT link FROM `sheypoor`"
                cursor.execute(imp)
                resultdb = cursor.fetchall()    
                
            Implink = []   #..............................#در قسمت پایین دستور حلقه داریم که لینک ها در این قسمت قرار میگیرند
            for value in resultdb:#...............#دستور را نوشتیم تا تمام مقادیر لینک ها را به ای ام پی انتقال دهیم
                Implink.append(value) 
                
            for xx in newarr:
                
                with connection.cursor() as cursor:#.......#تمام مقادیر مربوط به فقط لینک ها را استخراج میکنیم
                    imp = "SELECT link FROM `sheypoor` ORDER BY id DESC LIMIT 1"
                    cursor.execute(imp)
                    resultdb = cursor.fetchall()
                    xxx = str(xx[0])
                    resultdb = str(resultdb[0][0])
                    if resultdb in xxx:
                        
                        print("Found Similar... Continue For Results...")
                        
                    else:
                        print("Oh!... Found A New Record")
                        with connection.cursor() as cursor:
                            sql = "INSERT INTO `sheypoor` (`link`,`content`,`mahal`,`time`) VALUES (%s,%s,%s,%r)"
                            cursor.execute(sql,(str(xx[0]),str(xx[1]),str(xx[2]),float(time.time())))
                            #connection is not autocommit by default. So you must commit to save your changes.
                            requests.get(indexphp)      
                    connection.commit()   
                    
                    break  

    time.sleep(120)




