
langcode = "zh" 

def Text(string): 
    if langcode == "zh" and string in en_to_zh: 
        return en_to_zh[string]
    elif langcode == "zh" and string in zh_to_en:
        return zh_to_en[string]
    else: 
        return string

en_to_zh = {
    "About":"介绍",
    "Analytics for Product Research":"产品研究分析",
    "This app provides aggregate statistics for product data from searches on [**Amazon**](amazon.com) collected using [**Oxylabs' E-Commerce Scraper API**](https://oxylabs.io/products/scraper-api/ecommerce/amazon). Of the scraped results, only products with at least one review are included for analysis.":
    "本应用软件提供了使用[**Oxylabs' E-Commerce Scraper API**](https://oxylabs.io/products/scraper-api/ecommerce/amazon)收集的[**Amazon**](amazon.com)亚马逊产品搜索的数据统计. 被收集数据的产品每一个至少被一个用户评论过。",
    "This app provides aggregate statistics for product data from searches on [**Amazon**](amazon.com). Only products with at least one review are included for analysis.":
    "本应用软件提供了[**Amazon**](amazon.com)亚马逊产品搜索的数据统计. 被收集数据的产品每一个至少被一个用户评论过。",
    "Browse already collected data on these pages linked below and in the left sidebar:":
    "浏览在下面和左侧栏链接的这些页面上已经收集的数据:",
    "Jewelry":"珠宝首饰",
    "Nails":"美甲",
    "Explanation of Terms":"术语解释",
    "Search Phrase":"搜索短语",
    "Phrase":"短语",
    "Frequency":"次数",
    "Position":"位置",
    "Revenue":"收入",
    "Past Month Sales Volume":"上月销售量",
    "Organic Search Result":"自然搜索结果",
    "Paid Search Result":"赞助商搜索结果",
    "Organic":"自然",
    "Paid":"赞助商",
    "The relevant search phrases and the product's positions in the search results for those phrases (across all pages) are divided respectively by semicolons. These phrases are among those with the highest search volume associated with general categories based on [Keyword Tool](https://keywordtool.io/).":
    "相关搜索短语和产品在这些短语的搜索结果中的总位置在数据表中分别用分号隔开。根据[Keyword Tool](https://keywordtool.io/)，这些短语属于与一般类别相关的搜索量最高的短语。",
    "To estimate the minimum revenue for a product, we multiply price by the count of reviews.":
    "为了估算产品的最低收入，我们用价格乘以评论数",
    "These are products which have approximate sales information for the past month, e.g., '2K+ bought in past month.'":
    "这些产品有上个月的大致销售信息，例如 '上个月购买量超过2K'",
    "These are the non-sponsored search results returned for a query.":
    "这些是针对查询返回的非赞助商搜索结果。",
    "These are the sponsored results that are returned for a query.":
    "这些是针对查询返回的赞助结果。",
    "Amazon Jewelry Dashboard":"亚马逊珠宝仪表盘",
    "Amazon Nails Dashboard":"亚马逊美甲仪表盘",
    "Select a keyword for a category of products":"选择产品类别的关键词",
    "Select a metric for visualization":"选择可视化指标",
    "Top Best Sellers by Minimum Revenue":"按最低收入排序的最畅销产品",
    "Top Prime Products by Minimum Revenue":"按最低销售额排列的Prime产品",
    "Top Products with Past Month Sales Info by Minimum Revenue":"按最低收入排列的带有上个月销售量的产品",
    "Top Products with Price Strikethrough by Minimum Revenue":"按最低收入排列的带价格变动的产品",
    "Top Products by Minimum Revenue":"按最低收入排序的产品",
    "To display the top K products, enter a value for K:":"要显示 K 排序最高的产品，请输入 K 值：",
    "Select a type of n-gram":"选择符串类型",
    'N-gram':"符串",
    'Unigram':"单字符串",
    'Bigram':"双字符串",
    'Trigram':"三字符串",
    '4-Gram':"四字符串",
    "Type of Search Result":"搜索结果类型",
    'Product Type':"产品类型",
    "Average":"平均数",
    "Median":"中位数",
    "Best Seller":"畅销",
    "Prime":"亚马逊Prime",
    "Rating": "评级", 
    "Reviews Count": "评论数", 
    "Amount Discounted": "折扣金额", 
    "Percent Discounted": "折扣百分比", 
    "Search Phrases":"搜索短语",
    "Titles":"标题",

    'Title': '标题',
    'Minimum_Revenue': '最低收入', 
    'Price': '价格', 
    'Currency': '货币', 
    'Sponsored': '赞助商', 
    'Reviews_Count': '评论数',  
    'Price_Strikethrough': '价格变动', 
    'Keyword': '产品类别的关键词', 
    'View Product Image': '查看产品图片', 
    "View Detailed Product Page": '查看详细产品页面',
    
    ## JEWELRY 
    "All":"全部",
    "earrings": "耳环", 
    "birthstone": "诞生石", 
    "peridot": "橄榄石", 
    "necklace": "项链", 
    "amethyst": "紫水晶", 
    "cubic zirconia": "立方氧化锆", 
    "aquamarine": "海蓝宝石", 
    "sterling silver": "纯银", 
    "moonstone": "月光石", 
    "pearl": "珍珠", 
    "moissanite": "莫桑石", 
    "lapis lazuli": "青金石", 
    "rings": "戒指", 
    "smoky quartz": "烟晶", 
    "aura quartz": "灵气石英", 
    "turquoise": "绿松石", 
    "topaz": "黄玉", 
    "garnet": "石榴石", 
    "jade": "翡翠", 
    "citrine": "黄水晶", 
    "rose quartz": "玫瑰石英", 
    "tourmaline": "碧玺", 
    "clear quartz": "透明石英", 
    "calcite": "方解石", 
    "opalite": "蛋白石", 
    "sunstone": "太阳石", 
    "tiger's eye": "虎眼石", 
    "moldavite": "模长石", 
    "shungite": "霰石", 
    "orgone": "斲丧石", 
    "obsidian": "黑曜石", 
    "fluorite": "萤石", 
    "hematite": "赤铁矿", 
    "carnelian": "红玉髓",
    "selenite": "硒石", 
    "agate": "玛瑙", 
    "black agate": "黑玛瑙", 
    "jasper": "碧玉", 
    "black jasper": "黑碧玉", 
    "lepidolite": "鳞片石", 
    "aventurine": "砂金石", 
    "malachite": "孔雀石", 
    "blue lace agate": "蓝蕾丝玛瑙", 
    "labradorite": "拉长石",

    #### NAILS 
    'nail':'指甲','nail polish':'指甲油','press on nails':'按压式指甲','nail stickers':'指甲贴纸'
}

zh_to_en = {v:k for k,v in en_to_zh.items()}
