from functools import wraps
from inspect import signature


def strict(func):
    '''Декоратор для проверки соответстивия типов агрументов их аннотациям'''
    sig = signature(func)  # Получение сигнатуры функции
    annotations = func.__annotations__.copy()  # Получение аннотаций функции в виде словаря
    annotations.pop('return', None)  # Удаление аннотаций для return из словаря с аннотациями
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)  # Привязывание параметров к сигнатуре
        for name, value in bound.arguments.items():
            expected_type = annotations.get(name)  # Получение предполагаемого типа из словаяр с аннотациями
            if expected_type is not None and type(value) is not expected_type:  # Проверка совпадения типов
                raise TypeError(f'{name}: expected {expected_type}, got {type(value)} instead')
        return func(*args, **kwargs)  # Вызов целевой функции
    return wrapper
