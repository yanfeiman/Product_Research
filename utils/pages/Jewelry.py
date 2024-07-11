from utils.translation import *
from utils.dashboard import *
from app import Text 
    
products = pd.read_csv('data/products/products.csv',low_memory=False)
products = products.drop(columns=['Unnamed: 0'])
products = pd.concat([products,pd.read_csv(f'data/products/products2.csv',low_memory=False)], ignore_index=True) 
products.drop_duplicates(inplace=True)

stats = pd.read_csv('data/stats/stats_jewelry.csv')
stats['Product Type'] = stats['Product Type'].astype(str)

allterms = {}
for keyword in products.Keyword:
    if keyword not in allterms: 
        allterms[Text(keyword)] = 0

Dashboard(f'💎 {Text("Amazon Jewelry Dashboard")}', allterms, products, stats)


