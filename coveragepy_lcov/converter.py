import logging
from typing import Union

import coverage
from coverage.files import FnmatchMatcher, prep_patterns
from coverage.misc import CoverageException, NoSource, NotPython

log = logging.getLogger("coveragepy_lcov.converter")


class Converter:
    def __init__(
        self,
        relative_path: bool,
        config_file: Union[str, bool],
        data_file_path: str,
    ):
        self.relative_path = relative_path

        self.cov_obj = coverage.coverage(
            data_file=data_file_path, config_file=config_file
        )
        self.cov_obj.load()
        self.cov_obj.get_data()

    def get_lcov(self) -> str:
        """Get LCOV output

        This is shamelessly adapted from https://github.com/nedbat/coveragepy/blob/master/coverage/report.py

        """
        output = ""

        file_reporters = self.cov_obj._get_file_reporters(None)
        config = self.cov_obj.config

        if config.report_include:
            matcher = FnmatchMatcher(
                prep_patterns(config.report_include), "report_include"
            )
            file_reporters = [fr for fr in file_reporters if matcher.match(fr.filename)]

        if config.report_omit:
            matcher = FnmatchMatcher(prep_patterns(config.report_omit), "report_omit")
            file_reporters = [
                fr for fr in file_reporters if not matcher.match(fr.filename)
            ]

        if not file_reporters:
            raise CoverageException("No data to report.")

        for fr in sorted(file_reporters):
            try:
                analysis = self.cov_obj._analyze(fr)
                token_lines = analysis.file_reporter.source_token_lines()
                if self.relative_path:
                    filename = fr.relative_filename()
                else:
                    filename = fr.filename
                output += "TN:\n"
                output += f"SF:{filename}\n"

                lines_hit = 0
                for i, _ in enumerate(token_lines, 1):
                    hits = get_hits(i, analysis)
                    if hits is not None:
                        if hits > 0:
                            lines_hit += 1
                        output += f"DA:{i},{hits}\n"

                output += f"LF:{len(analysis.statements)}\n"
                output += f"LH:{lines_hit}\n"
                output += "end_of_record\n"

            except NoSource:
                if not config.ignore_errors:
                    raise

            except NotPython:
                if fr.should_be_python():
                    if config.ignore_errors:
                        msg = "Couldn't parse Python file '{}'".format(fr.filename)
                        self.cov_obj._warn(msg, slug="couldnt-parse")

                    else:
                        raise

        return output

    def print_lcov(self) -> None:
        """Print LCOV output

        Print out the LCOV output

        """
        lcov_str = self.get_lcov()
        print(lcov_str)

    def create_lcov(self, output_file_path) -> None:
        lcov_str = self.get_lcov()

        with open(output_file_path, "w") as output_file:
            output_file.write(lcov_str)


def get_hits(line_num, analysis):
    if line_num in analysis.missing:
        return 0

    if line_num not in analysis.statements:
        return None

    return 1
