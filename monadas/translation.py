import os
import yaml
from models.AppContext import AppContext

def _(group: str, textToTranslate: str, params: dict|None = None, language: str|None = None) -> str:

    lang = language if language is not None else (str(AppContext.get('lang')) if AppContext.get('lang') else 'en')
    params = params or {}

    projectRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    storagePath = os.path.join(projectRoot, 'lang', lang, f'{group}.yml')
    if os.path.exists(storagePath) and os.path.isfile(storagePath):

        resultString = textToTranslate

        with open(storagePath, 'r') as file:
            yamlData = yaml.safe_load(file)

            if textToTranslate in yamlData.keys():
                resultString = str(yamlData[textToTranslate]).strip()
        
        for paramName, param in params.items():
            resultString = resultString.replace(r'{'+paramName+r'}', str(param).strip())
        
        return resultString
    else:
        return textToTranslate
