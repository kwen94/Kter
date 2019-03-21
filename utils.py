import telnetlib
import re
import sys


def judge_legal_ip(one_str):
    '''
    正则匹配方法
    判断一个字符串是否是合法IP地址
    '''
    compile_ip=re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')  
    if compile_ip.match(one_str):  
        return True  
    else:  
        return False

def show(data):
    title = '{:<5}\t{:<20}\t{:<8}\t{:<20}\t{:<5}\t{:<40}'.format('序列','主机名','用户名','IP地址','密码','描述')
    print(title)
    for n, record in enumerate(data):
        print('{:<5}\t{:<20}\t{:<8}\t{:<20}\t{:<5}\t{:<40}'.format(n, record[0], record[1], record[2], '***', record[4]))
    print()
    num = input('[选择序号]>>> ').strip('\n').strip('\r\n').strip('\t').strip(' ')
    print(num)
    while True:
        if num == 'q' or num == 'qiut' or num == 'Q' or num == 'exit':
            sys.exit()
        try:
            num = int(num)
            if 0 <= num < len(data):
                return data[num]
        except:
            pass
        num = input('[输入错误][再次选择序号]>>> ').strip('\n').strip('\r\n').strip('\t').strip(' ')
        print(num)


def set_color(string, color='yellow'):
    if color == 'yellow':
        print('\033[33m{}\033[0m'.format(string))
    elif color == 'green':
        print('\033[32m{}\033[0m'.format(string))
    elif color == 'red':
        print('\033[31m{}\033[0m'.format(string))


def checkSystem(host):
    system = None
    try:
        telnetlib.Telnet(host=host, port=22, timeout=0.4)
    except Exception as e:
        try:
            telnetlib.Telnet(host=host, port=3389, timeout=0.4)
        except:
            pass
        else:
            system = 'Windows'
    else:
        system = 'Linux'

    if system is None:
        set_color('- {} 网络不可达！'.format(host), 'red')
        return None

    return system
