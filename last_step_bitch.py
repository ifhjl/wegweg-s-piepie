import pandas as pd
import requests as rq
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool

data = pd.read_excel(r"D:/cases_url.xlsx")
#各个投诉界面的网址
cases_url = []

#最终的数据
cases_data = []

#获取详细案件信息时出错的网址
cases_wrong_url = []

#诡异？
strange_url = []

count = 0

def cases(url):

    global count

    count+=1

    result = 0

    try:

        da = rq.get(url)

        #判断网页是否正常打开
        if da.status_code == 200:

            if url in cases_wrong_url:
                    cases_wrong_url.remove(url)


            
            if len(da.text) != 26147:

                da.encoding = 'utf-8'
                dom = etree.HTML(da.text, etree.HTMLParser(encoding='utf-8'))
                type_name = dom.xpath("/html/body/div[1]/div[2]/div[1]/a[3]/text()")[0]
                name = dom.xpath("/html/body/div[1]/div[2]/div[1]/a[4]/text()")[0]
                detail = dom.xpath("/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[1]/p/text()")[0]
                num = dom.xpath("/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[3]/p[2]/text()")[0]
                ques = dom.xpath("/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[3]/p[3]/text()")[0]
                time = dom.xpath("/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[3]/p[4]/text()")[0]
                seller = dom.xpath("/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[3]/p[5]/text()")[0]
                
                #将数据存入字典
                case = {'type_name':type_name,'name':name,'detail':detail,'num':num,'ques':ques,'time':time,'seller':seller}

                #将字典存入列表
                cases_data.append(case)

                #print("This shit work ! {}".format(url))

                result = "good!"

            else:
                result = "this website is a piece of shit! It's url is {}".format(url)
        
        else:
             cases_wrong_url.append(url)
             result = "might be a good website need observation."

    except Exception as e:

        if url not in cases_wrong_url:
            cases_wrong_url.append(url)
            print(url)
            print(e)
            result = "might be a good website need observation."
    
    print("This is the {}th case and the result is {}".format(count,result))

def spider(urls,func,thread_num):
    pool = ThreadPool(thread_num)
    pool.map(func, urls)
    pool.close()
    pool.join()


#获取各个投诉界面的信息(有问题，未解决)
spider(data[0],cases,10)
while (len(cases_wrong_url) > 10):
    print("left:{}".format(len(cases_wrong_url)))
    spider(cases_wrong_url,cases,10)

cases_data = pd.DataFrame(cases_data)

cases.to_excel(r"D:/finial_BITCH.xlsx")
