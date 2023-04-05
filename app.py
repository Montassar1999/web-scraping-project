# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO


# Create application
app = Flask(__name__)


# Bind home function to URL
@app.route('/')
def home():
    df = scraping()
    # print(df)
    return render_template('Tv.html', result=df ,data=df)



def scraping():
    url = "https://www.mytek.tn/image-son/televiseurs/tv-led.html"
    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")
    body = doc.body
    pages = doc.find_all(['ul'], class_='items pages-items')
    pagesCount = pages[0].find_all(['li']).__len__() - 1
    df = pd.DataFrame(columns=["marque", "title", "price", "description", "imgTv", "imgMarque"])
    for i in range(pagesCount):
        page = i + 1
        url = "https://www.mytek.tn/image-son/televiseurs/tv-led.html?p=" + str(page)
        result = requests.get(url).text
        doc = BeautifulSoup(result, "html.parser")
        title = doc.find_all(['strong'], class_='product name product-item-name')
        imgTv = doc.find_all('img', class_='product-image-photo')
        marque = doc.find_all('img', alt=True, attrs={'style':"width:32%;height:30%;display:block;"})
        description = doc.find_all(['div'], class_='strigDesc')
        price = doc.find_all(['div'], class_='price-box price-final_price')
        data = []
        imgMarque = doc.find_all('img', alt=True, attrs={'style':"width:32%;height:30%;display:block;"})

        for i in range(title.__len__()):
            marque[i] = marque[i]['alt']
            imgMarque[i] = imgMarque[i]['src']
            imgTv[i] = imgTv[i]['src']
            title[i] = title[i].text
            price[i] = price[i].find_all(['span'], class_='price')[0].text
            myPrice = price[i][0:-3]
            myPrice = ''.join(myPrice.split())
            myPrice = myPrice.replace(',','.')
            myPrice = float(myPrice)
            price[i] = myPrice
            description[i] = description[i].p.text
            row = [marque[i], title[i], price[i], description[i], imgTv[i], imgMarque[i]]
            data.append(row)
        a = pd.DataFrame(data, columns=["marque", "title", "price", "description", "imgTv", "imgMarque"])
        df = pd.concat([df, a], ignore_index=True)
    return df


@app.route('/filter', methods=['POST'])
def filter():
    json_data = request.form.get('data')
    df = pd.read_json(json_data)
    min = request.form.get('min_price')
    max  = request.form.get('max_price')
    marques = request.form.getlist('marque')

    if marques.__len__() == 0:
        marques = ['samsung', 'vega', 'schneider', 'telefunken', 'sony', 'orient', 'tcl', 'newstar', 'westpoint', 'biolux', 'saba', 'unionaire', 'lg', 'xiaomi']
    res = df[(df['price'] >= float(min)) & (df['price'] <= float(max)) & (df['marque'].isin(marques))]
    return render_template('Tv.html',result = res, data=df)

if __name__ == '__main__':
    # Run the application
    app.run()

