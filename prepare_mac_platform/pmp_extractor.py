import os
import shutil
import stat
import subprocess
import tarfile
import zipfile

import prepare_mac_platform.pmp_global_vars as globalvars

class Extractor:

    def _recursive_chown(self, path, user, group):
        for dirpath, dirnames, filenames in os.walk(path):
            shutil.chown(dirpath, user, group)
            for filename in filenames:
                shutil.chown(os.path.join(dirpath, filename), user, group)
    # ---- ---- ---- ----

    def _chmod_macos_files(self, path):
        files = os.listdir(path)
        files = [f for f in files if os.path.isfile(path + '/' + f)]
        for f in files:
            os.chmod(os.path.join(path, f), stat.S_IRWXU | stat.S_IRGRP|stat.S_IXGRP | stat.S_IROTH|stat.S_IXOTH)
    # ---- ---- ---- ----

    def _rmdir_extracted_dir(self, cur_extract_dir):
        if globalvars.EXTRACT_DIR not in cur_extract_dir:
            return
        if not os.path.isdir(cur_extract_dir):
            return
        shutil.rmtree(cur_extract_dir, ignore_errors=False)
    # ---- ---- ---- ----

    # TODO: to be tested
    def _extract_tarfile(self, archive_path, rel_dest_dir):
        try:
            cur_extract_dir = os.path.join(globalvars.EXTRACT_DIR, rel_dest_dir)
            with  tarfile.open(archive_path) as tgz_archive:
                tgz_archive.extractall(cur_extract_dir)
            return cur_extract_dir
        except tarfile.TarError as error:
            print(error)
    # ---- ---- ---- ----

    def _extract_zip(self, archive_path, rel_dest_dir):
        try:
            print(f"Zip: {archive_path}")
            cur_extract_dir = os.path.join(globalvars.EXTRACT_DIR, rel_dest_dir)
            with zipfile.ZipFile(archive_path, 'r') as zip_archive:
                # Extract all the members of the zip archive into a specific location.
                zip_archive.extractall(path=cur_extract_dir)
            return cur_extract_dir
        except zipfile.BadZipFile as error:
            print(error)
    # ---- ---- ---- ----

    def _create_vol_dir(self, target_dir):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
    # ---- ---- ---- ----

    def _mount_dmg(self, archive_path, rel_dest_dir):
        dmg_vol_dir = os.path.join(globalvars.VOLUME_DIR, rel_dest_dir)
        try:
            self._create_vol_dir(dmg_vol_dir)
            # NOTE: hdiutils is deprecating MacOS Golden Gate version
            status = subprocess.check_output(f"diskutil image attach --readOnly --mountPoint {dmg_vol_dir} {archive_path}", shell=True, universal_newlines=True)
        except subprocess.CalledProcessError as error:
            print(f"Error trying to mount {archive_path}: {error}")
        return dmg_vol_dir
    # ---- ---- ---- ----

    def _umount_dmg(self, dmg_vol_dir):
        try:
            status = subprocess.check_output(f"diskutil unmount {dmg_vol_dir}", shell=True, universal_newlines=True)
            shutil.rmtree(dmg_vol_dir, ignore_errors=False)
        except subprocess.CalledProcessError as error:
            print(f"Error while unmounting {dmg_vol_dir}: {error}")
    # ---- ---- ---- ----

    def extract_downloaded(self, archive_path, rel_dir_name):
        if ".zip" in archive_path:
            dir_path = self._extract_zip(archive_path, rel_dir_name)
        elif ".gz" in archive_path or ".gzip" in archive_path:
            dir_path = self._extract_tarfile(archive_path, rel_dir_name)
        elif ".tgz" in archive_path:
            dir_path = self._extract_tarfile(archive_path, rel_dir_name)
        elif ".bz2" in archive_path or ".bzip2" in archive_path:
            dir_path = self._extract_tarfile(archive_path, rel_dir_name)
        elif ".xz" in archive_path:
            dir_path = self._extract_tarfile(archive_path, rel_dir_name)
        elif ".zst" in archive_path:
            dir_path = self._extract_tarfile(archive_path, rel_dir_name)
        elif ".pkg" in archive_path:
            print(f"TODO Feature not implemented yet! Pkg: {archive_path}")
        elif ".dmg" in archive_path:
            dir_path = self._mount_dmg(archive_path, rel_dir_name)
        else:
            print(f"Unknown extension: {archive_path}")
            return None
        return dir_path

    def unextract_downloaded(self, dir_path, is_vol=False):
        if is_vol:
            # Note: at this point 'dir_path' is an absolute path
            self._umount_dmg(dir_path)
            return
        
        # Note: at this point 'dir_path' is a relative path
        self._rmdir_extracted_dir(dir_path)


# ---- ---- End of Class: Extractor ---- ----