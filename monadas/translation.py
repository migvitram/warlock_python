import os
import yaml

def _(group: str, textToTranslate: str, language: str='ua') -> str:

    storagePath = os.path.abspath('./lang/'+language+'/'+group+'.yml')
    if os.path.exists(storagePath) and os.path.isfile(storagePath):

        with open(storagePath, 'r') as file:
            yamlData = yaml.safe_load(file)

            if textToTranslate in yamlData.keys():
                return str(yamlData[textToTranslate]).strip()
        return textToTranslate
    else:
        return textToTranslate

