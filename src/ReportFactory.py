from reports import ReportStrategy, HandlersReportStrategy


class ReportFactory:
    @staticmethod
    def get_report(report_name: str) -> ReportStrategy | None:
        name = report_name.lower()
        if name == "handlers":
            return HandlersReportStrategy()
        else:
            raise ValueError("No such report exist")
