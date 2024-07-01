#######################
import streamlit as st
from translation import *
from st_pages import Page, show_pages, add_page_title
#######################
# add_page_title()

show_pages(
    [
        Page("About.py", Text("About")),
        Page("pages/Jewelry.py", Text("Jewelry")),
        Page("pages/Nails.py", Text("Nails")),
    ]
)

with st.sidebar:
    lang = st.selectbox('选择语言/Select Language： ', ["简体中文/Chinese (simplified)","英文/English"], index=0)
    if lang == "英文/English":
        langcode = "en"
    else: 
        langcode = "zh"

st.write(f"## {Text('Analytics for Product Research')}")

st.markdown("""
<style>
    .stSelectbox:first-of-type > div[data-baseweb="select"] > div {
	    background-color: white;
    	padding: 2px;
        border: none;
	}
    
    section[data-testid="stSidebar"] {
            width: 100px;
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

st.markdown(
    f"""
    {Text("This app provides aggregate statistics for product data from searches on [**Amazon**](amazon.com). Only products with at least one review are included for analysis.")} 
    
    {Text("Browse already collected data on these pages linked below and in the left sidebar:")} 
    - [{Text("Jewelry")}](https://beauty.streamlit.app/{Text("Jewelry")})
    - [{Text("Nails")}](https://beauty.streamlit.app/{Text("Nails")})

    """
)

with st.expander(Text('Explanation of Terms'), expanded=True):
        st.markdown(f'''
            - :blue[**{Text("Search Phrase")}**] and :blue[**{Text("Position")}**]: {Text("The relevant search phrases and the product's positions in the search results for those phrases (across all pages) are divided respectively by semicolons. These phrases are among those with the highest search volume associated with general categories based on [Keyword Tool](https://keywordtool.io/).")}
            - :blue[**{Text("Revenue")}**]: {Text("To estimate the minimum revenue for a product, we multiply price by the count of reviews.")}
            - :blue[**{Text("Past Month Sales Volume")}**]: {Text("These are products which have approximate sales information for the past month, e.g., '2K+ bought in past month.'")}
            - :blue[**{Text("Organic Search Result")}**]: {Text("These are the non-sponsored search results returned for a query.")} 
            - :blue[**{Text("Paid Search Result")}**]: {Text("These are the sponsored results that are returned for a query.")} 
            ''')
# ### See more complex demos
    # - Use a neural net to [analyze the Udacity Self-driving Car Image
    #     Dataset](https://github.com/streamlit/demo-self-driving)
    # - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)

