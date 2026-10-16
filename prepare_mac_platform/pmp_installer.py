import os
import shutil
import stat
import subprocess
import zipfile
import tarfile

import prepare_mac_platform.pmp_global_vars as globalvars

class Installer:

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

    def _rmdir_extracted_dir(rel_dest_dir):
        cur_extract_dir = os.path.join(globalvars.EXTRACT_DIR, rel_dest_dir)
        shutil.rmtree(cur_extract_dir, ignore_errors=False)
    # ---- ---- ---- ----
    # TODO: to be tested
    def _extract_tarfile(self, archive_path, rel_dest_dir):
        try:
            cur_extract_dir = os.path.join(globalvars.EXTRACT_DIR, rel_dest_dir)
            with  tarfile.open(archive_path) as tgz_archive:
                tgz_archive.extractall(cur_extract_dir)
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
            
    def _install_from_dir(self, source_dir, apply_chmod=True):
        dir_content = os.listdir(source_dir)
        if not dir_content:
            print(f"Error: Volume dir is empty: {source_dir}")
            return

        app_dir = [dir for dir in dir_content if os.path.isdir(source_dir + '/' + dir) and ".app" in dir]
        if not app_dir:
            print(f"Error: No App found in Volume:: {source_dir}")
            return

        destination_dir = os.path.join(globalvars.APPLICATIONS_DIR, app_dir[0])
        if os.path.isdir(destination_dir):
            print(f"Application already installed: {destination_dir}")
            return

        try:
            source_dir = os.path.join(source_dir, app_dir[0])
            shutil.copytree(source_dir, destination_dir)
            # NOTE: copytree() copies all atributes but chown
            st = os.stat(source_dir)
            self._recursive_chown(destination_dir, st.st_uid, st.st_gid)
            if apply_chmod:
                # NOTE: source could have no execution permissions
                app_macos_dir = os.path.join(destination_dir, "Contents/MacOS")
                self._chmod_macos_files(app_macos_dir)
        except OSError as err:
            print(f"Error copying whole dir into Applications: {rel_dest_dir}")
    # ---- ---- ---- ----
    
    def install_application(self, archive_path, rel_dir_name):
        if ".zip" in archive_path:
            self._extract_zip(archive_path, rel_dir_name)
            self._install_from_dir(os.path.join(globalvars.EXTRACT_DIR, rel_dir_name))
        elif ".gz" in archive_path or ".gzip" in archive_path:
            print(f"Tgz: {archive_path}")
            self._extract_tarfile(archive_path, rel_dir_name)
            self._install_from_dir(os.path.join(globalvars.EXTRACT_DIR, rel_dir_name))
        elif ".tgz" in archive_path:
            self._extract_tarfile(archive_path, rel_dir_name)
            self._install_from_dir(os.path.join(globalvars.EXTRACT_DIR, rel_dir_name))
        elif ".bz2" in archive_path or ".bzip2" in archive_path:
            self._extract_tarfile(archive_path, rel_dir_name)
            self._install_from_dir(os.path.join(globalvars.EXTRACT_DIR, rel_dir_name))
        elif ".xz" in archive_path:
            self._extract_tarfile(archive_path, rel_dir_name)
            self._install_from_dir(os.path.join(globalvars.EXTRACT_DIR, rel_dir_name))
        elif ".zst" in archive_path:
            self._extract_tarfile(archive_path, rel_dir_name)
            self._install_from_dir(os.path.join(globalvars.EXTRACT_DIR, rel_dir_name))
        elif ".app" in archive_path:
            print(f"Pkg: {archive_path}")
        elif ".dmg" in archive_path:
            print(f"Dmg: {archive_path}")
            vol_dir = self._mount_dmg(archive_path, rel_dir_name)
            self._install_from_dir(vol_dir, False)
            self._umount_dmg(vol_dir)
        else:
            print(f"Unknown extension: {archive_path}")
    # ---- ---- ---- ----
# ---- ---- End of Class: Installer ---- ----
