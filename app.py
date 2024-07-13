###############################
import streamlit as st
import pandas as pd 
import json 
import math 
from utils.translation import *
###############################

langcode = "zh" 

def Text(string): 
    if langcode == "zh" and string in en_to_zh: 
        return en_to_zh[string]
    elif string in zh_to_en:
        return zh_to_en[string]
    else: 
        return string
###############################
# from st_pages import Page, show_pages, add_page_title
# add_page_title()
# if langcode == "zh": 
#     show_pages(
#         [
#             Page("app.py", Text("Search")),
#             # Page("pages/Jewelry.py", Text("Jewelry")),
#             # Page("pages/Nails.py", Text("Nails")),
#         ]
#     )
# else: 
#     show_pages([Page("app.py", Text("Search"))])

###############################
PRODUCTS = pd.read_csv(f"data/products.csv")
# get categories 
with open(f'data/categories_graph.json',"r") as  file: 
    CATEGORIES_GRAPH = json.load(file)
    
# get names and translations of categories 
ids_names = pd.read_csv(f"data/ID_TO_NAME.csv")
ALL_ID_TO_NAME = {str(cat_id): (ids_names['name'][idx],ids_names['translation'][idx]) for idx, cat_id in enumerate(ids_names['id']) }
ALL_NAME_TO_ID = {ids_names['name'][idx]: str(cat_id) for idx, cat_id in enumerate(ids_names['id']) }
ALL_NAME_TO_ID.update({ids_names['translation'][idx]: str(cat_id) for idx, cat_id in enumerate(ids_names['id']) }) 

LASTUPDATED = "2024-07-03"
with open(f'data/search_ids.json',"r") as  file: 
    SEARCH_CATEGORIES = json.load(file)

NUMLEVELS = max(len(x) for x in SEARCH_CATEGORIES.values()) + 1 
ALL_RELEVANT_IDS = {c: [c] for c in list(SEARCH_CATEGORIES.keys())}
for search_id, elist in SEARCH_CATEGORIES.items():
    for e in elist: 
        if e not in ALL_RELEVANT_IDS: ALL_RELEVANT_IDS[e] = []
        ALL_RELEVANT_IDS[e].append(search_id)

relevant_cat = {}
for level,edge_dict in CATEGORIES_GRAPH.items(): 
    if level == "0" :relevant_cat['0'] = edge_dict
    else:
        relevant_cat[level] = {}
        for cat_id, children in edge_dict.items(): 
            if cat_id in ALL_RELEVANT_IDS: 
                relevant_cat[level][cat_id] = children

###############################
with st.sidebar:
    lang = st.selectbox('选择语言/Select Language： ', ["简体中文/Chinese (simplified)","英文/English"], index=0)
    if lang == "英文/English":
        langcode = "en"
    else: 
        langcode = "zh"

    st.write(f"## {Text('Amazon Analytics')}")
    st.write( Text("This website provides aggregate statistics for product data from searches on Amazon. Only products with at least one review are included for analysis."))

    with st.expander(Text('Explanation of Terms'), expanded=True):
        st.markdown(f'''
            - :blue[**{Text("Search Phrase")}**]: {Text("Each search phrase is a keyword which we applied to a relevant category. Browse the dropdown menu to the right to explore, and filter these keywords by categories.")}
            - :blue[**{Text("Revenue")}**]: {Text("To estimate the minimum revenue for a product, we multiply price by the count of reviews.")}
            - :blue[**{Text("Past Month Sales Volume")}**]: {Text("These are products which have approximate sales information for the past month, e.g., '2K+ bought in past month.'")}
            - :blue[**{Text("Organic Search Result")}**]: {Text("These are the non-sponsored search results returned for a query.")} 
            - :blue[**{Text("Paid Search Result")}**]: {Text("These are the sponsored results that are returned for a query.")} 
            ''')
    
    st.write(f"{Text('Last Updated')}: {LASTUPDATED}")

###############################
st.write(f"## {Text('Product Search')}")
cols = st.columns([8,2], gap='small')
# cols = st.columns([5,2,5], gap='small')

with cols[0]:
    text_search = st.text_input(Text("Search"),value="")
with cols[1]:
    source = st.selectbox(Text("Search Result Source"),[Text("All"),Text("Organic Search Result"),Text("Amazon's Choice"),Text("Paid Search Result")])
# with cols[2]:
#     options = st.multiselect("Product Type(s)",[Text("Best Seller"),Text("Past Month Sales Volume"),
#                                                    Text("Price Changed"),Text("Prime")])


cols = st.columns([2,6,2], gap='small')
with cols[0]:
    sortorder = st.selectbox(f"{Text('Sorting Order')}: ", [Text("High to Low"),Text("Low to High")])
with cols[1]:
    sortby = st.multiselect(f"{Text('Sort by (in this order)')}: ",[Text('Title and URL'),Text('Price (USD)'),Text("Minimum Revenue"),
                                   Text('Rating'),Text('Reviews Count'),Text("Past Month Sales Volume"),
                                   Text("Amount Discounted"),Text("Percent Discounted")],
                                   [Text("Minimum Revenue")])


def get_source(source):
    if source == "amazons_choices": 
        return Text("Amazon's Choice")
    return Text(source.capitalize())
PRODUCTS['source'] = PRODUCTS['source'].apply(get_source)

display_cols = {
                "url_image":Text("Image"),
                'url': Text('Page'),
                'title':Text('Title and URL'),
                'price':Text('Price (USD)'),
                'rating':Text('Rating'),
                'reviews_count':Text('Reviews Count'),
                'source':Text("Source"),
                "sales_volume":Text("Past Month Sales Volume"),
                "is_prime":Text('Prime'),
                "best_seller":Text("Best Seller"),
                "min_revenue":Text("Minimum Revenue"),
                "discount":Text("Amount Discounted"),
                "discount_rate":Text("Percent Discounted"), 
                }
PRODUCTS = PRODUCTS.rename(columns=display_cols)

if source == Text("Organic Search Result"):
    df = PRODUCTS[PRODUCTS[Text("Source")] == Text("Organic")]
elif source == Text("Paid Search Result"):
    df = PRODUCTS[PRODUCTS[Text("Source")] == Text("Paid Search Result")]
elif source == Text("Amazon's Choice"):
    df = PRODUCTS[PRODUCTS[Text("Source")] == Text("Amazon's Choice")]
else: 
    df = PRODUCTS 

if len(text_search) > 0: 
    df = df[df[Text('Title and URL')].str.contains(text_search, case=False, na=False)]

# Create a selectbox for parent categories
if langcode == "zh": 
    name_idx = 1 
else: 
    name_idx = 0 


import re 
roots = [f"{ALL_ID_TO_NAME[c][name_idx]} ({c})" for c in relevant_cat["0"]["null"]]
parents = st.multiselect(Text("Categories"), roots,placeholder =Text("Choose an option"))
parent_ids = []
for parent in parents: 
    curr_id = re.findall(r"\((.*?)\)",parent)[0]
    parent_ids.append(curr_id)

selected_cat = {}
selected_cat[0] = parent_ids.copy()

if NUMLEVELS > 1: 
    for level in range(NUMLEVELS)[1:]:
        if len(parent_ids) == 1 and parent_ids[0] in relevant_cat[str(level)]: 
            for parent in parent_ids: 
                children = []
                for c in relevant_cat[str(level)][parent]: 
                    if c not in ALL_RELEVANT_IDS: continue
                    children.append(f"{ALL_ID_TO_NAME[c][name_idx]} ({c})")
                if len(children) == 0: continue
                newparents = st.multiselect(Text("Subcategories"), children,placeholder =Text("Choose an option"))
                newparent_ids = []
                for newparent in newparents: 
                    curr_id = re.findall(r"\((.*?)\)",newparent)[0]
                    newparent_ids.append(curr_id)
            parent_ids = newparent_ids
            selected_cat[level] = parent_ids.copy()

for level in selected_cat.copy():
    if len(selected_cat[level]) == 0: 
        del selected_cat[level]

if len(selected_cat) > 0: 
    cat_df = pd.DataFrame(columns=df.columns)
    lastlevel = max(selected_cat.keys())
    for cid in selected_cat[lastlevel]: 
        for leaf in ALL_RELEVANT_IDS[cid]: 
            selected_rows = df[df['category_id'].str.contains(leaf, case=False, na=False)]
            cat_df = pd.concat([cat_df, selected_rows])
else: 
    cat_df = df.copy()


keywords = {}
for klist in cat_df['keyword']: 
    for k in klist.split("; "):
        keywords[Text(k)] = k
mykeywords = st.multiselect(Text("Search Phrase"), keywords.keys(),placeholder =Text("Choose an option"))
if len(mykeywords) > 0: 
    kdf = pd.DataFrame(columns=cat_df.columns)
    for k in mykeywords: 
        k = keywords[k]
        selected_rows = cat_df[cat_df['keyword'].str.contains(k, case=False, na=False)]
        kdf = pd.concat([kdf, selected_rows])
else: 
    kdf = cat_df.copy()
cat_df = kdf.copy()

if len(cat_df) > 0: 
    pricecol = st.columns([6,2,2])
    minprice = min(cat_df[Text("Price (USD)")])
    maxprice = max(cat_df[Text("Price (USD)")])
    mymin,mymax = minprice,maxprice
    with pricecol[0]:
        
        mymin,mymax = st.slider(
            Text("Price Range"),
            minprice, maxprice, (mymin, mymax))
    with pricecol[1]:
        mymin = st.number_input(Text("Min"),min_value=minprice,max_value=maxprice,value=mymin)
    with pricecol[2]:
        mymax = st.number_input(Text("Max"),min_value=minprice,max_value=maxprice,value=mymax)
    cat_df = cat_df[(cat_df[Text("Price (USD)")] >= mymin) & (cat_df[Text("Price (USD)")] <= mymax)]

# for option in options: 
#     if option == Text("Best Seller"):
#         df = df[df[Text("Best Seller")] == True]
#     if option == Text("Past Month Sales Volume"):
#         df = df[df[Text("Past Month Sales Volume")].notna()]
#     if option == Text("Price Changed"):
#         df = df[df[Text("Percent Discounted")]!= 0.0]
#     if option == Text("Prime"):
#         df = df[df[Text("Prime")] == True]

cat_df = cat_df[display_cols.values()]

################ RESULTS 
topn = 25
start, end = 0,topn
page = 1
cat_df = cat_df.drop_duplicates()


cat_df = cat_df.sort_values(by=sortby,ascending=[sortorder==Text("Low to High")]* len(sortby))
if len(cat_df) > 0: 
    with cols[2]:
        page = st.number_input(Text("Page"),min_value=1,max_value=math.ceil(len(cat_df)/topn),step=1)
        start = (page-1) * topn
        end = start + topn
if langcode == "zh": 
    st.markdown(f"共有 {len(cat_df)} 种产品. 第 {page} 页显示 {min(topn,len(cat_df))} 种产品.")
else: 
    st.markdown(f"There are a total of {len(cat_df)} products. Showing {min(topn,len(cat_df))} products on page {page}.")

rows = cat_df.iloc[start:end]

###############################
# stats 

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from nltk.util import ngrams
import numpy as np 
from collections import Counter 
ngram_types = {'Unigram':1,'Trigram':3,'Bigram':2,'4-Gram': 4}
original_cmap = plt.cm.Blues
n_colors = 256
colors = original_cmap(np.linspace(0, 1, n_colors))
darkening_factor = 0.8
colors[-n_colors//5:] *= darkening_factor
colors = np.clip(colors, 0, 1)
darkened_cmap = LinearSegmentedColormap.from_list('darkened_blues', colors)
def wordcloud(data,topK,n):
    data = data[Text("Title and URL")].head(topK)
    all_ngrams = []
    for item in data:
        tokens = item.split(" ")
        ngrams_list = list(ngrams(tokens, n))
        grams = []
        for gram in ngrams_list: 
            if '' in gram: continue 
            grams.append(" ".join(gram))
        all_ngrams.extend(grams)
    data = Counter(all_ngrams)
    wordcloud = WordCloud(width=2000, height=1000, background_color='white',colormap=darkened_cmap).generate_from_frequencies(data)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    return data

if len(cat_df) > 0: 
    st.markdown("---")
    metrics = [Text("Titles"),Text("Minimum Revenue"),Text("Price (USD)"),Text("Rating"),Text("Reviews Count"),
                Text("Amount Discounted"),Text("Percent Discounted")]

    viscols = st.columns([5,5])
    with viscols[0]:
        select_metric = st.selectbox(Text('Select a metric'),metrics)
    with viscols[1]:
        if len(cat_df) > 150: val = 150
        else: val = len(cat_df)
        topK = st.number_input(
                Text('To see aggregate statistics for the top K products, enter a value for K:'),
                min_value=1, max_value=len(cat_df), value=val, step=10,key="topk")
    top_df = cat_df.head(topK)
    product_types = [Text("Organic Search Result"),Text("Amazon's Choice"),Text("Paid Search Result"),
                    Text("Best Seller"),Text("Past Month Sales Volume"), Text("Price Changed"),Text("Prime")]
    if Text("Titles") == select_metric:
        if langcode != "zh":  
            st.markdown(f'#### Frequent Phrases in Titles for the Top {topK} Products')
        else: 
            st.markdown(f'#### 排名前 {topK} 产品标题中的常见短语')
        
        n = st.selectbox(Text('Select a type of n-gram'), [Text('Unigram'),Text('Bigram'),Text('Trigram'),Text('4-Gram')],index=2)
        n = Text(n)
        wordcols = st.columns([8,2])
        with wordcols[0]:
            frequencies = wordcloud(rows,topK,ngram_types[n])
            frequencies = pd.DataFrame.from_dict(frequencies, orient='index').reset_index()
            frequencies.columns = [Text('N-gram'), Text('Frequency')]
            frequencies = frequencies.sort_values(by=[Text('Frequency'),Text('N-gram')], ascending=[False,True])
            frequencies.reset_index(drop=True, inplace=True)
        with wordcols[1]: 
            if langcode != "zh":
                st.write(f"Top {len(frequencies)} N-grams")
            else: 
                st.write(f"一共 {len(frequencies)} 个符串")
            st.dataframe(frequencies,width=None)

    else: 
        stats = [{Text('Average'):round(rows[select_metric].mean(),2),Text('Median'):round(rows[select_metric].median(),2)}]
        stats = pd.DataFrame(stats)
        st.dataframe(stats)

###############################

if len(cat_df) > 0: 
    
    st.markdown("---")
    dim=(1.25,3,2,1,1,2,1,1,1,2,1,1)
    cols = st.columns(dim, gap='small')
    for idx, head in enumerate(display_cols.values()):
        if idx == 1: continue 
        if idx == 0: 
            cols[idx].write(head)
        else: 
            cols[idx-1].write(head)
    st.markdown("---")
    for i, row in rows.iterrows():
        cols = st.columns(dim, gap='small')

        for j, col in enumerate(rows.columns):
            if j == 1: continue
            if col == Text("Prime"):
                cols[j-1].checkbox('Prime', value=row[col], key=f'{col}_{i}_prime', label_visibility="hidden",disabled=True)
            elif col == Text("Best Seller"):
                cols[j-1].checkbox('Best Seller', value=row[col], key=f'{col}_{i}_bestseller', label_visibility="hidden",disabled=True)
            elif col in Text("Image"):
                cols[0].image(row[Text("Image")], use_column_width="always")
            elif col == Text('Title and URL'):
                url = row.iloc[1]
                asin = row.iloc[1].split("/")[-1]
                cols[j-1].write(row[col])
                cols[j-1].markdown(f'<a href="{url}" target="_blank">{asin}</a>', unsafe_allow_html=True)
            else: 
                cols[j-1].write(row[col])
        


# st.dataframe(df,
        # column_order=(display_cols.values()),
        # hide_index=False,
        # width=None,
        # height=1000,
        # column_config={
        #     Text("Minimum_Revenue"): st.column_config.ProgressColumn(
        #         Text("Minimum_Revenue"),
        #         format="%f",
        #         min_value=min(df[Text("Minimum_Revenue")]),
        #         max_value=max(df[Text("Minimum_Revenue")]),
        #     ),
        #     Text("Prime"): st.column_config.CheckboxColumn(),
        #     Text("Best_Seller"): st.column_config.CheckboxColumn(Text("Best Seller")),
        #     Text("View Detailed Product Page"): st.column_config.LinkColumn(Text("View Detailed Product Page")),
        #     Text("View Product Image"): st.column_config.LinkColumn(Text("View Product Image"))
        #     }
            
        # )


###############################
st.markdown("""
<style>
    
    .appview-container .main .block-container{
        max-width: 100%;
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 4rem;
        padding-bottom: 0rem;
    }
            
    [data-testid="block-container"] {
        padding-left: 0rem;
        padding-right: 0rem;
        padding-top: 0rem;
        padding-bottom: 0rem;
        margin-bottom: -7rem;
    }

    [data-testid="stVerticalBlock"] {
        padding-left: 0rem;
        padding-right: 0rem;
    }
            
    .stMultiSelect [role="listbox"] {
        max-width: 500px;  /* Adjust the width as needed */
        white-space: normal;  /* Allow text wrapping */
    }
            
</style>
""", unsafe_allow_html=True)

#####################################
