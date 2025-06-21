from typing import List, Any, Dict, Optional, Generator
from csv import DictReader

from src.common.wrappers import execution_time
from src.common.formatter import formatter
from src.common.dto import FileHandlerDTO


class CSVFileHandler:
    def __init__(
            self,
            filepath: Any,
            filters: Optional[List[str]] = None,
            aggregation: Optional[List[str]] = None,
    ):
        self._filepath: Any = filepath
        self._filters: Optional[List[str]] = filters
        self._aggregation: Optional[List[str]] = aggregation

    def get_full_data(self) -> Generator[Dict[Any, str | Any], None, None]:
        data: Generator[Dict[Any, str | Any], None, None]

        try:
            data = self._load_data()

            if self._aggregation:
                data = self._with_aggregation(data_generator=data)

            # Можно добавить дополнительные обработчики, например --order_by

            return data

        except Exception as error:
            raise Exception(str(error))

    @execution_time
    def get_with_formatter(self) -> FileHandlerDTO:
        result: FileHandlerDTO = FileHandlerDTO()

        try:
            data: Generator[Dict[str, Any], None, None] = self.get_full_data()

            data_formatter: Optional[str] = formatter(data_generator=data)
            if not data_formatter:
                raise Exception("По вашему запросу данных не найдено")

            result.result = data_formatter

        except Exception as error:
            result.error = str(error)

        return result

    def _load_data(self) -> Generator[Dict[Any, str | Any], None, None]:
        """
            :return чтение CSV файла с возможной фильтрацией. Возвращает генератор строк для эффективной работы с
            памятью. Потребление памяти: O(1)
        """
        try:
            with open(file=self._filepath, mode="r", encoding="utf-8", newline="") as csv_file:
                reader: DictReader = DictReader(csv_file)

                if not self._filters:
                    yield from reader
                    return  # Нужен для выхода из функции

                filter_column, filter_operator, filter_value = self._filters

                converted_filter_value: str = filter_value
                try:
                    converted_filter_value: float = float(filter_value)  # type: ignore
                except ValueError:
                    pass

                for row in reader:
                    if filter_column not in row:
                        continue

                    cell_value: str | float = row[filter_column]
                    if isinstance(converted_filter_value, float):
                        try:
                            cell_value: float = float(row[filter_column])  # type: ignore
                        except ValueError:
                            continue

                    match filter_operator:
                        case '=' if cell_value == converted_filter_value:
                            yield row
                        case '>' if cell_value > converted_filter_value:  # type: ignore
                            yield row
                        case '<' if cell_value < converted_filter_value:  # type: ignore
                            yield row
                        # Можно добавить другие операторы

        except Exception as error:
            raise Exception(str(error))

    def _with_aggregation(
            self,
            data_generator: Generator[Dict[str, Any], None, None]
    ) -> Generator[Dict[str, Any], None, None]:
        agg_column, agg_operator = self._aggregation  # type: ignore

        values: List[Any] = []
        total: float = 0
        count: float = 0

        try:
            for row in data_generator:
                if agg_column in row:
                    try:
                        value = float(row[agg_column])
                        values.append(value)
                        total += value
                        count += 1
                    except (ValueError, TypeError):
                        raise Exception("Агрегация поддерживает только числовые значения!")

            if count == 0:
                raise Exception(f"Нет данных для агрегации по колонке {agg_column}")

            result: Optional[float] = None
            match agg_operator:
                case "min":
                    result = min(values)
                case "max":
                    result = max(values)
                case "avg":
                    result = total / count

            yield {
                "function": agg_operator,
                "column": agg_column,
                "result": result
            }

        except Exception as error:
            raise Exception(str(error))
