
import requests
from bs4 import BeautifulSoup
import pymysql.cursors
import numpy as np
import time

try:   
    connection = pymysql.connect(host='localhost',user='mojtaba',password='1234',db='extractdata')
except:
    print("Ops... Can Not Connection to DataBase")

# while True:

# # دیوار فیلتر شده شخصی و منطقه 5
# urld = "https://divar.ir/s/tehran/buy-apartment/south-shahran?districts=151%2C921%2C156%2C153%2C82%2C147%2C170%2C158%2C157%2C173%2C174%2C920%2C159%2C140%2C167%2C168%2C169%2C160%2C155%2C148%2C145%2C146&user_type=personal"
indexphp = "http://localhost/SendTelegramPost/SendDodota.php"#.....#این متغییر وب پیچ ربات را بر میگرداند
# شیپور شخصی شده


for x in range(89,118):
    url  = "https://dodota.com/realestate/search/?deal_type=1&v1=1&region_code=THR&citycode=1&mahale_code=%i" %x
    scr = requests.get(url).text
    bs = BeautifulSoup(scr ,'html.parser')
    

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
        
        if "مشاور" in content.text or "کارشناس" in content.text:
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
        
    time.sleep(5)

# #این چند خط کد برای اصلاح ریدایرکت های زیاد در شیپور هستش
# loc = url
# seen = set()
# while True:
#     r = requests.get(loc, allow_redirects=False)
#     loc = r.headers['location']
#     if loc in seen: break
#     seen.add(loc)
    

# s = requests.Session()
# s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
# r = s.get(url).text

# bs = BeautifulSoup(r ,'html.parser')

# findsh = bs.find_all("article",{"class:","serp-item list"})
# # find = bs.find_all("div",{"class:","content"},limit=1)

# Content = []
# for value in findsh:
    
#     if (value.find("div",{"class:","shop-logo"}) in value.find("div",{"class:","content"})) == False:
    
#         link = value.find("a")['href']#..................#لینک ساخته می شود 
        
#         # ...# لینک که در بالا ساخته شد به خاطر گوه کاری شیپور مجبوریم که ریدایرکت رو دور بزنیم با کد ها زیر
#         loc = link
#         seen = set()
#         while True:
#             r = requests.get(loc, allow_redirects=False)
#             loc = r.headers['location']
#             if loc in seen: break
#             seen.add(loc)
            
#         s = requests.Session()
#         s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
#         scr = s.get(link).text#...........# سورس جدید برای باز کردن صفحات
    
#         bs = BeautifulSoup(scr ,'html.parser')#........#بیوتیفول  میزنیم به همون سورس جدید
#         findDs = bs.find("p",{"class:","description"})#.........#توضیحات رو میکشیم بیرون
    
#         if "مشاور" in findDs.text or "کارشناس" in findDs.text:
#             continue
#         else:
#             Content.append(link)#..............#link
#             Content.append(findDs.text)#.......#description
            
#             #...#جهت پیدا کردن و تمیز کردن محل در این صفحه
#             findmahal = bs.find("span",{"class:","small-text"}).text
#             findmahal = findmahal.strip()
#             Content.append(findmahal)#...........# mahal
            
            

#         newarr = np.array_split(Content, len(Content)/3)#....#این تقسیم بر 9 که اینجا میبینید برای تعداد یک سطر است اگر تعداد یک سطر کمتر شد باید این عدد دوباره اصلاح گردد
        
#         with connection.cursor() as cursor:#.......#تمام مقادیر مربوط به فقط لینک ها را استخراج میکنیم
#             imp = "SELECT link FROM `dodota`"
#             cursor.execute(imp)
#             resultdb = cursor.fetchall()    
            
#         Implink = []   #..............................#در قسمت پایین دستور حلقه داریم که لینک ها در این قسمت قرار میگیرند
#         for value in resultdb:#...............#دستور را نوشتیم تا تمام مقادیر لینک ها را به ای ام پی انتقال دهیم
#             Implink.append(value) 
            
#         for xx in newarr:
            
#             with connection.cursor() as cursor:#.......#تمام مقادیر مربوط به فقط لینک ها را استخراج میکنیم
#                 imp = "SELECT link FROM `dodota` ORDER BY id DESC LIMIT 1"
#                 cursor.execute(imp)
#                 resultdb = cursor.fetchall()
#                 xxx = str(xx[0])
#                 resultdb = str(resultdb[0][0])
#                 if resultdb in xxx:
                    
#                     print("Found Similar... Continue For Results...")
                    
#                 else:
#                     print("Oh!... Found A New Record")
#                     with connection.cursor() as cursor:
#                         sql = "INSERT INTO `dodota` (`link`,`content`,`mahal`,`time`) VALUES (%s,%s,%s,%r)"
#                         cursor.execute(sql,(str(xx[0]),str(xx[1]),str(xx[2]),float(time.time())))
#                         #connection is not autocommit by default. So you must commit to save your changes.
#                         requests.get(indexphp)      
#                 connection.commit()   
                
#                 break  

# time.sleep(120)




