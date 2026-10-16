import json
import os
import sys

from prepare_mac_platform.pmp_package import Package

JSON_FILE_VERSION = "0.0.1"

class JsonData:
#   .--------------.
# --|   Constants  |
#   '--------------'
    CUR_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
    CUR_JSON_FILE_PATH = os.path.join(CUR_SCRIPT_PATH, "pmp_archive_list.json")

#   .--------------.
# --|   Variables  |
#   '--------------'
    json_file_path = CUR_JSON_FILE_PATH
    json_data = {}
    JSON_ATTRIB_APPS = "applications"
    
    def __init__(self, file_path=None):
        if file_path is not None:
            self.set_json_file_path(file_path)
        self.json_data = self._read_from_json_file()

#   .---------------------.
# --|   Methods: Private  |
#   '---------------------'
    def _validate_json_data(self):
        if self.json_data["version"] != JSON_FILE_VERSION:
            sys.exit(f"Error: required json file version: {PROG_VERSION}")

    # ---- ---- ---- ----
    def _read_from_json_file(self):
        #print(f"path: {self.json_file_path}")
        json_fd = open(self.json_file_path)
        self.json_data = json.load(json_fd)
        json_fd.close()

        self._validate_json_data()
        return self.json_data

#   .---------------------.
# --|   Methods: Public   |
#   '---------------------'

    #   .--------------.
    # --|   Setters    |
    #   '--------------'
    def set_json_file_path(self, file_path):
        if os.path.exists(file_path):
            self.json_file_path = file_path

    #   .--------------.
    # --|   Getters    |
    #   '--------------'
    def get_app_total_items(self):
        return (len(self.json_data[self.JSON_ATTRIB_APPS]))
    
    def get_application_data(self, index):
        return self.json_data[self.JSON_ATTRIB_APPS][index]

    def get_application_type_str(self, index):
        type_idx = self.json_data[self.JSON_ATTRIB_APPS][index]['type']
        if type_idx < len(self.json_data['types']):
            return self.json_data['types'][type_idx]
        else:
            return "Unknown"

    def get_app_url(self, index):
        return self.json_data[self.JSON_ATTRIB_APPS][index]['url']

    def get_app_objs(self):
            app_pbj_list = []
            total_apps = self.get_app_total_items()

            for i in range(total_apps):
                cur_type_str = self.get_application_type_str(i)
                cur_app_obj = Package(self.get_application_data(i), cur_type_str)
                app_pbj_list.append(cur_app_obj)
            return app_pbj_list

    #   .--------------.
    # --|   Printing   |
    #   '--------------'
    def print_fancy(self, cur_json_data):
        json_formatted_str = json.dumps(cur_json_data, indent=4)
        print(json_formatted_str)

    def print_applications(self):
        total_apps = self.get_app_total_items()
        print(f"Total applications items: {total_apps}")

        for i in range(total_apps):
            self.print_fancy(self.get_application_data(i))
            print("---- ----")

        self.print_fancy(self.json_data[self.JSON_ATTRIB_APPS])

    # ---- ---- ---- ----
    
