import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

"""In this project we are going to analyze ebay purchases. 
 We'll check what is the most profitable color category, If Price and the number of stars a product got had something to do in common"""

sales = pd.read_csv('Ebay relations/marketing_sample_for_ebay_com-ebay_com_product__20210101_20210331__30k_data.csv',sep=',',on_bad_lines='skip')
#first lets clean the data to see if there is cooralation between the price of the item and his color
print(sales['Color Category'].sort_values())#203 colors
#we can see that there are a ton of colors, but a lot of them are just odd with just one option. so lets look at the top 15 colors
colors=sales['Color Category'].value_counts()[0:15]
color_list=colors.index
color_list=list(color_list)
def color_match(color):
    if color in color_list:
        return True
    return False
sales['match']=sales['Color Category'].apply(color_match)
sales=sales[sales['match']==True]
#we'll normalize the price column
pattern=r'[a-zA-Z][a-zA-Z][a-zA-Z]'
sales['Price']=sales['Price'].str.replace('$','').str.replace('.','').str.replace(',','').astype(float)
def color_fix(color):
    x=re.search(r'[a-zA-Z][a-zA-Z][a-zA-Z]+',color)
    color=color[x.start():x.end()]
    if color[-1]=='F':
        return color[:-1]
    return color
sales['Color Category']=sales['Color Category'].apply(color_fix).str.lower()

#we can see that there are some null values. In order not to lose data lest replace those values with the Average value of the series
sales_clean=sales[sales["Price"]!= np.nan]
mean_val=sales_clean['Price'].mean()
sales['Price'].replace(np.nan,mean_val,inplace=True)

sales=sales.sort_values('Price',ascending=False)
sales=sales.reset_index()
print(sales.columns)

"""we now have a useable data frame we can analyze
now that we have cleaned the data we can check if there is accual corralation between the color of an item and his price"""

pivot_table=pd.pivot_table(sales,'Price',index='Color Category')
pivot_table.sort_values('Price',inplace=True)
print(pivot_table)
pivot_table.plot(kind='barh',figsize=(8,8))
plt.show()
"""We can definatly see there is a cooralation between the color and price. Silver items tend to be the most expensive on average while Red items tend to be the cheapest
this is not a minor difference, we are talking about a 3 times multiplier"""


