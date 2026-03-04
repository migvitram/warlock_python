import os
import json

class Settings:

    storageFile = 'storage/personal_settings.json'

    def __init__(self) -> None:
        pass

    # method to make some settings about visits (e.g. stop to show the intro)
    @staticmethod
    def revisit() -> bool:
        Settings.checkSettingStorage()
        settings = Settings.readSettings()
        settings['visits'] += 1
        return Settings.writeSettings(settings)

    @staticmethod
    def updateParam(paramName: str, value: str|int) -> bool:
        Settings.checkSettingStorage()
        settings = Settings.readSettings()
        settings[paramName] = value
        return Settings.writeSettings(settings)

    @staticmethod
    def getParam(paramName: str) -> str|int|dict|list|tuple|bool:
        Settings.checkSettingStorage()
        settings = Settings.readSettings()
        return settings[paramName] if paramName in settings else False

    @staticmethod
    def getAsInt(paramName: str) -> int:
        Settings.checkSettingStorage()
        settings = Settings.readSettings()
        if paramName in settings.keys():
            paramToConvert = settings[paramName]
            
            if isinstance(paramToConvert, (str, dict, list, tuple)):
                return 1 if len(paramToConvert) > 0 else 0

            return int(settings[paramName])
        else:
            return 0

    @staticmethod
    def checkSettingStorage():
        if not os.path.exists(Settings.storageFile):
            with open(Settings.storageFile, 'w+') as storageFile:
                return storageFile.write(json.dumps(Settings.settingsStructure())) > 0
        return True

    @staticmethod
    def settingsStructure() -> dict:
        return {
            'visits': 0,
            'language': 'en'
        }
    
    @staticmethod
    def readSettings() -> dict:
        Settings.checkSettingStorage()
        with open(Settings.storageFile, 'r') as storageFile:
            return json.load(storageFile)

    @staticmethod
    def writeSettings(dataToWrite: dict) -> bool:
        Settings.checkSettingStorage()
        with open(Settings.storageFile, 'w+') as storageFile:
            content = storageFile.write(json.dumps(dataToWrite))
            return content > 0