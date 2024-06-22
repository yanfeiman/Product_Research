import streamlit as st

st.set_page_config(
    page_title="About",
    # page_icon="👋",
)

st.write("# Analytics for Product Research")

# st.sidebar.success("Browse a page above.")
st.markdown("""
<style>
    .stSelectbox:first-of-type > div[data-baseweb="select"] > div {
	    background-color: white;
    	padding: 10px;
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
# header {visibility: hidden;}

st.markdown(
    """
    This app provides aggregate statistics for product data on [**Amazon**](amazon.com) and [**Etsy**](etsy.com) collected using [**Oxylabs' E-Commerce Scraper API**](https://oxylabs.io/products/scraper-api/ecommerce/amazon). Of the scraped results, only products with at least one review are included for analysis. 

    Browse already collected data on these pages linked below and in the left sidebar: 
    - [Jewelry](https://beauty.streamlit.app/)
    - [Nails](https://beauty.streamlit.app/)

"""
)
# ### See more complex demos
    # - Use a neural net to [analyze the Udacity Self-driving Car Image
    #     Dataset](https://github.com/streamlit/demo-self-driving)
    # - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)