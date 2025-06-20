from typing import Callable, Any
from time import perf_counter


def execution_time(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        start: float = perf_counter()

        result: Any = func(*args, **kwargs)

        end: float = perf_counter()
        print(f"Время исполнения запроса: {round(end - start, 4)}сек")

        return result

    return wrapper
