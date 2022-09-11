import socket


def check_address_is_available(tcp_ip, tcp_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((tcp_ip, tcp_port))
        raise Exception(f'IP-адрес {tcp_ip} на порту {tcp_port} уже используется')

    finally:
        s.close()
