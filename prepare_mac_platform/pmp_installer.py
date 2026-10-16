import os
import shutil
import stat

import prepare_mac_platform.pmp_global_vars as globalvars

class Installer:

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
                # NOTE: source could have no execution permissions
                app_macos_dir = os.path.join(destination_dir, "Contents/MacOS")
                self._chmod_macos_files(app_macos_dir)
        except OSError as err:
            print(f"Error copying whole dir into Applications: {rel_dest_dir}")
    # ---- ---- ---- ----
    
    def install_application_old(self, archive_path, rel_dir_name):
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

    def install_application(self, archive_path, rel_dir_name):
        dir_path = self.extract_downloaded(archive_path, rel_dir_name)
        if not dir_path:
            return
        
        if ".dmg" in archive_path:
            self._install_from_dir(dir_path, False)
            self._umount_dmg(dir_path)
        else:
            self._install_from_dir(dir_path)    
            self._rmdir_extracted_dir(dir_path)
        
        
            
# ---- ---- End of Class: Installer ---- ----
