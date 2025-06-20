import pytest

from collections.abc import Generator
from typing import List, Any, Optional

from src.common.dto import FileHandlerDTO
from src.processor import CSVFileHandler


class TestCSVFileHandler:
    """Данные тесты принимают только валидные параметры, прошедшие валидацию"""

    @pytest.mark.parametrize(
        "filepath, filters, aggregation",
        [
            ("tests/testdata.csv", None, None),
            ("tests/testdata.csv", None, ["price", "avg"]),
            ("tests/testdata.csv", ["price", ">", "200"], ["price", "min"]),
            ("tests/testdata.csv", ["price", "<", "200"], ["price", "max"]),
        ]
    )
    def test_get_method_with_result(
            self,
            filepath: Any,
            filters: Optional[List[str]],
            aggregation: Optional[List[str]]
    ) -> None:
        handler: CSVFileHandler = CSVFileHandler(
            filepath=filepath,
            filters=filters,
            aggregation=aggregation
        )

        result: FileHandlerDTO = handler.get_with_formatter()

        assert result.result is not None
        assert result.error is None

    @pytest.mark.parametrize(
        "filepath, filters, aggregation",
        [
            ("tests/testdata.csv", ["price", ">", "1000000"], None),
            ("tests/testdata.csv", ["price", "<", "-1000000"], None),
            ("tests/testdata.csv", ["price", ">", "5"], ["unsup_column", "avg"]),
        ]
    )
    def test_get_method_with_empty_result(
            self,
            filepath: Any,
            filters: Optional[List[str]],
            aggregation: Optional[List[str]]
    ):
        handler: CSVFileHandler = CSVFileHandler(
            filepath=filepath,
            filters=filters,
            aggregation=aggregation
        )

        result: FileHandlerDTO = handler.get_with_formatter()

        assert result.result is None
        assert result.error is not None

    @pytest.mark.parametrize(
        "filepath, filters, expected_result",
        [
            ("tests/testdata.csv", None, Generator),
            ("tests/testdata.csv", ["price", ">", "1000000"], Generator),
            ("tests/testdata.csv", ["price", ">", "5"], Generator),
        ]
    )
    def test_load_data(
            self,
            filepath: Any,
            filters: Optional[List[str]],
            expected_result: Optional[Generator]
    ) -> None:
        handler: CSVFileHandler = CSVFileHandler(
            filepath=filepath,
            filters=filters,
            aggregation=None
        )

        result = handler._load_data()

        assert isinstance(result, Generator)
