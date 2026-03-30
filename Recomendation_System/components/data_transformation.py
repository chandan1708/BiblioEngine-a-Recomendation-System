import os
import sys
import pickle
import pandas as pd 
from Recomendation_System.logger.log import logging
from Recomendation_System.exception.exception_handler import AppException
from Recomendation_System.config.configuration import AppConfiguration

class DataTransformation:
    def __init__(self,app_config=AppConfiguration()):
        try:
            logging.info(f"{'='*20}Data Transformation log started.{'='*20} ")
            self.data_transformation_config = app_config.get_data_transformation_config()
            self.data_validation_config = app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def get_data_transformer(self):
        try:
            df=pd.read_csv(self.data_transformation_config.clean_data_file_path)

            #lets create a pivot table
            book_pivot=df.pivot_table(columns='user_id',index='title',values='rating')
            logging.info(f"shape of book pivot table {book_pivot.shape}")
            book_pivot.fillna(0,inplace=True)

            #saving pivot table data 
            os.makedirs(self.data_transformation_config.transformed_data_dir,exist_ok=True)

            pickle.dump(book_pivot,open(os.path.join(self.data_transformation_config.transformed_data_dir,'transformed_data.pkl'),'wb'))
            logging.info(f"Transformed data saved to {self.data_transformation_config.transformed_data_dir}")
            logging.info(f"{'='*20}Data Transformation log ended.{'='*20} ")

            #keeping books name
            books_name=book_pivot.index

            #saving book_name for web app
            os.makedirs(self.data_validation_config.serialized_objects_dir,exist_ok=True)
            pickle.dump(books_name,open(os.path.join(self.data_validation_config.serialized_objects_dir,'books_name.pkl'),'wb'))
            logging.info(f"Books name saved to {self.data_validation_config.serialized_objects_dir}")
            logging.info(f"{'='*20}Data Transformation log ended.{'='*20} ")

            #saving book_pivot objects for web app

            os.makedirs(self.data_validation_config.serialized_objects_dir,exist_ok=True)
            pickle.dump(book_pivot,open(os.path.join(self.data_validation_config.serialized_objects_dir,'book_pivot.pkl'),'wb'))
            logging.info(f"Book pivot saved to {self.data_validation_config.serialized_objects_dir}")
            logging.info(f"{'='*20}Data Transformation log ended.{'='*20} ")

        except Exception as e:
            raise AppException(e, sys) from e

    
    def initiate_data_transformation(self):
        try:
            logging.info(f"{'='*20}Data Transformation log started.{'='*20} ")
            self.get_data_transformer()
            logging.info(f"{'='*20}Data Transformation log ended.{'='*20} ")
        except Exception as e:
            raise AppException(e, sys) from e