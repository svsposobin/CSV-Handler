from typing import List

from src.cli import read_args
from src.common.dto import FileHandlerDTO, CliArgsDTO
from src.processor import CSVFileHandler


def run(sys_args: List[str]) -> FileHandlerDTO:
    result: FileHandlerDTO = FileHandlerDTO()

    try:
        cli_args: CliArgsDTO = read_args(sys_args)

        if cli_args.error:
            raise Exception(cli_args.error)

        assert cli_args.args is not None

        handler: CSVFileHandler = CSVFileHandler(
            filepath=cli_args.args.file,
            filters=cli_args.args.where,
            aggregation=cli_args.args.aggregate,
        )

        data: FileHandlerDTO = handler.get_with_formatter()

        if data.error:
            raise Exception(data.error)

        result.result = data.result

    except Exception as error:
        result.error = str(error)

    return result
