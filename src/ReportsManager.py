from ReportFactory import ReportFactory


class ReportsManager:
    def __init__(self, report_name: str, files: list[str]):
        try:
            # trying to get report class using report factory
            self.report_strategy = ReportFactory.get_report(report_name)
        except ValueError:
            print("Invalid report name")
            exit(1)
        self.files = files

    def get_report(self) -> None:
        print(self.report_strategy.generate_report(self.files))
