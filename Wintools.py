import subprocess
import time
import re
import pickle


class WinCli:
    def __init__(self):
        pass

    def connect(self, rdp_path, ip):
        cli_name = 'mstsc.exe'
        command = '{} {}'.format(cli_name, rdp_path)
        self._update_rdp(rdp_path, ip)
        cmd = subprocess.Popen(command, shell=True)
        time.sleep(0.2)
        cmd.kill()

    def _update_rdp(self, rdp_path, ip):
        address_str = 'full address:s:'
        
        with open(rdp_path, 'r') as f:
            lines = f.readlines()

        with open(rdp_path, 'w') as f_w:
            for line in lines:
                if line.startswith(address_str):
                    line = '{}{}\n'.format(address_str, ip)
                f_w.write(line)
