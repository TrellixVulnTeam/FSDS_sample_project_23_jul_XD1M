import os, sys
from re import L
from housing.config.configuration import Configuration
from housing.logger import logging
from housing.exception import HousingException

from housing.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from housing.entity.config_entity import DataIngestionConfig
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import DataValidation
from housing.component.data_transformation import DataTransformation
from housing.component.model_trainer import ModelTrainer
from housing.entity.artifact_entity import DataValidationArtifact, ModelTrainerArtifact
class Pipeline():

    def __init__(self, config:Configuration= Configuration())-> None:
        try:
            self.config= config
        except Exception as e:
            raise HousingException(e, sys) from e
    
    def start_data_ingestion(self)-> DataIngestionArtifact:
        try:
            data_ingestion= DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config() )

            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise HousingException(e, sys) from e

    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation= DataValidation(data_validation_config= self.config.get_data_validation_config(),
                                             data_ingestion_artifact= data_ingestion_artifact)

            #logging.info("Data Validation is done!")
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise HousingException(e, sys) from e

    def start_data_transformation(self, data_ingestion_artifact:DataIngestionArtifact,
                                         data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:

            data_transformation= DataTransformation(data_transformation_config=self.config.get_data_transformation_config(),
                                                    data_ingestion_artifact=data_ingestion_artifact,
                                                    data_validation_artifact=data_validation_artifact)
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise HousingException(e, sys) from e

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact,
                            )->ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(model_trainer_config=self.config.get_model_trainer_config(),
                                         data_transformation_artifact=data_transformation_artifact
                                         )
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise HousingException(e, sys) from e

    def start_model_evaluation(self):
        pass

    def start_model_pusher(self):
        pass

    def run_pipeline(self):
        try:
            ## Data ingestion
            data_ingestion_artifact= self.start_data_ingestion()
            
            logging.info(f"Data ingestion pipeline executed successfully")
            ##Data Validation pipeline
            data_validation_artifact= self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            logging.info(f"Data Validation pipeline executed successfully")

            ##Data Tatansformation pipeline
            data_transformation_artifact= self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                            data_validation_artifact=data_validation_artifact)
            logging.info(f"Data transformation is done artifact:{data_transformation_artifact}")
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            logging.info(f"Data trainer artifact is completed. artifact:{model_trainer_artifact}")
        except Exception as e:
            raise HousingException(e, sys) from e