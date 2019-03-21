from Lnxtools import LinuxCli
from Wintools import WinCli
from table import myexcel
import utils
import sys
import paramiko
import os
from utils import set_color


#  使用时设置alias环境变量，让其可以在任一目录运行


DIR_NAME = os.path.dirname(sys.argv[0])
ABS_PATH = os.path.abspath(DIR_NAME)

class WinExec:

    _FAT='10.10.10'
    _UAT='10.10.20'
    _PRO='10.0.1'

    def __init__(self, host):
        self.host = host
        self.win = WinCli()

    def exec(self):
        rdp_path = self.get_rdp_path()
        if rdp_path is None:
            set_color('- rdp文件未发现')
            return
        self.win.connect(rdp_path, self.host)
    
    def get_rdp_path(self):
        if self.host.startswith(self._FAT) | self.host.startswith(self._UAT) | self.host.startswith(self._PRO):
            rdp_path = 'mstsc_rdp/default.rdp'
        else:
            set_color('- Windows环境中未发现该网段IP')
            rdp_path = None
        return rdp_path


class Terminal:
    env = ['test', 'fat', 'uat', 'pro']
    default_passwd_sheet_name = '通用密码'
    excel_path = '{}/passwd/passwd.xlsx'.format(ABS_PATH)
    privatekey_path = '{}/passwd/id_rsa'.format(ABS_PATH)


    def __init__(self, var):
        self.var = var
        self.excel = myexcel(self.excel_path)
        self.result = self.excel.get(self.env)
        self.default_passwd = self.excel.get(self.default_passwd_sheet_name)

    def run(self):
        if self.var:
            if utils.judge_legal_ip(self.var):
                system = utils.checkSystem(self.var)
                if system == 'Linux':
                    set_color('检测系统为：Linux', 'green')
                    self.specific(self.result, self.var)
                elif system == 'Windows':
                    set_color('检测系统为：Windows', 'green')
                    WinExec(self.var).exec()
                else:
                    sys.exit()
            else:
                self.ambiguous(self.result, var)

    def specific(self, result, host):  # 精确匹配
        match = []
        user = None
        password = None
        for _, v in result.items():
            for i in v:
                if i[2] == str(host):
                    user = i[1]
                    password = i[3]
                    match.append(i)

        if len(match) == 1:
            LinuxCli(user, password, host).connect()

        elif len(match) == 0:
            set_color('- IP未匹配')
            self.tars_jump('root', host)

        else:   # 多选条件
            match_record = utils.show(match)
            user = match_record[1]
            password = match_record[3]
            host = match_record[2]
            LinuxCli(user, password, host).connect()

    def ambiguous(self,result, var):  # 模糊匹配
        match = []
        for _, v in result.items():
            for n, i in enumerate(v):
                if n == 0:
                    continue
                tmp_i = i[:]
                tmp_i.pop(3)
                if str(tmp_i).find(var) != -1:
                    match.append(i)

        if len(match) == 1:
            tmp_record = match[0][:]
            tmp_record[3] = "***"
            set_color('匹配到记录 {}'.format(tmp_record), 'green')
            LinuxCli(match[0][1], match[0][3], match[0][2]).connect()

        elif len(match) == 0:
            set_color('- IP未匹配')

        else:   # 多选条件
            match_record = utils.show(match)
            user = match_record[1]
            password = match_record[3]
            host = match_record[2]
            LinuxCli(user, password, host).connect()

    def tars_jump(self, user, host):  # 使用私钥登录
        set_color('- 使用私钥登录')
        if not LinuxCli(user, None, host).connect(type='PublicKey', PublicKeyPath=self.privatekey_path):
            password = self.default_passwd.get('通用密码')[1][1]
            self.passwd_login(password, host=host, user=user)# 使用通用密码登录

    def passwd_login(self, password, host, user='root'):
        set_color('- 使用通用密码登录')
        LinuxCli(user, password, host).connect()



var = sys.argv[1]
print()
Terminal(var).run()



