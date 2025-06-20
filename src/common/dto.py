from argparse import Namespace
from dataclasses import dataclass
from typing import Optional


@dataclass
class CliArgsDTO:
    args: Optional[Namespace] = None
    error: Optional[str] = None


@dataclass
class FileHandlerDTO:
    error: Optional[str] = None
    result: Optional[str] = None
