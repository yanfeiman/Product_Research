from app import Text
from PRODUCT_APP.app.models.translation import *
from utils.dashboard import *

products = pd.read_csv('data/products/nail.csv',low_memory=False)
stats = pd.read_csv('data/stats/stats_nail.csv')
allterms = ['nail','nail polish','press on nails','nail stickers']
for term in allterms: 
    products = pd.concat([products,pd.read_csv(f'data/products/{term}.csv')], ignore_index=True) 
allterms = [Text(_) for _ in allterms]

products.drop_duplicates(inplace=True)

stats['Product Type'] = stats['Product Type'].astype(str)
Dashboard(f'💅 {Text("Amazon Nails Dashboard")}', allterms, products,stats)
