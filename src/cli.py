from argparse import ArgumentParser
from typing import List

from src.common.constants import ALLOW_AGGREGATE_METHODS, ALLOW_FILTER_OPERATORS
from src.common.validator import CliArgsValidator
from src.common.dto import CliArgsDTO
from src.common.constants import ERRORS_MAPPING


def read_args(args: List[str]) -> CliArgsDTO:
    result: CliArgsDTO = CliArgsDTO()

    try:
        cli_args: ArgumentParser = ArgumentParser(
            prog="CSV - Handler ",
            description="Скрипт по обработки .csv файлов, не поддерживает другие расширения",
            exit_on_error=False,
        )

        cli_args.add_argument(
            "--file", "-f",
            type=CliArgsValidator.filepath,
            required=True,
            help="В данный флаг нужно передать файл или путь к файлу (Вместе с расширением .csv)",
            metavar="FILE/FILE_PATH",
        )

        cli_args.add_argument(
            "--where", "-w",
            type=CliArgsValidator.filter,
            help=f"Фильтрация по: <колонка><один_оператор><условие>\nДоступные условия: {ALLOW_FILTER_OPERATORS}",
            metavar="COLUMN=CONDITION",
        )

        cli_args.add_argument(
            "--aggregate", "-a",
            type=CliArgsValidator.aggregation,
            help=f"Агрегация по: <колонка>=<метод>.\nДоступные методы: {ALLOW_AGGREGATE_METHODS}",
            metavar="COLUMN=OPERATION",
        )

        result.args = cli_args.parse_args(args)

    except Exception as error:
        result.error = ERRORS_MAPPING.get(str(error), error)  # type: ignore

    return result
