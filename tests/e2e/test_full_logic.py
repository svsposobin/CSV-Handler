import pytest

from typing import List

from src.common.dto import FileHandlerDTO
from src.logic import run


class TestFullLogic:
    @pytest.mark.parametrize(
        "cli_args",
        [
            (['-f', 'tests/testdata.csv', '-w', 'brand=apple']),
            (['-f', 'tests/testdata.csv', '-w', 'brand=apple', '-a', 'price=min']),
            (['-f', 'tests/testdata.csv', '-w', 'price>300']),
            (['-f', 'tests/testdata.csv', '-w', 'rating>4.5', '-a', 'price=min'])
        ]
    )
    def test_e2e_success(self, cli_args: List[str]) -> None:
        result: FileHandlerDTO = run(cli_args)

        assert result.error is None
        assert result.result is not None

    @pytest.mark.parametrize(
        "cli_args",
        [
            (['-f', 'tests/testdata.csv', '-w', 'brand>apple']),  # Невалидный оператор фильтрации для строк
            (['-f', 'unvalid/path', '-w', 'price>300']),  # Невалидный путь для файла
            (['-f', 'tests/da.csv', '-w', 'brand=apple']),  # Невозможно найти файл
            (['-f', 'tests/testdata', '-w', 'price>300']),  # Невозможно обработать файл без расширения .csv
            (['-f', 'tests/testdata', '-a', 'price=ggg']),  # Некорректная функция-агрегатор
            (['-f', 'tests/testdata.csv', '-a', 'price>avg']),  # Некорректная агрегация
        ]
    )
    def test_e2e_failure(self, cli_args: List[str]) -> None:
        result: FileHandlerDTO = run(cli_args)

        assert result.error is not None
        assert result.result is None
