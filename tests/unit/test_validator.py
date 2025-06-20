import pytest

from contextlib import nullcontext as does_not_raise
from typing import Any, Optional, List
from pathlib import Path

from src.common.validator import CliArgsValidator


class TestCliArgsValidator:
    @pytest.mark.parametrize(
        "filepath, expected_result, expectation",
        [
            ("tests/testdata.csv", "tests/testdata.csv", does_not_raise()),
            ("testdata.csv", None, pytest.raises(FileExistsError)),
            ("tests/testdata", None, pytest.raises(Exception)),
        ]
    )
    def test_filepath_validator(
            self,
            filepath: Any,
            expected_result: Optional[Path],
            expectation
    ) -> None:
        with expectation:
            if expected_result is None:
                assert CliArgsValidator.filepath(filepath=filepath) == expected_result
            else:
                assert CliArgsValidator.filepath(filepath=filepath) == Path(expected_result)

    @pytest.mark.parametrize(
        "filters, expected_result, expectation",
        [
            ("price>200", ["price", ">", "200"], does_not_raise()),
            ("price>apple", None, pytest.raises(Exception)),
            ("brand!=apple", None, pytest.raises(Exception)),
        ]
    )
    def test_filters_validator(
            self,
            filters: str,
            expected_result: Optional[List[str]],
            expectation
    ) -> None:
        with expectation:
            assert CliArgsValidator.filter(choice=filters) == expected_result

    @pytest.mark.parametrize(
        "aggregation_choice, expected_result, expectation",
        [
            ("price>brand", None, pytest.raises(Exception)),
            ("id=avg", ["id", "avg"], does_not_raise()),
            ("price=avg", ["price", "avg"], does_not_raise()),
        ]
    )
    def test_aggregation_validator(
            self,
            aggregation_choice: str,
            expected_result: Optional[List[str]],
            expectation
    ):
        with expectation:
            assert CliArgsValidator.aggregation(choice=aggregation_choice) == expected_result
