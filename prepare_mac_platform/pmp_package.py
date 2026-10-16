import os

from prepare_mac_platform.pmp_downloader import Downloader
from prepare_mac_platform.pmp_installer import Installer
from prepare_mac_platform.pmp_utils import Utils

class Package(Downloader, Installer, Utils):

    data = {}
    #version = "0.0.1"
    #   .------------------------.
    # --|   Methods: Private     |
    #   '------------------------'

    def __init__(self, data):
        self.data = data


    # ---- ---- Setters ---- ----

    def _set_downloaded_at(self, downloaded_path):
        if os.path.exists(downloaded_path):
            self.data['downloaded'] = downloaded_path

    # ---- ---- Getters ---- ----

    def _get_downloaded_path(self):
        return self.data['downloaded']
    # ---- ---- ---- ----

    def _get_pkg_name(self):
        return self.data['name']
    # ---- ---- ---- ----

    def _get_url(self):
        return self.data['url']

    def _pre_download(self):
        self._run_field_command_script('pre_download')

    def _post_download(self):
        self._run_field_command_script('post_download')

    def _pre_install(self):
        self._run_field_command_script('pre_install')

    def _post_install(self):
        self._run_field_command_script('post_install')

    #   .------------------------.
    # --|   Methods: Public      |
    #   '------------------------'

    def download(self):
        self._pre_download()

        location = self.download_application(self._get_url())
        self._set_downloaded_at(location)

        self._post_download()

    def print_info(self):
        print(
            f'''
-- Name: {self.data['name']}
\tDescription: {self.data['description']}
\tURL: {self.data['url']}
\tLicense: {self.data['license']}
\tPre-Download Cmd: {self.data['pre_download']}
\tPost-Download Cmd: {self.data['post_download']}
\tPre-Install Cmd: {self.data['pre_install']}
\tPost-Install Cmd: {self.data['post_install']}'''
        )

    # ---- ---- ---- ----

    def install(self):
        self._pre_install()

        location = self._get_downloaded_path()
        pkg_name = self._get_pkg_name()
        self.install_application(location, pkg_name)

        self._post_install()
