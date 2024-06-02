#######################
import streamlit as st
import pandas as pd
import numpy as np 
import altair as alt
import plotly.express as px
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
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
    metrics = {}

    if selected_category == 'All': 
        df = products
        for term in stats.Title: 
            if term not in metrics: metrics[term] = None 
        metrics['Frequent Phrases'] = None 
    else: 
        df = products[products.Keyword == selected_category.lower()]
        # select_searchterm = st.selectbox('Select a search term associated with the keyword above', searchterms)
        # df = df[df.Search_Term == select_searchterm]
        # metrics = ["Frequent Phrases","Minimum_Revenue","Price","Rating","Reviews_Count","Best_Seller","Sales_Volume_Past_Month","Prime","Price Strikethrough"]
        # metrics = ["Frequent Phrases","Minimum Revenue","Prices","Feedback","Amount Discounted","Percentage Discounted"]
        metrics = ["Frequent Phrases","Aggregate Statistics"]
    select_metric = st.selectbox('Select a metric for visualization', metrics)
    
#######################

def bar_mean(title): 
    if selected_category == "All": 
        data = stats[stats.Title == title]
        data = data.sort_values(by=['Mean','Type','Keyword'], ascending=[False,False,True])
        chart = alt.Chart(data).mark_bar(opacity=0.7).encode(
            x=alt.X('Keyword:O', axis=alt.Axis(labelAngle=90), title='Keyword'),  
            y=alt.Y('Mean:Q', title=f"Average {title}").stack(None),
            color=alt.Color('Type:N', legend=alt.Legend(title="Type of Search Result",orient="bottom"))  
        )
    else: 
        relevant = stats[stats.Keyword==selected_category.lower()]
        # if title == 'Minimum Revenue': 

    st.altair_chart(chart, use_container_width=True)

def bar_median(title): 
    data = stats[stats.Title == title]
    data = data.sort_values(by=['Median','Type','Keyword'], ascending=[False,False,True])
    chart = alt.Chart(data).mark_bar(opacity=0.7).encode(
        x=alt.X('Keyword:O', axis=alt.Axis(labelAngle=90), title='Keyword'),  
        y=alt.Y('Median:Q', title=f"Median {title}").stack(None),
        color=alt.Color('Type:N', legend=alt.Legend(title="Type of Search Result",orient="bottom"))  
    )
    st.altair_chart(chart, use_container_width=True)

def bar_searchterms(topK): 
    data = df
    terms = []
    for term in data.Search_Term.head(topK): 
        terms.extend(term.split("; "))
    terms = Counter(terms).most_common(n=50)
    chart = pd.DataFrame({
        'Search Term': [x[0] for x in terms],
        'Frequency': [x[1] for x in terms]
    }
    )
    chart = chart.sort_values(by='Frequency',ascending=True)
    fig = px.bar(chart, x='Frequency', y='Search Term', orientation='h')
    st.plotly_chart(fig)


def wordcloud(n):
    data = df.Title.head(n)
    # all_ngrams = []
    # for string in data:
    #     tokens = nltk.word_tokenize(string)
    #     for i in range(n): 
    #         ngrams_list = list(ngrams(tokens, i))
    #         ngrams_list = ['_'.join(gram) for gram in ngrams_list]
    #     all_ngrams.extend(ngrams_list)
    # data = " ".join(all_ngrams)
    data = " ".join(data)
    wordcloud = WordCloud(width=1600, height=800, background_color='white',colormap='winter').generate(data)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    # word_frequencies = pd.DataFrame(list(wordcloud.words_.items()), columns=['Word', 'Frequency'])
    # word_frequencies = word_frequencies.sort_values(by=['Frequency','Word'], ascending=[False,True])
    # st.write("Word Frequencies:")
    # st.dataframe(word_frequencies)
    
def histogram(title): 
    data = df[title]
    fig = px.histogram(data, nbins=30, labels={'value': 'Value', 'count': 'Frequency'})
    st.plotly_chart(fig)
     
#######################
col = st.columns((4, 5), gap='large')
with col[0]: 

    if select_metric == "Frequent Phrases": 
        if 1000 < len(df): val = 1000
        else: val = len(df)
        topK = st.number_input(
            'Enter a value for K:',
            min_value=1, max_value=len(df), value=val, step=100)
        st.markdown('#### Frequent Phrases in Titles for the Top K Products')
        wordcloud(topK)
        st.markdown('#### Frequent Search Terms for the Top K Products')
        bar_searchterms(topK)
    else: 
        st.markdown(f'#### {select_metric}')
        if selected_category == "All": 
            st.markdown('Average')
            bar_mean(select_metric)
            st.markdown('Median')
            bar_median(select_metric)
        else: 
            # if select_metric in ["Minimum_Revenue","Price","Rating","Reviews_Count"]:
            #     histogram(select_metric)
            # elif 'Strikethrough' in select_metric: 
                # relevant = stats[stats.Keyword==selected_category]
                # discounts = relevant[relevant.Title == "Amount Discounted"]
                # percents = relevant[relevant.Title == "Percentage Discounted"]
                # toprint = discounts
                # toprint = discounts.update(percents)
                # st.write(toprint)
            relevant = stats[stats.Keyword==selected_category.lower()]
            st.dataframe(relevant,
                column_order=("Title", "Type", "Mean","Median","Mode","Mode Freq","Max","Min","Percentile25","Percentile75"),
                hide_index=True
            )

with col[1]:
    if "Best" in select_metric: 
        st.markdown('#### Top Best Sellers by Minimum Revenue')
        all_df = df[df.Best_Seller == True]
    elif "Prime" in select_metric: 
        st.markdown('#### Top Prime Products by Minimum Revenue')
        all_df = df[df.Prime == True]
    elif "Past" in select_metric: 
        st.markdown('#### Top Products with Past Month Sales Info by Minimum Revenue')
        all_df = df[df['Sales_Volume_Past_Month'].notnull()]
    elif "Discount" in select_metric or 'Strikethrough' in select_metric: 
        st.markdown('#### Top Products with Price Strikethrough by Minimum Revenue')
        all_df = df[df['Discount'].notnull()]
    else: 
        st.markdown('#### Top Products by Minimum Revenue')
        all_df = df

    if 1000 < len(df): val = 1000
    else: val = len(df)
    topK = st.number_input(
            'Enter a value for K:',
            min_value=1, max_value=len(df), value=val, step=100)
    top_df = all_df.head(topK)
    st.markdown(f'Top {len(top_df)} out of {len(all_df)} Total Products')
    st.dataframe(top_df,
                column_order=("Title", "Minimum_Revenue", "Price","Currency","Sponsored","Rating","Reviews_Count","Best_Seller","Sales_Volume_Past_Month","Prime","Price_Strikethrough","Discount","Discount_Rate","Search_Term", "Position","ASIN","URL","Image_URL"),
                hide_index=True,
                width=None,
                column_config={
                    "Minimum_Revenue": st.column_config.ProgressColumn(
                        "Minimum_Revenue",
                        format="%f",
                        min_value=min(df.Minimum_Revenue),
                        max_value=max(df.Minimum_Revenue),
                    ),
                    "Sponsored": st.column_config.TextColumn("Paid Search Result",)
                    }
                    
                )
    
    with st.expander('About', expanded=True):
        st.write('''
            - Data: [**Amazon**](amazon.com) using [Oxylab's E-Commerce Scraper API](https://oxylabs.io/products/scraper-api/ecommerce/amazon). Of the scraped results, only products with at least one review are included for analysis. 
            - :blue[**Search Term**] and :blue[**Position**]: The relevant search terms and the product's positions in the search results for those terms (across all pages) are divided respectively by semicolons. These terms are among those with the highest search volume associated with more general key terms based on [Keyword Tool](https://keywordtool.io/).
            - :blue[**Revenue**]: Price multiplied by the count of reviews. 
            - :blue[**Past Month Sales**]: These are products which have approximate sales information for the past month, e.g., "2K+ bought in past month."
            ''')
        
    
    
