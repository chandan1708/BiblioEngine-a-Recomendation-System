import os
import sys
import ast 
import pandas as pd
import pickle
from Recomendation_System.logger.log import logging
from Recomendation_System.exception.exception_handler import AppException
from Recomendation_System.config.configuration import AppConfiguration


class DataValidation:
    def __init__(self,app_config=AppConfiguration()):
        try:
            logging.info(f"{'='*20}Data Validation log started.{'='*20} ")
            self.data_validation_config = app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e
    
    def preprocess_data(self):
        try:
            books = pd.read_csv(
                self.data_validation_config.books_csv_file,
                sep=";",
                encoding="latin1",
                on_bad_lines="skip",
                low_memory=False,
            )
            ratings = pd.read_csv(
                self.data_validation_config.ratings_csv_file,
                sep=";",
                encoding="latin1",
                on_bad_lines="skip",
            )
            logging.info(f"Shape of ratings data file:{ratings.shape}")
            logging.info(f"Shape of books data file:{books.shape}")
            books=books[['ISBN','Book-Title','Book-Author','Year-Of-Publication','Publisher','Image-URL-L']]
            books.rename(columns={"Book-Title":"title","Book-Author":"author","Year-Of-Publication":"year","Publisher":"publisher","Image-URL-L":"image_url"}, inplace=True)
            ratings.rename(columns={"User-ID":"user_id","Book-Rating":"rating"}, inplace=True)
            

            #eliminating outliers by storing users who had at least reated more than 200 books
            x=ratings['user_id'].value_counts() > 200
            y=x[x].index
            ratings=ratings[ratings['user_id'].isin(y)]
            
            #join ratings with books
            ratings_with_books=ratings.merge(books,on='ISBN')

            #creating a dataframe with number of ratings for each book
            number_rating=ratings_with_books.groupby('title')['rating'].count().reset_index()
            number_rating.rename(columns={'rating':'num_rating'},inplace=True)
            
            #merging the number of ratings with the ratings dataframe
            final_rating=ratings_with_books.merge(number_rating,on='title')

            #take those books which have more than 50 ratings by user
            final_rating=final_rating[final_rating['num_rating']>=50]
            
            #drop duplicate values
            final_rating.drop_duplicates(['user_id','title'],inplace=True)
            logging.info(f"Shape of final rating data file:{final_rating.shape}")
            
            #saving cleaned data for transformation
            os.makedirs(self.data_validation_config.clean_data_dir,exist_ok=True)
            final_rating.to_csv(os.path.join(self.data_validation_config.clean_data_dir,'clean_data.csv'),index=False)
            logging.info(f"Cleaned data saved to {self.data_validation_config.clean_data_dir}")
            

            #saving final_rating objects for web app
            os.makedirs(self.data_validation_config.serialized_objects_dir,exist_ok=True)
            pickle.dump(final_rating,open(os.path.join(self.data_validation_config.serialized_objects_dir,'final_rating.pkl'),'wb'))
            logging.info(f"Final rating objects saved to {self.data_validation_config.serialized_objects_dir}")

        except Exception as e:
            logging.info(f"Error in data validation: {e}")
            raise AppException(e, sys) from e
    
    def initiate_data_validation(self):
        try:
            logging.info(f"{'='*20}Data Validation log started.{'='*20} ")
            self.preprocess_data()
            logging.info(f"Data validation completed successfully")
        except Exception as e:
            raise AppException(e, sys) from e 