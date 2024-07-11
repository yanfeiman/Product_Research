###############################
import streamlit as st
import pandas as pd 
import json 
from utils.translation import *
from st_pages import Page, show_pages, add_page_title
from streamlit_dynamic_filters import DynamicFilters
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
ALL_ID_TO_NAME = pd.read_csv(f"data/ID_TO_NAME.csv")
ALL_ID_TO_NAME = {str(cat_id): ALL_ID_TO_NAME['name'][idx] for idx, cat_id in enumerate(ALL_ID_TO_NAME['id']) }
LASTUPDATED = "2024-07-03"
with open(f'data/search_ids.json',"r") as  file: 
    SEARCH_CATEGORIES = json.load(file)
###############################
with st.sidebar:
    lang = st.selectbox('选择语言/Select Language： ', ["简体中文/Chinese (simplified)","英文/English"], index=0)
    if lang == "英文/English":
        langcode = "en"
    else: 
        langcode = "zh"

    st.write(f"## {Text('Amazon Analytics')}")
    st.write( Text("This website provides aggregate statistics for product data from searches on Amazon. Only products with at least one review are included for analysis."))

    # - :blue[**{Text("Search Phrase")}**] {Text("and")} :blue[**{Text("Position")}**]: {Text("The relevant search phrases and the product's positions in the search results for those phrases (across all pages) are divided respectively by semicolons.")}
    with st.expander(Text('Explanation of Terms'), expanded=True):
        st.markdown(f'''
            - :blue[**{Text("Revenue")}**]: {Text("To estimate the minimum revenue for a product, we multiply price by the count of reviews.")}
            - :blue[**{Text("Past Month Sales Volume")}**]: {Text("These are products which have approximate sales information for the past month, e.g., '2K+ bought in past month.'")}
            - :blue[**{Text("Organic Search Result")}**]: {Text("These are the non-sponsored search results returned for a query.")} 
            - :blue[**{Text("Paid Search Result")}**]: {Text("These are the sponsored results that are returned for a query.")} 
            ''')
    
    st.write(f"{Text('Last Updated')}: {LASTUPDATED}")

###############################
st.write(f"## {Text('Product Search')}")
text_search = st.text_input(Text("Search"),value="")
options = st.multiselect("Choose the types of product",[Text("Best Seller"),Text("Paid Search Result"),
                                                   Text("Organic Search Result"),Text("Amazon's Choice"),
                                                   Text("Price Changed"),Text("Prime")],
                                                   [Text("Best Seller"),
                                                   Text("Organic Search Result")])

cat_options = st.multiselect("Choose the product category",["Violin Strings"])

cols = st.columns([3,5], gap='small')
with cols[0]:
    sortorder = st.selectbox("Sort Order: ", ["High to Low","Low to High"])
with cols[1]:
    sortby = st.multiselect("Sort by",[Text('Title and URL'),Text('Price (USD)'),Text("Minimum Revenue"),
                                   Text('Rating'),Text('Reviews Count'),Text("Past Month Sales Volume"),
                                   Text("Amount Discounted"),Text("Percent Discounted")],
                                   [Text("Minimum Revenue")])


def get_source(source):
    if source == "amazons_choices": 
        return Text("Amazon's Choice")
    return Text(source.capitalize())
PRODUCTS['source'] = PRODUCTS['source'].apply(get_source)
df = PRODUCTS[PRODUCTS["title"].str.contains(text_search, case=False, na=False)]

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
df = df.rename(columns=display_cols)
df = df[display_cols.values()]
for option in options: 
    if option == Text("Best Seller"):
        df = df[df[Text("Best Seller")] == True]
    if option == Text("Organic Search Result"):
        df = df[df[Text("Source")] == Text("Organic")]
    if option == Text("Amazon's Choice"):
        df = df[df[Text("Source")] == Text("Amazon's Choice")]
    if option == Text("Past Month Sales Volume"):
        df = df[df[Text("Past Month Sales Volume")] != 0]
topn = 50
st.markdown(f"There are a total of {len(df)} products. Showing the top {topn} products (if available).")
df = df.head(topn)


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
for i, row in df.iterrows():
    cols = st.columns(dim, gap='small')

    for j, col in enumerate(df.columns):
        if j == 1: continue
        if col == Text("Prime"):
            cols[j-1].checkbox('Prime', value=row[col], key=f'{col}_{i}_prime', label_visibility="hidden",disabled=True)
        elif col == Text("Best Seller"):
            cols[j-1].checkbox('Best Seller', value=row[col], key=f'{col}_{i}_bestseller', label_visibility="hidden",disabled=True)
        elif col in Text("Image"):
            cols[0].image(row[Text("Image")], width=60)
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
            
</style>
""", unsafe_allow_html=True)

#####################################
# st.write(f"## {Text('Analytics for Product Research')}")

# st.markdown(
#     f"""
    
#     {Text("Browse already collected data on these pages linked below and in the left sidebar:")} 
#     - [{Text("Jewelry")}](https://beauty.streamlit.app/{Text("Jewelry")})
#     - [{Text("Nails")}](https://beauty.streamlit.app/{Text("Nails")})

#     """
# )

# ### See more complex demos
    # - Use a neural net to [analyze the Udacity Self-driving Car Image
    #     Dataset](https://github.com/streamlit/demo-self-driving)
    # - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)

