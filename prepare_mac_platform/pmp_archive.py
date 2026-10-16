import os

from prepare_mac_platform.pmp_downloader import Downloader
from prepare_mac_platform.pmp_extractor import Extractor
from prepare_mac_platform.pmp_utils import Utils

class Archive(Downloader, Extractor, Utils):

    data = {}
    #version = "0.0.1"
    #   .------------------------.
    # --|   Methods: Private     |
    #   '------------------------'

    def __init__(self, data, type_str):
        self.data = data
        self.data['type_str'] = type_str
    # ---- ---- ---- ----

    # ---- ---- Setters ---- ----

    def _set_downloaded_at(self, downloaded_path):
        if os.path.exists(downloaded_path):
            self.data['downloaded'] = downloaded_path

    # ---- ---- Getters ---- ----

    def _get_downloaded_path(self):
        return self.data['downloaded']
    # ---- ---- ---- ----

    def _get_name(self):
        return self.data['name']
    # ---- ---- ---- ----

    def _get_url(self):
        return self.data['url']
    # ---- ---- ---- ----

    def _pre_download(self):
        self._run_field_command_script('pre_download')
    # ---- ---- ---- ----

    def _post_download(self):
        self._run_field_command_script('post_download')
    # ---- ---- ---- ----

    def _pre_install(self):
        self._run_field_command_script('pre_install')

    def _post_install(self):
        self._run_field_command_script('post_install')

    #   .------------------------.
    # --|   Methods: Public      |
    #   '------------------------'

    def download(self):
        self._pre_download()

        location = self.download_node(self._get_url())
        self._set_downloaded_at(location)

        self._post_download()
    # ---- ---- ---- ----

    def print_info(self):
        print(
            f'''
-- Name: {self.data['name']}
\tDescription: {self.data['description']}
\tType: {self.data['type_str']}
\tURL: {self.data['url']}
\tLicense: {self.data['license']}
\tPre-Download Cmd: {self.data['pre_download']}
\tPost-Download Cmd: {self.data['post_download']}'''
        )
    # ---- ---- ---- ----

    def install(self):
        self._pre_install()

        archive_path = self._get_downloaded_path()
        node_name = self._get_name()

        dir_path = self.extract_downloaded(archive_path, node_name)
        if not dir_path:
            return

        self._post_install()

        command = "cp -pRP \"" + dir_path + "\"/*  \"" + self.data['target_dir'] + "\""
        self._run_command_script(command)

        if ".dmg" in archive_path:
            self._umount_dmg(dir_path)
        else:
            self._rmdir_extracted_dir(dir_path)

# ---- ---- End of Class: Archive ---- ----
