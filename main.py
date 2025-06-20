from sys import argv as sys_argv, exit as sys_exit

from src.logic import main_logic
from src.common.dto import FileHandlerDTO

if __name__ == "__main__":
    result: FileHandlerDTO = main_logic(sys_args=sys_argv[1:])

    if result.error:
        print(result.error)
        sys_exit(1)

    print(result.result)
