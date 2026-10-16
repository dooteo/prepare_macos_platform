import json
import os
import sys

from prepare_mac_platform.pmp_package import Package
from prepare_mac_platform.pmp_archive import Archive

JSON_FILE_VERSION = "0.0.2"

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
    JSON_ATTRIB_ARCHIV = "archives"
    
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
    def _get_node_total_items(self, attrib):
        return (len(self.json_data[attrib]))

    def _get_node_data(self, attrib, index):
        return self.json_data[attrib][index]

    def _get_node_type_str(self, attrib, index):
        type_idx = self.json_data[attrib][index]['type']
        if type_idx < len(self.json_data['types']):
            return self.json_data['types'][type_idx]
        else:
            return "Unknown"

    def _get_node_url(self, attrib, index):
        return self.json_data[attrib][index]['url']

    #   .-------------------.
    # --|   Getters : Apps  |
    #   '-------------------'
    def get_app_total_items(self):
        return self._get_node_total_items(self.JSON_ATTRIB_APPS)
    
    def get_app_data(self, index):
        return self._get_node_data(self.JSON_ATTRIB_APPS, index)

    def get_app_type_str(self, index):
        return self._get_node_type_str(self.JSON_ATTRIB_APPS, index)

    def get_app_url(self, index):
        #return self.json_data[self.JSON_ATTRIB_APPS][index]['url']
        return self._get_node_url(self.JSON_ATTRIB_APPS, index)

    def get_app_objs(self):
            obj_list = []
            total_objs = self.get_app_total_items()

            for i in range(total_objs):
                cur_type_str = self.get_app_type_str(i)
                cur_obj = Package(self.get_app_data(i), cur_type_str)
                obj_list.append(cur_obj)
            return obj_list

    #   .-----------------------.
    # --|   Getters : Archives  |
    #   '-----------------------'
    def get_archive_total_items(self):
        return self._get_node_total_items(self.JSON_ATTRIB_ARCHIV)

    def get_archive_data(self, index):
        return self._get_node_data(self.JSON_ATTRIB_ARCHIV, index)

    def get_archive_type_str(self, index):
        return self._get_node_type_str(self.JSON_ATTRIB_ARCHIV, index)

    def get_archive_url(self, index):
        return self._get_node_url(self.JSON_ATTRIB_ARCHIV, index)


    def get_archive_objs(self):
            obj_list = []
            total_objs = self.get_archive_total_items()

            for i in range(total_objs):
                cur_type_str = self.get_archive_type_str(i)
                cur_obj = Archive(self.get_archive_data(i), cur_type_str)
                obj_list.append(cur_obj)
            return obj_list

    def get_node_objs(self):
            app_list = []
            total_objs = self.get_app_total_items()
            for i in range(total_objs):
                cur_type_str = self.get_app_type_str(i)
                cur_obj = Package(self.get_app_data(i), cur_type_str)
                app_list.append(cur_obj)

            archive_list = []
            total_objs = self.get_archive_total_items()
            for i in range(total_objs):
                cur_type_str = self.get_archive_type_str(i)
                cur_obj = Archive(self.get_archive_data(i), cur_type_str)
                archive_list.append(cur_obj)

            return app_list, archive_list

    #   .--------------.
    # --|   Printing   |
    #   '--------------'
    def print_fancy(self, cur_json_data):
        json_formatted_str = json.dumps(cur_json_data, indent=4)
        print(json_formatted_str)

    def print_applications(self):
        total_apps = self.get_app_total_items()
        print(f"Total application items: {total_apps}")

        for i in range(total_apps):
            self.print_fancy(self.get_app_data(i))
            print("---- ----")

        self.print_fancy(self.json_data[self.JSON_ATTRIB_APPS])

    def print_archives(self):
        total_apps = self.get_archive_total_items()
        print(f"Total archvie items: {total_apps}")

        for i in range(total_apps):
            self.print_fancy(self.get_app_data(i))
            print("---- ----")

        self.print_fancy(self.json_data[self.JSON_ATTRIB_ARCHIV])

    # ---- ---- ---- ----
    
