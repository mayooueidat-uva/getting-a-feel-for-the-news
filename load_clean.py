import requests
import time
import duckdb
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from prefect import task, flow
import matplotlib.pyplot as plt
import textwrap
import logging

#import os

# configuring the logging mechanism
logging.basicConfig(
    filename='load.log',
    filemode="a",
    style="{", 
    datefmt="%Y-%m-%d-%H:%M:%x", 
    level="INFO"
)
logger = logging.getLogger(__name__)


# fetching secret key from our environment.
# of course i'm not committing it to this repo
#my_api_key = os.environ.get("9f2cea00198d4c24955ae9d517cf77fe")

# list of news source names for the API to call from
news_source_names = ["cnn", "fox-news", "the-wall-street-journal", "abc-news", "associated-press",
"cbs-news", "the-huffington-post", "breitbart-news", "msnbc", "the-american-conservative",
                    "the-verge", "national-review"]

# path to our database, where our sql tables will be located
db_path = "DS4320_project1.duckdb"

# defining load function 
def load_relevant_data():
    con = duckdb.connect(db_path)
    logger.info("connected to duckdb instance.") 
    try: 
        # create SQL table for news articles and their headlines
        con.execute(f"""
                    CREATE TABLE IF NOT EXISTS NEWS_ARTICLES_TEST_3(
                        source_id VARCHAR,
                        source_name VARCHAR,
                        article_title VARCHAR,
                        article_pubdate TIMESTAMP, 
                        article_url VARCHAR
                    )
                    """)
        logger.info("created empty SQL table for news article details.") 
        
        # creating SQL table for each news source and reliability scores and bias scores
        con.execute(f"""
                    CREATE TABLE IF NOT EXISTS SOURCE_AND_RELIABILITY_TEST_3(
                    source_id VARCHAR, 
                    source_bias DOUBLE,
                    source_reliability DOUBLE, 
                    reliability_threshold_diff DOUBLE, 
                    unreliability_threshold_diff DOUBLE 
                    )
                    """)
        logger.info("created empty SQL table for news source bias/reliability details.") 
       
        # creating SQL table for the sentiments in article headlines
        con.execute(f"""
                    CREATE TABLE IF NOT EXISTS HEADLINE_SENTIMENTS_TEST_3(
                    source_id VARCHAR, 
                    article_title VARCHAR, 
                    title_sentiment DOUBLE
                    )
                    """)
        logger.info("created empty SQL table for headline sentiment details.") 

        # creating SQL table for source identificatory details
        con.execute(f"""
                    CREATE TABLE IF NOT EXISTS SOURCE_NAME_ID_TEST_3(
                    source_id VARCHAR, 
                    source_name VARCHAR, 
                    source_url VARCHAR
                    )
                    """)
        logger.info("created SQL table for news sources' identificatory details.") 
        
        # populating SQL table for source bias and reliability 
        source_bias_and_reliability = pd.read_csv("https://raw.githubusercontent.com/pollyannafx/datascience-sandbox/refs/heads/main/source-bias-reliability.csv")
        source_bias_and_reliability_df = pd.DataFrame(source_bias_and_reliability)
        con.execute(f"INSERT INTO SOURCE_AND_RELIABILITY_TEST_3 SELECT * FROM source_bias_and_reliability_df")
        logger.info("populated SQL table for source bias and reliability.") 
        
        ############## articles we will be fetching from APIs ############
        source_names_and_ids = []
        news_articles = []
        headline_sentiments = []
    
        # defining our sntiment analysis tool 
        analyzer = SentimentIntensityAnalyzer()
    
        # connecting to master newsAPI 
        response1 = requests.get("https://newsapi.org/v2/sources?language=en&country=us&apiKey=9f2cea00198d4c24955ae9d517cf77fe")
        logger.info("connected to master newsAPI.") 

        # retrieving data from newsAPI 
        open_source_page1 = response1.json()
        logger.info("retrieved info from master newsAPI.") 

        # retrieving individual pieces of identificatory information 
        sources_more = open_source_page1.get("sources", "") 
        for source in sources_more:
            source_id = source.get("id", "") 
            source_name = source.get("name", "")
            source_url = source.get("url", "")
              
            # appending to dictionary 
            source_names_and_ids.append({
                "source_id": source_id, 
                "source_name": source_name,
                "source_url": source_url
            })

        # populating SQL table for news source identificatory information 
        source_names_and_ids_df = pd.DataFrame(source_names_and_ids)
        con.execute(f"INSERT INTO SOURCE_NAME_ID_TEST_3 SELECT * FROM source_names_and_ids_df")
        logger.info("populated SQL table for news sources' identificatory details.") 
    
                                   
        # initialising link for per-source API  
        for source in news_source_names: 
            base_url = f"https://newsapi.org/v2/everything?sources={source}&language=en&apiKey=9f2cea00198d4c24955ae9d517cf77fe"
    
            query_params_1 = {
                "sources": source,
                "sortBy": "top",
                "apiKey": "9f2cea00198d4c24955ae9d517cf77fe"
            } 
        
          ### news_articles
            # connecting to per-source API 
            response2 = requests.get(url = base_url, params = query_params_1)
            logger.info(f"connected to {source} newsAPI.") 
            
            # retrieving info from per-source API 
            open_source_page2 = response2.json()
            logger.info(f"retrieved info from {source} newsAPI.") 

            # fetching all articles for a specific source
            articles_list = open_source_page2.get("articles","")
            # retrieving information from each 
            for article in articles_list:
                source =  article.get("source", "")
                source_id = source.get("id", "")
                source_name = source.get("name", "")
                article_title = article.get("title", "")
                article_pubdate = article.get("publishedAt", "")
                article_url = article.get("url", "") 
                
                # appending information from the articles to a dictionary
                news_articles.append({
                    "source_id": source_id,
                    "source_name": source_name,
                    "article_title": article_title,
                    "article_pubdate": article_pubdate, 
                    "article_url": article_url
                })

                # performing sentiment analysis on the articles' headlines 
                title_sentiment = analyzer.polarity_scores(article_title)["compound"]
                # taking the absolute value 
                title_sentiment = abs(title_sentiment)
                logger.info(f"conducted sentiment analysis on article titles from {source}.") 

                # appending to dictionary 
                headline_sentiments.append({
                    "source_id": source_id,
                    "article_title": article_title,
                    "title_sentiment": title_sentiment
                    })

            # creating dataframes for both article details and for sentiments of headlines 
            headline_sentiments_df = pd.DataFrame(headline_sentiments)  
            news_articles_df = pd.DataFrame(news_articles)

            # populating SQL table for news article details 
            con.execute(f"INSERT INTO NEWS_ARTICLES_TEST_3 SELECT * FROM news_articles_df")
            logger.info(f"populated SQL table for news articles with articles from {source}.") 

            # populating SQL tables for headline sentiments
            con.execute(f"INSERT INTO HEADLINE_SENTIMENTS_TEST_3 SELECT * FROM headline_sentiments_df")
            logger.info(f"populated SQL table for headline sentiments with headline sentiments from {source}.") 
        
        # creating dictionary of dataframes. i used these when conducting EDA 
        tables_dict = {"news_articles_df":news_articles_df, "source_names_and_ids_df":source_names_and_ids_df,
                        "source_bias_and_reliability_df":source_bias_and_reliability_df, "headline_sentiments_df":headline_sentiments_df}
        return tables_dict


    # error handling 
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

# so it works 
if __name__ == '__main__':
    load_relevant_data()