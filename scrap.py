from bs4 import BeautifulSoup
import requests
import pandas as pd
url = "https://www.mytek.tn/image-son/televiseurs/tv-led.html"
result = requests.get(url).text
doc = BeautifulSoup(result, "html.parser")
body = doc.body
pages = doc.find_all(['ul'],class_='items pages-items')
pagesCount = pages[0].find_all(['li']).__len__()-1
print(pagesCount)
df = pd.DataFrame(columns=["marque","title", "price", "description","imgTv","imgMarque"])
for i in range(pagesCount):
    page = i+1
    url = "https://www.mytek.tn/image-son/televiseurs/tv-led.html?p="+str(page)
    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")
    body = doc.body
    title = doc.find_all(['strong'],class_='product name product-item-name')
    imgTv = doc.find_all('img',class_='product-image-photo')
    marque = doc.find_all('img', alt=True , attrs={'style' : "width:32% ;height:30%;display:block;"})
    tv = doc.find_all(['div'],class_='product details product-item-details')
    description = doc.find_all(['div'],class_='strigDesc')
    price = doc.find_all(['div'],class_='price-box price-final_price')
    data = []
    imgMarque = doc.find_all('img', alt=True , attrs={'style' : "width:32% ;height:30%;display:block;"})
    for i in range(title.__len__()) :
        marque[i] = marque[i]['alt']
        imgMarque[i] = imgMarque[i]['src']
        imgTv[i] = imgTv[i]['src']
        title[i] = title[i].text
        price[i] = price[i].find_all(['span'], class_='price')[0].text
        description[i] = description[i].p.text
        row = [marque[i],title[i],price[i],description[i],imgTv[i],imgMarque[i]]
        data.append(row)
    a = pd.DataFrame(data,columns=["marque","title","price","description","imgTv","imgMarque"])
    df = pd.concat([df, a], ignore_index=True)
newdf = df[df['marque'].isin(['samsung'])]
print(newdf['title'])
#print(df)