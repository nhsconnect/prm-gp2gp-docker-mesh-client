import glob
from gp2gp.uploader import MeshFile
from pathlib import Path
from defusedxml.ElementTree import parse
from datetime import datetime


class MeshInboxScanner:
    def __init__(self):
        self.directory = ""

    def scan(self, directory):
        self.directory = directory
        files = []
        file_paths = glob.glob(f"{directory}/*.dat")

        for file_path in file_paths:
            date = self._get_date(file_path)
            files.append(MeshFile(path=file_path, date_delivered=date))
        return files

    def _get_date(self, dat_path):
        ctrl_path = self._find_ctrl_from_dat(dat_path)
        date_string = self._parse_value_from_xml(ctrl_path)
        parsed_date = self._parse_date_from_string(date_string)
        return parsed_date

    def _find_ctrl_from_dat(self, dat_path):
        file_name = Path(dat_path).stem
        return f"{self.directory}/{file_name}.ctrl"

    def _parse_value_from_xml(self, xml_path):
        root = parse(xml_path).getroot()
        raw_date = root.find("StatusRecord").find("DateTime").text
        return raw_date

    def _parse_date_from_string(self, date_string):
        return datetime.strptime(date_string, "%Y%m%d%H%M%S")
