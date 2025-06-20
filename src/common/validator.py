from pathlib import Path
from typing import List, Optional, Any
from re import fullmatch, IGNORECASE, Match

from src.common.constants import ALLOW_AGGREGATE_METHODS, ALLOW_FILTER_OPERATORS


class CliArgsValidator:
    @staticmethod
    def filepath(filepath: Any) -> Optional[Path]:
        path: Path = Path(filepath)

        if path.suffix.lower() != ".csv":
            raise Exception("Утилита поддерживает файлы только с расширением .csv")
        if not path.exists():
            raise FileExistsError(f"Файл {path} не найден или невозможно открыть, проверьте название или путь")

        return path

    @staticmethod
    def filter(choice: str) -> Optional[List[str]]:
        """
        :param choice: str -> cli arg, example: 'price>200'
        :return: List[str] -> [column, operator, condition], example: ['price', '>', '200']
        """
        pattern: str = fr'^\s*([a-zA-Z_]\w*)\s*([{ALLOW_FILTER_OPERATORS}])(?![{ALLOW_FILTER_OPERATORS}])\s*(.+?)\s*$'

        match: Optional[Match[str]] = fullmatch(pattern=pattern, string=choice)

        if not match:
            raise Exception(
                f"""
                    Некорректный формат выражения для флага --where '{choice}'.
                    Ожидается: <колонка><один_оператор><условие>
                    Доступные условия: {ALLOW_FILTER_OPERATORS}
                """
            )

        column, operator, condition = match.groups()

        is_num: bool = condition.lstrip('-').replace(".", "", 1).isdigit()
        if not is_num and operator != "=":
            raise Exception(f"Нельзя применить операторы < и > к фильтрации по строке: {choice}")

        return [column, operator, condition]

    @staticmethod
    def aggregation(choice: str) -> Optional[List[str]]:
        """
        :param choice: str -> cli arg, example: 'price=max'
        :return: List[str] -> [column, operation], example: ['price', 'max']
        """
        pattern: str = fr'^\s*([a-zA-Z_]\w*)\s*=\s*({ALLOW_AGGREGATE_METHODS})\s*$'
        match: Optional[Match[str]] = fullmatch(pattern=pattern, string=choice, flags=IGNORECASE)

        if not match:
            raise Exception(
                f"""
                    Некорректный формат выражения: '{choice}'.
                    Ожидается: <колонка>=<метод>
                    Доступные методы: {ALLOW_AGGREGATE_METHODS}
                """
            )

        func, value = match.groups()
        func = func.lower()

        return [func, value]
