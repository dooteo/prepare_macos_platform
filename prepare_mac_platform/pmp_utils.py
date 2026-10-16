import subprocess

class Utils:
    #   .------------------------.
    # --|   Methods: Private     |
    #   '------------------------'

    def _run_field_command_script(self, field):
        command = self.data[field]
        if not command:
            return
        print(f"Run cmd: \n---- ---- ----\n{command}\n---- ---- ----\n")
        return
        try:
            status = subprocess.check_output(f"{command}", shell=True, universal_newlines=True)
        except subprocess.CalledProcessError as error:
            print(f"Error while run: {command}\n{error}")

    # ---- ---- ---- ----

# ---- ---- End of Class: Utils ---- ----

