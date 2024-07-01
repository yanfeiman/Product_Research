#######################
from translation import * 
import streamlit as st
import json 
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

class Dashboard(): 
    def __init__(self, title, allterms, products, stats):
        self.allterms = allterms
        self.products = products
        self.stats = stats 

        ##############################
        with st.sidebar: 
            st.title(title)
            # a category of products 

            categories = [Text('All')]
            categories.extend([term.capitalize() for term in allterms])
            selected_category = st.selectbox(Text('Select a keyword for a category of products'), categories)
            selected_category = Text(selected_category)
            self.selected_category = selected_category

            if selected_category == 'All': 
                df = products
                metrics = {}
                for idx, term in enumerate(stats.Title):
                    p_type = stats['Product Type'][idx]
                    term = f"{Text(p_type)} - {Text(term)}" 
                    if term not in metrics: metrics[term] = None 
                    if f"{Text(p_type)} - {Text("Search Phrases")}" not in metrics: 
                        metrics[f"{Text(p_type)} - {Text("Search Phrases")}"] = None 
                    if f"{Text(p_type)} - {Text("Titles")}" not in metrics: 
                        metrics[f"{Text(p_type)} - {Text("Titles")}"] = None 
            else: 
                df = products[products.Keyword == selected_category.lower()]
                metrics = [Text("Revenue"),Text("Price"),Text("Rating"),Text("Reviews Count"),
                        Text("Amount Discounted"),Text("Percent Discounted"),
                        Text("Search Phrases"),Text("Titles")]
            
            select_metric_orig = st.selectbox(Text('Select a metric for visualization'), metrics)
            select_metric = [Text(_) for _ in select_metric_orig.split(" - ")]
            select_metric = " - ".join(select_metric)

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
        unique = {}
        for info in all_prod: 
            if info["ASIN"] not in unique: 
                unique[info["ASIN"]] = info
            else: 
                unique[info["ASIN"]]["Keyword"] = str(unique[info["ASIN"]]["Keyword"]) + "; " + str(info["Keyword"])
                unique[info["ASIN"]]["Search_Term"] = str(unique[info["ASIN"]]["Search_Term"]) + "; " + str(info["Search_Term"])
                unique[info["ASIN"]]["Position"] = str(unique[info["ASIN"]]["Position"]) + "; " + str(info["Position"])
        unique = pd.DataFrame(unique.values())
        self.unique = unique 
        ##############################3
        col = st.columns((4, 5), gap='large')

        with col[1]:

            if "Best" in select_metric: 
                st.markdown(f'#### {Text("Top Best Sellers by Minimum Revenue")}')
            elif "Prime" in select_metric: 
                st.markdown(f'#### {Text("Top Prime Products by Minimum Revenue")}')
            elif "Past" in select_metric: 
                st.markdown(f'#### {Text("Top Products with Past Month Sales Info by Minimum Revenue")}')
            elif 'Discounted' in select_metric: 
                st.markdown(f'#### {Text("Top Products with Price Strikethrough by Minimum Revenue")}')
            else: 
                st.markdown(f'#### {Text("Top Products by Minimum Revenue")}')
                
            if len(unique) > 150: val = 150
            else: val = len(unique)
            topK = st.number_input(
                    Text('To display the top K products, enter a value for K:'),
                    min_value=1, max_value=len(unique), value=val, step=100,key="table")
            top_df = unique.head(topK)
            if langcode != "zh":
                st.markdown(f'Top {len(top_df)} out of {len(unique)} Total Products')
            else: 
                st.markdown(f'产品总数 {len(unique)} 个中的前 {len(top_df)} 个')
                
            st.dataframe(top_df,
                        column_order=("Title", "Minimum_Revenue", "Price","Currency","Sponsored",
                                    "Rating","Reviews_Count","Best_Seller","Sales_Volume_Past_Month",
                                    "Prime","Price_Strikethrough","Discount","Discount_Rate",
                                    "Keyword","Search_Term", "Position","ASIN","URL","Image_URL"),
                        hide_index=True,
                        width=None,
                        column_config={
                            "Minimum_Revenue": st.column_config.ProgressColumn(
                                Text("Minimum_Revenue"),
                                format="%f",
                                min_value=min(df.Minimum_Revenue),
                                max_value=max(df.Minimum_Revenue),
                            ),
                            "Title": st.column_config.TextColumn(Text("Title")),
                            "Price": st.column_config.TextColumn(Text("Price")),
                            "Currency": st.column_config.TextColumn(Text("Currency")),
                            "Rating": st.column_config.TextColumn(Text("Rating")),
                            "Reviews_Count": st.column_config.TextColumn(Text("Reviews_Count")),
                            "Prime": st.column_config.CheckboxColumn(Text("Prime")),
                            "Price_Strikethrough": st.column_config.TextColumn(Text("Price_Strikethrough")),
                            "Keyword": st.column_config.TextColumn(Text("Keyword")),

                            "Best_Seller": st.column_config.CheckboxColumn(Text("Best Seller")),
                            "Sales_Volume_Past_Month": st.column_config.TextColumn(Text("Past Month Sales Volume")),
                            "Discount": st.column_config.TextColumn(Text("Amount Discounted")),
                            "Discount_Rate": st.column_config.TextColumn(Text("Percent Discounted")),
                            "Sponsored": st.column_config.CheckboxColumn(Text("Paid Search Result")),
                            "Search_Term": st.column_config.TextColumn(Text("Search Phrase")),
                            "Position": st.column_config.TextColumn(Text("Position")),
                            "URL": st.column_config.LinkColumn(Text("View Detailed Product Page")),
                            "Image_URL": st.column_config.LinkColumn(Text("View Product Image"))
                            }
                            
                        )
            
            
        ngram_types = {'Unigram':1,'Trigram':3,'Bigram':2,'4-Gram': 4}
        with col[0]: 
            if "Title" in select_metric:
                if langcode != "zh":  
                    st.markdown(f'#### Frequent Phrases in Titles for the Top {topK} Products')
                else: 
                    st.markdown(f'#### 排名前 {topK} 产品标题中的常见短语')
                
                n = st.selectbox(Text('Select a type of n-gram'), [Text('Unigram'),Text('Bigram'),Text('Trigram'),Text('4-Gram')],index=2)
                n = Text(n)
                frequencies = self.wordcloud(topK,ngram_types[n])
                if langcode != "zh":
                    st.write(f"Top {len(frequencies)} N-grams")
                else: 
                    st.write(f"一共 {len(frequencies)} 个符串")
                frequencies = pd.DataFrame.from_dict(frequencies, orient='index').reset_index()
                frequencies.columns = [Text('N-gram'), Text('Frequency')]
                frequencies = frequencies.sort_values(by=[Text('Frequency'),Text('N-gram')], ascending=[False,True])
                frequencies.reset_index(drop=True, inplace=True)
                st.dataframe(frequencies,width=None)
            
            elif "Search Phrases" in select_metric:
                if langcode != "zh":  
                    st.markdown(f'#### Frequent Search Terms for the Top {topK} Products')
                else: 
                    st.markdown(f'#### 排名前 {topK} 产品标题中的常见相关搜索短语')
                terms = self.bar_searchterms(topK)
                terms = pd.DataFrame.from_dict(terms, orient='index').reset_index()
                terms.columns = [Text('Search Phrase'), Text('Frequency')]
                terms = terms.sort_values(by=[Text('Frequency'),Text('Search Phrase')], ascending=[False,True])
                terms.reset_index(drop=True, inplace=True)
                st.dataframe(terms,width=None)
            else: 
                st.markdown(f'#### {select_metric_orig}')
                st.markdown(Text('Average'))
                self.bar_metric(select_metric)
                st.markdown(Text('Median'))
                self.bar_metric(select_metric,"Median")

    #######################
    def bar_metric(self,title,metric="Mean"): 
        if self.selected_category == "All": 
            ptype,title = title.split(" - ")
            data = self.stats[self.stats.Title == title]
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
            data = self.stats[self.stats.Title == title]
            data = data[data.Keyword == self.selected_category.lower()]
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


    def bar_searchterms(self,topK): 
        data = self.unique
        terms = []
        for term in data.Search_Term.head(topK): 
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

    def wordcloud(self,topK,n):
        data = self.unique.Title.head(topK)
        all_ngrams = []
        for item in data:
            translator = str.maketrans('', '', string.punctuation)
            item = item.translate(translator)
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
        
    # def histogram(title): 
    #     data = unique[title]
    #     fig = px.histogram(data, nbins=30, labels={'value': 'Value', 'count': 'Frequency'})
    #     st.plotly_chart(fig)
        
    #######################
