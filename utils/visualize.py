#######################
from .translation import *
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

original_cmap = plt.cm.Blues
n_colors = 256
colors = original_cmap(np.linspace(0, 1, n_colors))
darkening_factor = 0.6
colors[-n_colors//5:] *= darkening_factor
colors = np.clip(colors, 0, 1)
darkened_cmap = LinearSegmentedColormap.from_list('darkened_blues', colors)
#######################

ngram_types = {'Unigram':1,'Trigram':3,'Bigram':2,'4-Gram': 4}

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


    
#######################
