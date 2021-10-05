from bs4 import BeautifulSoup
import requests
import pandas as pd

url = requests.get('https://www.daraz.com.np')
sp = BeautifulSoup(url.content, 'html.parser')
print(sp.text)

# title = sp.find_all('div', 'fs-card-title')
# sellprice = sp.find_all('span', 'price')
# originalprice = sp.find_all('span', 'price')
# discount = sp.find_all('span', 'fs-discount')


# titleLoop = [titles.text for titles in title]
# sellLoop = [sells.text for sells in sellprice]
# originalpriceLoop = [orig.text for orig in originalprice]
# discountLoop = [discounts.text for discounts in discount]
# print(sellLoop)
# # print(titleLoop)

# data = {
#     'Name_of_console':titleLoop,
#     'Selling_price':sellLoop,
#     'Original_price': originalpriceLoop,
#     'discount': discountLoop
# }

# print(len(titleLoop))
# print(len(sellLoop))
# print(len(orginalLoop))
# print(len(discountLoop))

# df= pd.DataFrame(data,columns=[
#     'Name_of console',
#     'Selling_price',
#     'discount'
# ])

# df2 = pd.DataFrame(data,columns=['Original_price'])
# Originalprice =df2['Original_price']
# df = df.join(Originalprice)
# print(df)
# df.to_csv(r'bs.csv',index=False)