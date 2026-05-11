import os
import yaml
from models.AppContext import AppContext

def _(group: str, textToTranslate: str, params: dict={}, language: str|None = None) -> str:

    lang = language if language is not None else str(AppContext.get('lang'))

    storagePath = os.path.abspath('./lang/'+lang+'/'+group+'.yml')
    if os.path.exists(storagePath) and os.path.isfile(storagePath):

        with open(storagePath, 'r') as file:
            yamlData = yaml.safe_load(file)

            if textToTranslate in yamlData.keys():
                resultString = str(yamlData[textToTranslate]).strip()
                for paramName, param in params.items():
                    resultString = resultString.replace(r'{'+paramName+r'}', param)
                return resultString
        return textToTranslate
    else:
        return textToTranslate

