import os
import re
import urllib.request
# NOTE: import requests # not available in MacOS basic python
# NOTE: import wget  # not available in MacOS basic python
import shutil

import prepare_mac_platform.pmp_global_vars as globalvars

class Downloader:

    #   .------------------------.
    # --|   Methods: Private     |
    #   '------------------------'

    def _urllib_exception(e):
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)

    #   .------------------------.
    # --|   Methods: Public      |
    #   '------------------------'

    def download_application(self, cur_url):
        print(f'---- URL: {cur_url}')
        target_file_path = ""
        try:
            req = urllib.request.Request(cur_url, data=None, headers=globalvars.USER_AGENT_HEADER)
            
            with urllib.request.urlopen(req) as response:
                if response.getheader('Content-Disposition') is None:
                    target_file_path = os.path.join(globalvars.DOWNLOADS_DIR, os.path.basename(response.url))
                else:
                    fname = re.findall("filename\*?=([^;]+)", response.getheader('Content-Disposition'), flags=re.IGNORECASE)
                    target_file_path = os.path.join(globalvars.DOWNLOADS_DIR, fname[0].strip().strip('"'))

                if os.path.isfile(target_file_path):
                    print(f'---- Previously downloaded: {target_file_path}')
                    return target_file_path

                with open(target_file_path, 'wb') as fdest:
                    shutil.copyfileobj(response, fdest)
            return target_file_path
        except urllib.error.HTTPError as e:
            _urllib_exception(e)
    # ---- ---- ---- ----

# ---- ---- End of Class: Downloader ---- ----


