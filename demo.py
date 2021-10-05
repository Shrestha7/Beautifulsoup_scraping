from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

webpageurl = 'https://www.daraz.com.np'
data = requests.get(webpageurl)

soup = BeautifulSoup(data.text,'html.parser')

print(soup)
# alls = []
# for d in soup.findAll('div', attrs={'class':'card-official-stores-wrapper'}):
#         name = d.find('a', attrs={'class':'card-jfy-image'})['title']
#         print(name)
#         salePrice= d.find('p', attrs={'class':"product_price price_sale b-product_price-sale b-product_price"})['data-pricevalue']
#         for c in d.findAll('li', attrs={'class':'product_swatch_list_item'}):
#                 style = c.find('a', attrs={'class' :'swatch'})['title']
#                 link = c.find('a', attrs={'class' :'swatch'})['href']
#                 print(name,style,salePrice,link)
#                 all1=[]
#                 all1.append(name)
#                 all1.append(style)
#                 all1.append(salePrice)
#                 all1.append(link)
#                 alls.append(all1)

# data = np.array(alls)
# df = pd.DataFrame(data,columns=['Name','Style','Sale price','URL'])
# df