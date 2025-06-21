from tabulate import tabulate

from typing import Generator, Dict, Any, List, Optional


def formatter(
        data_generator: Generator[Dict[str, Any], None, None],
        table_format: str = 'grid'
) -> Optional[str]:
    """
        Данный форматтер не рекомендуется использовать для обработки огромных файлов, так как он загружает
        все данные в память!
    """
    data: List[Any] = []
    headers: Optional[Any] = None

    for index, row in enumerate(data_generator):
        if index == 0:
            headers = row.keys()

        data.append(row.values())

    if not headers:
        return None

    return tabulate(data, headers=headers, tablefmt=table_format)
