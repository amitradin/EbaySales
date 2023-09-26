import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#We are going to check if there is a corraltion between a Seller's Rating and the Price of Items he sells

sales = pd.read_csv('Ebay relations/marketing_sample_for_ebay_com-ebay_com_product__20210101_20210331__30k_data.csv',sep=',',on_bad_lines='skip')
sales['Price']=sales['Price'].str.replace('$','').str.replace('.','').str.replace(',','').astype(float)
sales['Seller Rating']=sales['Seller Rating'].str.replace('%','').astype(float)
mean_val=sales['Seller Rating'].mean()
sales=sales[sales['Seller Rating']>85]
sales['Seller Rating']=sales['Seller Rating'].replace(np.nan,mean_val)#replacing the null values with the mean of the column

#we'll create a funcition to categorize the sellrs rating
def seller_rating_buckets(rating):

    if rating>99.5:
        return "Extremely High"
    if rating >99:
        return "Very high"
    if rating>98.5:
        return 'High'
    if rating>98:
        return 'Medium'
    else:
        return 'Low'
    
print(sales['Price'].corr(sales['Seller Rating']))#0.017933515545626052, there is not much correlation between the two variables so we should not expect much
sales[('Seller Cat')]=sales['Seller Rating'].apply(seller_rating_buckets)
pivot_sales=pd.pivot_table(sales,values='Price',index='Seller Cat')
pivot_sales.sort_values('Price',inplace=True)
#lest plot the results
pivot_sales.plot(kind='barh',figsize=(10,7))
plt.xlabel('Rating')
plt.ylabel('Average Price')
plt.title('Comparing Average Prices For Sellers With Different Rating',color='blue')
plt.show()
#We can see that there is accually No corraltion between the Seller's Rating and the Price of the Items he sells.