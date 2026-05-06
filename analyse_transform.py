import logging
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV
import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import train_test_split

# configuring the logging mechanism
logging.basicConfig(
    filename='analysis.log',
    filemode="a",
    style="{", 
    datefmt="%Y-%m-%d-%H:%M:%x", 
    level="INFO"
)
logger = logging.getLogger(__name__)

def analyse_relevant_data(): 
    # connecting to duckdb instance 
    con = duckdb.connect(db_path)
    try:
        # joining tables for analysis 
        df = con.execute(f"""SELECT 
        s.source_id,
        h.title_sentiment,
        s.source_reliability
        FROM HEADLINE_SENTIMENTS_TEST_3 h 
        JOIN SOURCE_AND_RELIABILITY_TEST_3 s
        ON h.source_id = s.source_id
        ;""").df()
        logger.info("joined tables for analysis") 
        
        # feature and target matrices 
        X = df.iloc[:,1:2]
        y = df.iloc[:,-1:]
        logger.info("created feature and target matrices") 

        # Create training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)
        logger.info("created training and test sets") 
 
        # designing pipeline 
        final_pipeline = Pipeline([
            ('poly', PolynomialFeatures(degree=9, include_bias=False)),
            ('scaler', StandardScaler()),
            ('lasso', Lasso(alpha=0.016681))
        ])
        logger.info("designed pipeline") 

        # finally fitting polynomial reg pipeline 
        final_pipeline.fit(X_train, y_train)
        y_pred = final_pipeline.predict(X_test)
        logger.info("fit the polynomial reg pipeline") 
        logger.info("output predictions") 

        # creating scatterplot 
        plt.scatter(x=X_test, y=y_pred)
        plt.scatter(x=X_test, y=y_test) 
        plt.xlabel("VADER sentiment score absolute value") 
        plt.ylabel("AdFontes Media reliability score") 
        plt.suptitle("Getting a feel for the news", y=0.999, fontsize=16)
        plt.title("Gauging whether sentiment strength can predict\nnews source reliability", fontsize=9)
        plt.legend(labels=["y_pred","y_test"], loc="lower right")
        logger.info("created graph") 
        
        # making a png image of our graph. 
        output_path = "reliability_sentiment.png"
        plt.savefig(output_path, format="png")
        print(f"Saved plot to {output_path}")
        logger.info("saved graph") 

        # 'showing' graph 
        plt.show()

        # output path to our graph (it's a png image now) 
        return output_path
        
    # error handling
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

# so it will actually work 
if __name__ == '__main__':
    analyse_relevant_data()
