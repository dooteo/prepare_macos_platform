import subprocess

class Utils:
    #   .------------------------.
    # --|   Methods: Private     |
    #   '------------------------'

    def _run_command_script(self, command):
        print(f"Run cmd: \n---- ---- ----\n{command}\n---- ---- ----\n")
        try:
            status = subprocess.check_output(f"{command}", shell=True, universal_newlines=True)
            print(f"Run Cmd Status: {status}")
        except subprocess.CalledProcessError as error:
            print(f"Error while run: {command}\n{error}")
    # ---- ---- ---- ----

    def _run_field_command_script(self, field):
        command = self.data[field]
        if not command:
            return
        self._run_command_script(command)
    # ---- ---- ---- ----

# ---- ---- End of Class: Utils ---- ----

