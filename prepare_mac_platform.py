#!/usr/bin/python3

import os
import sys

#import prepare_mac_platform.pmp_global_vars as globalvars
from prepare_mac_platform.pmp_json import JsonData
from prepare_mac_platform.pmp_package import Package
from prepare_mac_platform.pmp_downloader import download_all_applications
from prepare_mac_platform.pmp_installer import install_all_applications


#   .---------------.
# --|      MAIN     |
#   '---------------'

def main():

    jdata = JsonData()
    pkg_list = jdata.get_app_objs()
    
    download_all_applications(pkg_list)
    install_all_applications(pkg_list)

    print("\n---- ---- ---- ----\n")
    print("Please, run manually one by one installed program")
    print("When a warning popup suggest to move the App to the bin")
    print("you can try it granting run permission. Do it so from:")
    print("   Preferences -> Privacy & Security -> Security")
    print("PROGRAM was blocvked from use (...) -> click on 'Open Anyway' button.")

    print("\n---- ---- ---- ---- \nWelcome to download, install and set up programs to make you comfortable with the Mac experience")

if __name__ == "__main__":
    main()
