#!/usr/bin/python3

import os
import sys

import prepare_mac_platform.pmp_global_vars as globalvars
from prepare_mac_platform.pmp_json import JsonData
from prepare_mac_platform.pmp_package import Package

#   .---------------.
# --|   Functions   |
#   '---------------'

def create_dir(target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
# ---- ---- ---- ----

def print_all_app_info(applications):
    for cur_app in applications:
        cur_app.print_info()
# ---- ---- ---- ----

def download_all_applications(applications):
    create_dir(globalvars.DOWNLOADS_DIR)

    for cur_app in applications:
        cur_app.download()
# ---- ---- ---- ----

def install_all_applications(applications):
    print("-- Install Applications Step --")
    for cur_app in applications:
        cur_app.install()
# ---- ---- ---- ----

def install_all_archives(archives):
    print("-- Install Archives Step --")
    for cur_archive in archives:
        cur_archive.install()
# ---- ---- ---- ----


#   .---------------.
# --|      MAIN     |
#   '---------------'

def main():
    print("\n---- ---- ---- ---- \nWelcome to download, install and set up programs to make you comfortable with the Mac experience")

    jdata = JsonData()
    pkg_list = jdata.get_app_objs()
    
    print_all_app_info(pkg_list)
    download_all_applications(pkg_list)
    install_all_applications(pkg_list)

    print("\n---- ---- ---- ----\n")
    print("Please, run manually one by one installed program")
    print("When a warning popup suggest to move the App to the bin")
    print("you can try it granting run permission. Do it so from:")
    print("   Preferences -> Privacy & Security -> Security")
    print("PROGRAM was blocked from use (...) -> click on 'Open Anyway' button.")


if __name__ == "__main__":
    main()
