from defusedxml.ElementTree import parse
from datetime import datetime


class MeshFile:
    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        if not isinstance(other, MeshFile):
            return NotImplemented

        return self.path == other.path

    def read_delivery_date(self):
        ctl_path = self._find_ctl_from_dat()
        date_string = self._parse_value_from_xml(ctl_path)
        parsed_date = self._parse_date_from_string(date_string)
        return parsed_date

    def _find_ctl_from_dat(self):
        file_name = self.path.stem
        return self.path.parent / f"{file_name}.ctl"

    def _parse_value_from_xml(self, xml_path):
        root = parse(xml_path).getroot()
        raw_date = root.find("StatusRecord").find("DateTime").text
        return raw_date

    def _parse_date_from_string(self, date_string):
        return datetime.strptime(date_string, "%Y%m%d%H%M%S")
