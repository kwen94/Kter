import subprocess
import time
import paramiko
import os
from utils import set_color


class Cli:
    def __init__(self, user, password, host, port=22):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
    
    def connect(self):
        pass


class LinuxCli(Cli):

    @staticmethod
    def test_passwd_login(user, host, passwd):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=host, username=user, password=passwd, timeout=2)
        except Exception as e:
            set_color('- 登录失败 {}'.format(e), 'red')
            return False
        else:
            return True

    @staticmethod
    def test_key_login(user, host, key_path):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key_real_path = os.path.expanduser(key_path)
        key = paramiko.RSAKey.from_private_key_file(key_real_path)

        try:
            client.connect(hostname=host, username=user, pkey=key, timeout=2)
        except Exception as e:
            set_color('- 登录失败 {}'.format(e), 'red')
            return False
        else:
            return True

    def connect(self, type='Password', PublicKeyPath=None):
        cli_name = 'SecureCRT.exe'
        command = None
        if type == 'Password':
            if not LinuxCli.test_passwd_login(self.user, self.host, self.password):
                return False
            command = '{cli_name} /SSH2 /T /L {user} /P {port} /PASSWORD {password} {host}'.format(cli_name=cli_name,
                                                                 user=self.user,
                                                                 port=self.port,
                                                                 password=self.password,
                                                                 host=self.host)
        elif type == 'PublicKey':
            if not LinuxCli.test_key_login(self.user, self.host, PublicKeyPath):
                return False
            command = '{cli_name} /SSH2 /T /L {user} /P {port} /I {PublicKeyPath} {host}'.format(cli_name=cli_name,
                                                                user=self.user,
                                                                port=self.port,
                                                                PublicKeyPath=PublicKeyPath,
                                                                host=self.host)
        cmd = subprocess.Popen(command, shell=True)
        time.sleep(0.5)
        cmd.kill()
        return True
