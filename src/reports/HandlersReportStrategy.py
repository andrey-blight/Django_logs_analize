import re

from reports import ReportStrategy


class HandlersReportStrategy(ReportStrategy):
    # regex that find pattern LOG_LEVEL django.requests: ... URL ...
    HANDLER_REGEX = r"(?P<level>INFO|DEBUG|WARNING|ERROR|CRITICAL) django.request: .*? (?P<url>/[^\s]+)"
    # regex to find log level in lines where we don't have handler
    NOT_HANDLER_REGEX = r"(?P<level>INFO|DEBUG|WARNING|ERROR|CRITICAL)"
    # count chars in one column
    COLUMN_WIDTH = 20

    def generate_report(self, logs: list[str]) -> str:
        answer = dict()
        for file in logs:
            data = self._parse_file(file)
            self._merge(answer, data)
        return self._stringify(answer)

    def _parse_file(self, file: str) -> dict[str, dict[str, int]]:
        """Parse log file
        :return dict like {URL: {INFO: 1, DEBUG: 1,...}, ...}"""
        data = dict()
        handler_now = None
        with open(file, 'r') as f:
            for line in f.readlines():
                # get log level and handler if this line contains django.requests:
                request_data = re.findall(self.HANDLER_REGEX, line)
                if request_data:
                    for match in request_data:
                        log_level, request_url = match
                        if request_url not in data:
                            data[request_url] = {"INFO": 0, "WARNING": 0, "ERROR": 0, "DEBUG": 0,
                                                 "CRITICAL": 0}
                        data[request_url][log_level] += 1
                        handler_now = request_url
                else:
                    # this line doesn't have handler so we need add log level to last seen handler

                    # if we haven't seen any request we don't understand what about it so just continue
                    if handler_now is None:
                        continue
                    try:
                        log_level = re.findall(self.NOT_HANDLER_REGEX, line)[0]
                    except IndexError:
                        continue
                    data[handler_now][log_level] += 1
        return data

    @staticmethod
    def _merge(answer: dict[str, dict[str, int]], data: dict[str, dict[str, int]]) -> None:
        """Merge total count and count in file"""
        for handler in data:
            if handler not in answer:
                answer[handler] = {"INFO": 0, "WARNING": 0, "ERROR": 0, "DEBUG": 0, "CRITICAL": 0}

            for level, count in data[handler].items():
                answer[handler][level] += count

    def _stringify(self, data: dict[str, dict[str, int]]) -> str:
        """Sorting and stringify dict data"""
        all_handlers_data: list[tuple[str, str]] = []
        total_count = 0
        for handler in data:
            # get list like [(INFO, 1), (DEBUG, 2), ...]
            handler_data: list[tuple[str, int]] = []
            for level, count in data[handler].items():
                total_count += count
                handler_data.append((level, count))
            # sort by log level and create line with numbers
            handler_data.sort(key=lambda x: x[0])
            handler_line = '\t'.join(
                f"{count:<{self.COLUMN_WIDTH}}" for level, count in handler_data)
            all_handlers_data.append((handler, handler_line))

        all_handlers_data.sort(key=lambda x: x[0])
        all_handlers_line = '\n'.join(
            f"{handler:<{self.COLUMN_WIDTH}}\t{line}" for handler, line in all_handlers_data)

        header = ['HANDLERS', "CRITICAL", "DEBUG", "ERROR", "INFO", "WARNING"]
        header_line = '\t'.join(f"{column:<{self.COLUMN_WIDTH}}" for column in header)
        result = [
            "HANDLERS REPORT",
            f"TOTAL: {total_count}",
            header_line,
            all_handlers_line
        ]
        return '\n'.join(result)
