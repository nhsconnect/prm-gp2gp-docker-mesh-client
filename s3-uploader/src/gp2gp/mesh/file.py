from defusedxml.ElementTree import parse, ParseError
from datetime import datetime


EVENT_TYPE_TRANSFER = "TRANSFER"


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
        try:
            root = parse(xml_path).getroot()
            status_record = root.find("StatusRecord")
            raw_date = status_record.find("DateTime").text
            event_type = status_record.find("Event").text
            if event_type == EVENT_TYPE_TRANSFER:
                return raw_date
            else:
                raise MeshFileException(
                    f"Unexpected event type in CTRL file, path: {xml_path}, event: {event_type}"
                )
        except ParseError as e:
            raise MeshFileException(f"Invalid XML in CTRL file, {xml_path}") from e
        except AttributeError as e:
            raise MeshFileException(f"Unexpected XML structure in CTRL file, {xml_path}") from e

    def _parse_date_from_string(self, date_string):
        return datetime.strptime(date_string, "%Y%m%d%H%M%S")


class MeshFileException(Exception):
    pass
