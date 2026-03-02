import os
from datetime import datetime
import zoneinfo
from dotenv import load_dotenv

class Logger:

    singletoneInstance = None
    timezone: str = 'UTC'
    loggerStoragePath = 'storage/app.log'
    loggerStorageInst = False

    def __init__(self, timezone: str|None=None) -> None:
        load_dotenv()
        timezone = timezone if timezone is not None else os.getenv("APP_TIMEZONE")

        if timezone is not None:
            allTimezones = zoneinfo.available_timezones()
            for tz in sorted(list(allTimezones)):
                if timezone == tz:
                    Logger.timezone = timezone
                    break
            pass

        Logger.checkLogFileExists()

    @staticmethod
    def checkLogFileExists():
        if not os.path.exists(Logger.loggerStoragePath):
            message = Logger.getTime() + 'Loger initiate'
            with open(Logger.loggerStoragePath, 'w+') as storageFile:
                storageFile.write(message)
        else:
            pass

    @staticmethod
    def getInstance(timezone: str|None=None):
        if Logger.singletoneInstance is None:
            Logger.singletoneInstance = Logger(timezone)
        return Logger.singletoneInstance

    @staticmethod
    def log(message: str):
        logger = Logger.getInstance()
        Logger.checkLogFileExists()

        with open(logger.loggerStoragePath, 'r') as storageFile:
            content = storageFile.read()

        with open(logger.loggerStoragePath, 'w') as storageFile:
            storageFile.write(Logger.getTime() + message + "\n" + content)
        return
    
    @staticmethod
    def clean():
        logger = Logger.getInstance()
        if os.path.exists(logger.loggerStoragePath):
            os.remove(logger.loggerStoragePath)
            return os.path.exists(logger.loggerStoragePath) == False
        return False

    @staticmethod
    def getTime() -> str:
        timezone = Logger.timezone
        return "[" + datetime.now(zoneinfo.ZoneInfo(timezone)).strftime("%d/%m/%Y, %H:%M:%S") + "] : "