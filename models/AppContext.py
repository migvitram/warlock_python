from typing import Any

class AppContext:

    contextParams: dict = {}

    @staticmethod
    def has(paramName: str) -> bool:
        return paramName in AppContext.contextParams

    @staticmethod
    def get(paramName: str) -> object:
        if AppContext.has(paramName):
            return AppContext.contextParams[paramName]
        return False
    
    @staticmethod
    def set(paramName: str, value: object) -> bool:
        AppContext.contextParams[paramName] = value
        return True