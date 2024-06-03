#######################
import streamlit as st
import pandas as pd
import numpy as np 
import altair as alt
import plotly.express as px
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import nltk
from nltk.util import ngrams
import string 
#######################
st.set_page_config(
    page_title="Amazon Jewelry Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded")


#######################
st.markdown("""
<style>
    .stSelectbox:first-of-type > div[data-baseweb="select"] > div {
	    background-color: white;
    	padding: 10px;
        border: none;
	}
            
    [data-testid="block-container"] {
        padding-left: 2rem;
        padding-right: 2rem;
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
# header {visibility: hidden;}
#######################
products = pd.read_csv('data/products.csv')
products = products.drop(columns=['Unnamed: 0'])
stats = pd.read_csv('data/stats.csv')
stats['Product Type'] = stats['Product Type'].astype(str)


allterms = {}
for keyword in products.Keyword:
    if keyword not in allterms: 
        allterms[keyword] = 0



with st.sidebar:
    st.title('💎 Amazon Jewelry Dashboard')
    
    # a category of products 
    categories = ['All']
    categories.extend([term.capitalize() for term in allterms])
    selected_category = st.selectbox('Select a keyword for a category of products', categories)
    
    if selected_category == 'All': 
        df = products
        metrics = {}
        for idx, term in enumerate(stats.Title):
            p_type = stats['Product Type'][idx]
            term = f"{p_type} - {term}" 
            if term not in metrics: metrics[term] = None 
            if f"{p_type} - Frequent Phrases" not in metrics: metrics[f"{p_type} - Frequent Phrases"] = None 
    else: 
        df = products[products.Keyword == selected_category.lower()]
        metrics = ["Revenue","Prices","Rating","Reviews Count","Amount Discounted","Percent Discounted","Frequent Phrases"]

    select_metric = st.selectbox('Select a metric for visualization', metrics)
    if "Best" in select_metric: 
        all_df = df[df.Best_Seller == True]
    elif "Prime" in select_metric: 
        all_df = df[df.Prime == True]
    elif "Past" in select_metric: 
        all_df = df[df['Sales_Volume_Past_Month'].notnull()]
    elif 'Discounted' in select_metric: 
        all_df = df[df['Discount'].notnull()]
    else: 
        all_df = df

all_df['URL'] = 'https://amazon.com' + df['URL'].astype(str)
all_prod = all_df.to_dict(orient='records')
unique_asin = {info['ASIN']: 0 for info in all_prod}
unique = {}
for info in all_prod: 
    if info["ASIN"] not in unique: 
        unique[info["ASIN"]] = info
    else: 
        unique[info["ASIN"]]["Keyword"] = unique[info["ASIN"]]["Keyword"] + "; " + info["Keyword"]
        unique[info["ASIN"]]["Search_Term"] = unique[info["ASIN"]]["Search_Term"] + "; " + info["Search_Term"]
        unique[info["ASIN"]]["Position"] = unique[info["ASIN"]]["Position"] + "; " + info["Position"]
unique = pd.DataFrame(unique.values())
#######################

def bar_metric(title,metric="Mean"): 
    if selected_category == "All": 
        ptype,title = title.split(" - ")
        data = stats[stats.Title == title]
        data = data[data["Product Type"] == ptype]
        data = data.sort_values(by=[metric,'Search Type','Keyword'], ascending=[False,False,True])
        chart = alt.Chart(data).mark_bar(opacity=0.7).encode(
            x=alt.X('Keyword:O', axis=alt.Axis(labelAngle=90), title='Keyword'),  
            y=alt.Y(f'{metric}:Q', title=f"{metric} {title}").stack(None),
            color=alt.Color('Search Type:N', legend=alt.Legend(title="Type of Search Result",orient="bottom"))  
        )
    else: 
        data = stats[stats.Title == title]
        data = data[data.Keyword == selected_category.lower()]
        data = data.sort_values(by=[metric,'Search Type','Product Type'], ascending=[False,False,True])
        chart = alt.Chart(data).mark_bar(opacity=0.7).encode(
            x=alt.X(f'{metric}:Q', axis=alt.Axis(labelAngle=0), title=f"{metric} {title}").stack(None),  
            y=alt.Y('Product Type:O',title='Product Type'),
            color=alt.Color('Search Type:N', legend=alt.Legend(title="Type of Search Result",orient="bottom"))  
        )
    st.altair_chart(chart, use_container_width=True)


def bar_searchterms(topK): 
    data = unique
    terms = []
    for term in data.Search_Term.head(topK): 
        terms.extend(term.split("; "))
    terms = Counter(terms)
    topterms = Counter(terms).most_common(n=25)
    chart = pd.DataFrame({
        'Search Phrase': [x[0] for x in topterms],
        'Frequency': [x[1] for x in topterms]
    }
    )
    chart = chart.sort_values(by='Frequency',ascending=True)
    fig = px.bar(chart, x='Frequency', y='Search Phrase', orientation='h')
    st.plotly_chart(fig)
    return terms

original_cmap = plt.cm.Blues
n_colors = 256
colors = original_cmap(np.linspace(0, 1, n_colors))
darkening_factor = 0.6
colors[-n_colors//5:] *= darkening_factor
colors = np.clip(colors, 0, 1)
darkened_cmap = LinearSegmentedColormap.from_list('darkened_blues', colors)

def wordcloud(n):
    data = unique.Title.head(n)
    all_ngrams = []
    for item in data:
        translator = str.maketrans('', '', string.punctuation)
        item = item.translate(translator)
        tokens = nltk.word_tokenize(item)
        for i in range(2,4): 
            ngrams_list = list(ngrams(tokens, i))
            ngrams_list = ['_'.join(gram) for gram in ngrams_list]
        all_ngrams.extend(ngrams_list)
    data = Counter(all_ngrams)
    wordcloud = WordCloud(width=2000, height=1000, background_color='white',colormap=darkened_cmap).generate_from_frequencies(data)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    return data
    
def histogram(title): 
    data = unique[title]
    fig = px.histogram(data, nbins=30, labels={'value': 'Value', 'count': 'Frequency'})
    st.plotly_chart(fig)
     
#######################
col = st.columns((4, 5), gap='large')

with col[1]:

    if "Best" in select_metric: 
        st.markdown('#### Top Best Sellers by Minimum Revenue')
    elif "Prime" in select_metric: 
        st.markdown('#### Top Prime Products by Minimum Revenue')
    elif "Past" in select_metric: 
        st.markdown('#### Top Products with Past Month Sales Info by Minimum Revenue')
    elif 'Discounted' in select_metric: 
        st.markdown('#### Top Products with Price Strikethrough by Minimum Revenue')
    else: 
        st.markdown('#### Top Products by Minimum Revenue')
        
    if len(unique) > 1000: val = 1000
    else: val = len(unique)
    topK = st.number_input(
            'Enter a value for K:',
            min_value=1, max_value=len(unique), value=val, step=100,key="table")
    top_df = unique.head(topK)
    st.markdown(f'Top {len(top_df)} out of {len(unique)} Total Products')
    st.dataframe(top_df,
                column_order=("Title", "Minimum_Revenue", "Price","Currency","Sponsored","Rating","Reviews_Count","Best_Seller","Sales_Volume_Past_Month","Prime","Price_Strikethrough","Discount","Discount_Rate","Keyword","Search_Term", "Position","ASIN","URL","Image_URL"),
                hide_index=True,
                width=None,
                column_config={
                    "Minimum_Revenue": st.column_config.ProgressColumn(
                        "Minimum_Revenue",
                        format="%f",
                        min_value=min(df.Minimum_Revenue),
                        max_value=max(df.Minimum_Revenue),
                    ),
                    "Sponsored": st.column_config.TextColumn("Paid Search Result",),
                    "Search_Term": st.column_config.TextColumn("Search Phrases",),
                    "Search_Term": st.column_config.TextColumn("Search Keywords",),
                    "URL": st.column_config.LinkColumn("View Detailed Product Page"),
                    "Image_URL": st.column_config.LinkColumn("View Product Image")
                    }
                    
                )
    
    with st.expander('About', expanded=True):
        st.markdown('''
            - Data: [**Amazon**](amazon.com) using [Oxylab's E-Commerce Scraper API](https://oxylabs.io/products/scraper-api/ecommerce/amazon). Of the scraped results, only products with at least one review are included for analysis. 
            - :blue[**Search Phrases**] and :blue[**Position**]: The relevant search phrases and the product's positions in the search results for those phrases (across all pages) are divided respectively by semicolons. These phrases are among those with the highest search volume associated with more general key terms (**Search Keywords**) based on [Keyword Tool](https://keywordtool.io/).
            - :blue[**Revenue**]: Price multiplied by the count of reviews. 
            - :blue[**Past Month Sales**]: These are products which have approximate sales information for the past month, e.g., "2K+ bought in past month."
            - :blue[**Organic**]: These are the non-sponsored search results returned for a query. 
            - :blue[**Sponsored/Paid**]: These are the paid advertisements among the results that are returned for a query. 
            ''')
    

with col[0]: 
    if "Frequent Phrases" in select_metric: 
        # if 1000 < len(all_df): val = 1000
        # else: val = len(all_df)
        # topK = st.number_input(
        #     'Enter a value for K:',
        #     min_value=1, max_value=len(all_df), value=val, step=100,key="phrases")
        st.markdown(f'#### Frequent Phrases in Titles for the Top {topK} Products')
        frequencies = wordcloud(topK)
        st.write(f"Top {len(frequencies)} phrases")
        frequencies = pd.DataFrame.from_dict(frequencies, orient='index').reset_index()
        frequencies.columns = ['Phrase', 'Frequency']
        frequencies = frequencies.sort_values(by=['Frequency','Phrase'], ascending=[False,True])
        frequencies.reset_index(drop=True, inplace=True)
        st.dataframe(frequencies,width=None)
        st.markdown(f'#### Frequent Search Terms for the Top {topK} Products')
        terms = bar_searchterms(topK)
        terms = pd.DataFrame.from_dict(terms, orient='index').reset_index()
        terms.columns = ['Search Phrase', 'Frequency']
        terms = terms.sort_values(by=['Frequency','Search Phrase'], ascending=[False,True])
        terms.reset_index(drop=True, inplace=True)
        st.dataframe(terms,width=None)
    else: 
        st.markdown(f'#### {select_metric}')
        st.markdown('Average')
        bar_metric(select_metric)
        st.markdown('Median')
        bar_metric(select_metric,"Median")
        # if select_metric in ["Minimum_Revenue","Price","Rating","Reviews_Count"]:
        #     histogram(select_metric)
        # elif 'Strikethrough' in select_metric: 
            # relevant = stats[stats.Keyword==selected_category]
            # discounts = relevant[relevant.Title == "Amount Discounted"]
            # percents = relevant[relevant.Title == "Percentage Discounted"]
            # toprint = discounts
            # toprint = discounts.update(percents)
            # st.write(toprint)
        # relevant = stats[stats.Keyword==selected_category.lower()]
        # st.dataframe(relevant,
        #     column_order=("Title", "Type", "Mean","Median","Mode","Mode Freq","Max","Min","Percentile25","Percentile75"),
        #     hide_index=True
        # )
