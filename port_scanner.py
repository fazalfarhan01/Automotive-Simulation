import sys
import socket

import ipaddress
import threading


addresses = [str(ip) for ip in ipaddress.IPv4Network('192.168.0.0/24')][1:-1]

near_by_nodes = []


def is_port_open(target):
    try:
        port = 8502
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        # returns an error indicator
        result = s.connect_ex((target, port))
        s.close()
        if result == 0:
            near_by_nodes.append(target)
            return True
        else:
            return False

    except KeyboardInterrupt:
        print("\n Exiting Program !!!!")
        sys.exit()
    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
    except socket.error:
        print("\ Server not responding !!!!")
        sys.exit()


def get_near_by_nodes() -> str:
    threads = []

    for ip in addresses:
        threads.append(threading.Thread(target=is_port_open, args=[ip]))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    return near_by_nodes[0]
