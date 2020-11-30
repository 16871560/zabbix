import  requests,json,paramiko,time,yaml
import os,time

file=os.path.abspath(os.path.dirname(__file__)+'/server_conf')
headers = { "Accept": "application/json, text/plain, */*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Content-Length": "83",
                    "Content-Type": "application/json;charset=UTF-8",
                    "Cookie": "SRV=80",
                    "Host": "www.cytingchechang.com",
                    "Origin": "https://www.cytingchechang.com",
                    "Pragma": "no-cache",
                    "Referer": "https://www.cytingchechang.com/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    'Sec-Fetch-Site':'same-origin',
                     'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"

                   }
data=json.dumps({"userName":"face_yhb","userPassword":"123_com_hk","auth_code":"","platformType":"0"})
def post():
        url="https://www.cytingchechang.com/pb/pv/v1/login" ###车场URL
        #url="https://beta.cytingchechang.com/pb/pv/v1/login"
        try:

            p= requests.post(url,data,headers=headers,timeout=20)
            if p.status_code ==500:

                return p.status_code
            else:
                ret = json.loads(p.text)
                return ret ###返回一个字典
        except TimeoutError as e:
            return 'reboot'
        finally:
            return ret


def reboot_os_core_dataproc_server():
    infos=get_conf()
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for host in infos.keys():
            ssh.connect(host,timeout=10,username=infos[host]["user"],password=infos[host]["pwd"])
            if infos[host].get('cmd'):
                for comand in infos[host]['cmd']:
                    stdin, stdout, stderr = ssh.exec_command(comand) ###配置文件
                    # stdin, stdout, stderr = ssh.exec_command('sh /data/shscript/reboot_data_server.sh')
                    for it in stdout:
                        print(it)
                return 1
            else:
                pass
                # stdin, stdout, stderr = ssh.exec_command('sh /tmp/test.sh')
                # stdin,stdout,stderr=ssh.exec_command('sh /data/restar_datapro.sh')  #####重启命令,如果本机有脚本，则运行脚本，如果无则执行在server_conf里面配置的cmd
def  get_conf():
    with open(file) as f:
        info = f.read()
    return yaml.load(info,Loader=yaml.FullLoader)
if __name__ == '__main__':
    while 1:


        ret=post()
        print(ret)

        if ret.get('code') not in [1,-1]:
            # print(ret.get('code'))
            print("Oops.....")
            print('starting reboot_dataproc')
            reboot_os_core_dataproc_server() ####开始执行脚本
        if ret==500:
            print("Oops.....")
            print('starting reboot_dataproc')
            reboot_os_core_dataproc_server()

        else:
                # ret=get_conf()
                # for item in ret:
                #     if ret[item].get('cmd'):
                #         print(item,ret[item],ret[item]['cmd']),
                #
                #     else:
                #         print(item,ret[item])
                print('ok')
        ret={}
        time.sleep(90)