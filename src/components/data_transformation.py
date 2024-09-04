import sys 
from dataclasses import dataclass
import os 
from sklearn.pipeline import Pipeline





import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.utils import save_object




from src.exception import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    
    def get_data_transformer_object(self):
        '''
        This function is responsible for data tranformation.
        
        '''
        try:
            numerical_columns=['writing score','reading score']
            categorical_columns=[
                'gender',
                'race/ethnicity',
                'parental level of education',
                'test preparation course',
            ]

            num_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())
                
                
                ]
            )    

            cat_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder',OneHotEncoder(handle_unknown='ignore',sparse_output=True)),
                    ('scaler',StandardScaler(with_mean=False)),
                    
                ]

            )    

            logging.info("Categorical columns scaling completed")
            logging.info("numerical columns encoding completed")
            
            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipeline",cat_pipeline,categorical_columns),

                ]


            )
            return preprocessor 
        
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("read train and test data completed ")
            logging.info("Opening preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column="math score"
            numerical_columns=["writing score","reading score"]

            input_feature_train_df=train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df=train_df[target_column]

            input_feature_test_df=test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df=test_df[target_column]

            logging.info("Applying preprocessing object on training dataframe and testing data frame")
            

            input_feature_train_array=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_array=preprocessing_obj.transform(input_feature_test_df)

            train_arr=np.c_[
                input_feature_train_array,np.array(target_feature_train_df)

            ]
            test_arr=np.c_[
                input_feature_test_array,np.array(target_feature_test_df)

            ]

            logging.info("Saved preprocessing object.")

            save_object(
                
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )


        except Exception as e:
            raise CustomException(e,sys)
        