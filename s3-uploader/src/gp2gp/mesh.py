from dataclasses import dataclass
from pathlib import Path
from defusedxml.ElementTree import parse
from datetime import datetime


class MeshInboxScanner:
    def scan(self, directory):
        directory_path = Path(directory)

        file_paths = directory_path.glob("*.dat")

        for file_path in file_paths:
            date = self._get_date(file_path)
            yield MeshFile(path=str(file_path), date_delivered=date)

    def _get_date(self, dat_path):
        ctrl_path = self._find_ctrl_from_dat(dat_path)
        date_string = self._parse_value_from_xml(ctrl_path)
        parsed_date = self._parse_date_from_string(date_string)
        return parsed_date

    def _find_ctrl_from_dat(self, dat_path):
        file_name = dat_path.stem
        return dat_path.parent / f"{file_name}.ctrl"

    def _parse_value_from_xml(self, xml_path):
        root = parse(xml_path).getroot()
        raw_date = root.find("StatusRecord").find("DateTime").text
        return raw_date

    def _parse_date_from_string(self, date_string):
        return datetime.strptime(date_string, "%Y%m%d%H%M%S")


@dataclass(frozen=True)
class MeshFile:
    path: str
    date_delivered: datetime
