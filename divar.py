
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
    
    #url = 'http://gatechannel.ir/fileResults.php'
    #url = "http://aparat.com"
    #url = "http://www.kashano.ir/searchResult/%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86-%D8%AE%D8%B1%DB%8C%D8%AF-%D8%B4%D9%87%D8%B1%D8%A7%D9%86--%D8%AA%D9%87%D8%B1%D8%A7%D9%86-%D8%B4%D9%87%D8%B1%D8%B2%DB%8C%D8%A8%D8%A7--%D8%AA%D9%87%D8%B1%D8%A7%D9%86-%D8%AC%D9%86%D8%AA-%D8%A2%D8%A8%D8%A7%D8%AF-%D8%B4%D9%85%D8%A7%D9%84%DB%8C-(%D8%A7%D8%B2-%D8%A2%D8%A8%D8%B4%D9%86%D8%A7%D8%B3%D8%A7%D9%86-%D8%AA%D8%A7-%D8%B3%DB%8C%D9%85%D9%88%D9%86-%D8%A8%D9%88%D9%84%DB%8C%D9%88%D8%A7%D8%B1)--%D8%AA%D9%87%D8%B1%D8%A7%D9%86-%D8%AC%D9%86%D8%AA-%D8%A2%D8%A8%D8%A7%D8%AF-%D9%85%D8%B1%DA%A9%D8%B2%DB%8C-(%D8%A7%D8%B2-%D9%87%D9%85%D8%AA-%D8%AA%D8%A7-%D8%A2%D8%A8%D8%B4%D9%86%D8%A7%D8%B3%D8%A7%D9%86)--%D8%AA%D9%87%D8%B1%D8%A7%D9%86-%D8%AC%D9%86%D8%AA-%D8%A2%D8%A8%D8%A7%D8%AF-%D8%AC%D9%86%D9%88%D8%A8%DB%8C-(%D8%A7%D8%B2-%D8%A2%DB%8C%D8%AA-%D8%A7%D9%84%D9%84%D9%87-%DA%A9%D8%A7%D8%B4%D8%A7%D9%86%DB%8C-%D8%AA%D8%A7-%D9%87%D9%85%D8%AA)--%D8%AA%D9%87%D8%B1%D8%A7%D9%86-%D8%B3%D8%A7%D8%B2%D9%85%D8%A7%D9%86-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87--%D8%AA%D9%87%D8%B1%D8%A7%D9%86"

    #دیوار تمام آپارتمان ها
    #url = "https://divar.ir/s/tehran/buy-apartment"

    # دیوار فیلتر شده شخصی و منطقه 5
    indexphp = "http://localhost/SendTelegramPost/SendDivar.php"#.....#این متغییر وب پیچ ربات را بر میگرداند
    
    #......# یو آر ال کل منطقه 5
    # url = "https://divar.ir/s/tehran/buy-apartment/south-shahran?districts=151%2C921%2C156%2C153%2C82%2C147%2C170%2C158%2C157%2C173%2C174%2C920%2C159%2C140%2C167%2C168%2C169%2C160%2C155%2C148%2C145%2C146&user_type=personal"
    
    #....# یو آر ال منطقه 5 قسمت هایی
    url = "https://divar.ir/s/tehran/buy-residential/south-shahran?districts=151%2C147%2C170%2C158%2C173%2C920%2C159%2C160%2C155%2C148%2C145%2C146&user_type=personal"

    scr = requests.get(url).text
    bs = BeautifulSoup(scr ,'html.parser')
    #for divar web site

    find = bs.find_all("a",{"class:","col-xs-12 col-sm-6 col-xl-4 p-tb-large p-lr-gutter post-card"})

    #Link = []
    Content = []
    for x in find:
        
        title = x.attrs['href']#.................#کل سرچی که در بالا زده میشود با این دستور فقط اونهایی که اچرف دارند جدا میشوند
        result = "https://divar.ir"+(title)#.....#ایجاد یوارال جدید
        url = result#............................#بوآرال جدید ساخته شد
        # Content.append(url)#.....................#link
        scr = requests.get(url).text#............#حالا این بوآرال رو به سورس اون دسترسی پیدا میکنیم
        bs = BeautifulSoup(scr ,'html.parser')#..#یه بیوتیفول می زنیم و داده استخراج میکنیم
        content = bs.find("div",{"class:","post-page__description"})
        
        if "مشاور" in content.text or "کارشناس" in content.text or "خانم" in content.text or "مسکن" in content.text or "املاک" in content.text:
            continue
        else:
            Content.append(url)#.....................#link
            Content.append(content.text) #content
            
            
            pro2 = bs.find_all("a",{"class:","post-fields-item__value"})
            Content.append(pro2[1].text) #mahal
            
            pro = bs.find_all("div",{"class:","post-fields-item__value"})
            Content.append(pro[1].text) #area 
            Content.append(pro[2].text) #odd 
            Content.append(pro[3].text) #bedroom
            Content.append(pro[4].text) #price
            #Content.append(pro[8].text) #asansor
            #Content.append(pro[9].text) #parking
            #Content.append(pro[10].text)#anbary
        

        newarr = np.array_split(Content, len(Content)/7)#....#این تقسیم بر 9 که اینجا میبینید برای تعداد یک سطر است اگر تعداد یک سطر کمتر شد باید این عدد دوباره اصلاح گردد
        
        with connection.cursor() as cursor:#.......#تمام مقادیر مربوط به فقط لینک ها را استخراج میکنیم
            imp = "SELECT link FROM `divar`"
            cursor.execute(imp)
            resultdb = cursor.fetchall()
        
        Implink = []   #..............................#در قسمت پایین دستور حلقه داریم که لینک ها در این قسمت قرار میگیرند
        for value in resultdb:#...............#دستور را نوشتیم تا تمام مقادیر لینک ها را به ای ام پی انتقال دهیم
            Implink.append(value) 

        for xx in newarr:
        
            with connection.cursor() as cursor:#.......#تمام مقادیر مربوط به فقط لینک ها را استخراج میکنیم
                imp = "SELECT link FROM `divar` ORDER BY id DESC LIMIT 1"
                cursor.execute(imp)
                resultdb = cursor.fetchall()
                xxx = str(xx[0])
                resultdb = str(resultdb[0][0])
                if resultdb in xxx:
                    
                    print("Found Similar... Continue For Results...")
                    
                else:
                    print("Oh!... Found A New Record")
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO `divar` (`link`,`content`,`mahal`,`area`,`odd`,`bedroom`,`price`,`time`) VALUES (%s,%s,%s,%s,%s,%s,%s,%r)"
                        cursor.execute(sql,(str(xx[0]),str(xx[1]),str(xx[2]),str(xx[3]),str(xx[4]),str(xx[5]),str(xx[6]),float(time.time())))
                        #connection is not autocommit by default. So you must commit to save your changes.
                        requests.get(indexphp)  
                connection.commit()   
                
                break
        
    time.sleep(20)