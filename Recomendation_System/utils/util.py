import yaml
import sys 
from Recomendation_System.exception.exception_handler import AppException

def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    """
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise AppException(e,sys) from e

