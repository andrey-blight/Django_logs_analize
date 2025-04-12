import os
import sys
from ReportsManager import ReportsManager


def _check_file_exists(file_path: str) -> None:
    if not os.path.isfile(file_path):
        raise ValueError(f"File '{file_path}' does not exist.")


def parse_args(argv: list[str]) -> tuple[list[str], str]:
    """This function parses the arguments passed to the script.
    Firstly, it adds all logs file inside files list and checks if each file exists.
    Secondly, it searches for --report param and check valid argv.
    """
    report = None
    files = []
    i = 1
    while i < len(argv):
        # find --report, check that next argument exist and write report name.
        if argv[i] == '--report':
            if i + 1 < len(argv):
                report = argv[i + 1]
                i += 1
            else:
                raise ValueError("No report name")
        else:
            _check_file_exists(argv[i])
            files.append(argv[i])
        i += 1
    if report is None:
        raise ValueError("No report name")
    if not files:
        raise ValueError("No log files")
    return files, report


if __name__ == '__main__':
    try:
        log_files, report_name = parse_args(sys.argv)
    except ValueError as ex:
        print("Incorrect arguments")
        print(ex.args[0])
        print("Usage: python3 main.py filename1 filename2 ... --report <report name>")
        exit(1)
    ReportsManager(report_name, log_files).get_report()
