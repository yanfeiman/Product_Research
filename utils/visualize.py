#######################
from PRODUCT_APP.app.models.translation import *
from app import Text,langcode
import streamlit as st
import pandas as pd
import numpy as np 
import altair as alt
import plotly.express as px
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from nltk.util import ngrams
import string 
original_cmap = plt.cm.Blues
n_colors = 256
colors = original_cmap(np.linspace(0, 1, n_colors))
darkening_factor = 0.6
colors[-n_colors//5:] *= darkening_factor
colors = np.clip(colors, 0, 1)
darkened_cmap = LinearSegmentedColormap.from_list('darkened_blues', colors)
#######################

ngram_types = {'Unigram':1,'Trigram':3,'Bigram':2,'4-Gram': 4}
 
# if "Title" in select_metric:
#     if langcode != "zh":  
#         st.markdown(f'#### Frequent Phrases in Titles for the Top {topK} Products')
#     else: 
#         st.markdown(f'#### 排名前 {topK} 产品标题中的常见短语')
    
#     n = st.selectbox(Text('Select a type of n-gram'), [Text('Unigram'),Text('Bigram'),Text('Trigram'),Text('4-Gram')],index=2)
#     n = Text(n)
#     frequencies = self.wordcloud(topK,ngram_types[n])
#     if langcode != "zh":
#         st.write(f"Top {len(frequencies)} N-grams")
#     else: 
#         st.write(f"一共 {len(frequencies)} 个符串")
#     frequencies = pd.DataFrame.from_dict(frequencies, orient='index').reset_index()
#     frequencies.columns = [Text('N-gram'), Text('Frequency')]
#     frequencies = frequencies.sort_values(by=[Text('Frequency'),Text('N-gram')], ascending=[False,True])
#     frequencies.reset_index(drop=True, inplace=True)
#     st.dataframe(frequencies,width=None)

# elif "Search Phrases" in select_metric:
#     if langcode != "zh":  
#         st.markdown(f'#### Frequent Search Terms for the Top {topK} Products')
#     else: 
#         st.markdown(f'#### 排名前 {topK} 产品标题中的常见相关搜索短语')
#     terms = self.bar_searchterms(topK)
#     terms = pd.DataFrame.from_dict(terms, orient='index').reset_index()
#     terms.columns = [Text('Search Phrase'), Text('Frequency')]
#     terms = terms.sort_values(by=[Text('Frequency'),Text('Search Phrase')], ascending=[False,True])
#     terms.reset_index(drop=True, inplace=True)
#     st.dataframe(terms,width=None)
# else: 
#     st.markdown(f'#### {select_metric_orig}')
#     st.markdown(Text('Average'))
#     self.bar_metric(select_metric)
#     st.markdown(Text('Median'))
#     self.bar_metric(select_metric,"Median")

#######################
def bar_metric(title,stats,selected_category=None,metric="Mean"): 
    if selected_category is None: 
        ptype,title = title.split(" - ")
        data = stats[stats.Title == title]
        data = data[data["Product Type"] == ptype]
        data = data.sort_values(by=[metric,'Search Type','Keyword'], ascending=[False,False,True])
        kw_map = {w:Text(w) for w in data["Keyword"]}
        data["Keyword"] = data["Keyword"].map(kw_map)
        p_map = {w:Text(w) for w in data["Product Type"]}
        data["Product Type"] = data["Product Type"].map(p_map)
        data['Search Type'] = data["Search Type"].map({"Organic":Text("Organic"),"Paid":Text("Paid")})
        chart = alt.Chart(data).mark_bar(opacity=0.7).encode(
            x=alt.X('Keyword:O', axis=alt.Axis(labelAngle=90), title=Text('Keyword')),  
            y=alt.Y(f'{metric}:Q', title=f"{Text(title)}").stack(None),
            color=alt.Color('Search Type:N', title= Text("Search Type"), legend=alt.Legend(title=Text("Type of Search Result"),orient="bottom"))  
        )
    else: 
        data = stats[stats.Title == title]
        data = data[data.Keyword == selected_category.lower()]
        data = data.sort_values(by=[metric,'Search Type','Product Type'], ascending=[False,False,True])
        kw_map = {w:Text(w) for w in data["Keyword"]}
        data["Keyword"] = data["Keyword"].map(kw_map)
        p_map = {w:Text(w) for w in data["Product Type"]}
        data["Product Type"] = data["Product Type"].map(p_map)
        data['Search Type'] = data["Search Type"].map({"Organic":Text("Organic"),"Paid":Text("Paid")})
        chart = alt.Chart(data).mark_bar(opacity=0.7).encode(
            x=alt.X(f'{metric}:Q', axis=alt.Axis(labelAngle=0), title=Text(title)).stack(None),  
            y=alt.Y('Product Type:O',title=Text('Product Type')),
            color=alt.Color('Search Type:N', title=Text("Search Type"),legend=alt.Legend(title=Text("Type of Search Result"),orient="bottom"))  
        )
    st.altair_chart(chart, use_container_width=True)


def bar_searchterms(data,topK): 
    terms = []
    for term in data.keyword.head(topK): 
        terms.extend(term.split("; "))
    terms = Counter(terms)
    topterms = Counter(terms).most_common(n=25)
    chart = pd.DataFrame({
        Text('Search Phrase'): [x[0] for x in topterms],
        Text('Frequency'): [x[1] for x in topterms]
    }
    )
    chart = chart.sort_values(by=Text('Frequency'),ascending=True)
    fig = px.bar(chart, x=Text('Frequency'), y= Text('Search Phrase'), orientation='h')
    st.plotly_chart(fig)
    return terms

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
    
#######################
