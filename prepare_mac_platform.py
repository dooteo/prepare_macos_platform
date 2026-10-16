#!/usr/bin/python3

import os
import sys

import prepare_mac_platform.pmp_global_vars as globalvars
from prepare_mac_platform.pmp_json import JsonData
from prepare_mac_platform.pmp_package import Package
from prepare_mac_platform.pmp_archive import Archive

#   .---------------.
# --|   Functions   |
#   '---------------'
def download_all_objs(node_obj_list):
    create_dir(globalvars.DOWNLOADS_DIR)

    for cur_obj in node_obj_list:
        cur_obj.download()
# ---- ---- ---- ----

def install_all_objs(node_obj_list):
    print("-- Install Step --")
    for cur_obj in node_obj_list:
        cur_obj.install()
# ---- ---- ---- ----

def print_all_obj_info(node_obj_list):
    for cur_obj in node_obj_list:
        cur_obj.print_info()
# ---- ---- ---- ----

def create_dir(target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
# ---- ---- ---- ----


#   .---------------.
# --|      MAIN     |
#   '---------------'

def main():
    print("\n---- ---- ---- ---- \nWelcome to download, install and set up programs to make you comfortable with the Mac experience")

    jdata = JsonData()
    app_list, archive_list = jdata.get_node_objs()

    print_all_obj_info(app_list)
    download_all_objs(app_list)
    install_all_objs(app_list)

    print_all_obj_info(archive_list)
    download_all_objs(archive_list)
    install_all_objs(archive_list)

    print("\n---- ---- ---- ----\n")
    print("Please, run manually one by one installed program")
    print("When a warning popup suggest to move the App to the bin")
    print("you can try it granting run permission. Do it so from:")
    print("   Preferences -> Privacy & Security -> Security")
    print("PROGRAM was blocked from use (...) -> click on 'Open Anyway' button.")


if __name__ == "__main__":
    main()
