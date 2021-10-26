import socket
import json
import nxbt


def read_credential(path):
    with open(path, 'r') as f:
        content = f.read()
    cred_dict = json.loads(content)
    return cred_dict['host'], cred_dict['port']


def bind_socket(params):
    thost, tport = params
    print('host: {}'.format(thost))
    print('port: {}'.format(tport))
    ss = socket.socket()
    ss.bind(params)
    return ss


def connect_nx():
    nx = nxbt.Nxbt()
    print('nxbt object created')
    controller_index = nx.create_controller(nxbt.PRO_CONTROLLER)
    # print('nxbt controller index: {}'.format(controller_index))
    print('waiting for connection')
    nx.wait_for_connection(controller_index)
    print('connected')
    return nx, controller_index


def run_macro(tnx, controller_index, tmacro):
    tnx.macro(controller_index, tmacro)


if __name__ == '__main__':
    credential_path = '../credential/controller_ip_credential.json'
    host, port = read_credential(credential_path)
    ss = bind_socket((host, port))

    nx, nxci = connect_nx()
    print('Await for macro commands...')

    quit_v = True

    while quit_v:
        ss.listen()
        cs, addr = ss.accept()
        print('connection from: {}'.format(str(addr)))

        macro = ''
        while True:
            data = cs.recv(1024).decode()
            if not data:
                break
            macro += data
        cs.send('accepted macro:\n{}'.format(macro))
        cs.close()
        print('RUN:\n{}'.format(macro))
        if macro == 'quit()':
            quit_v = False
        run_macro(nx, nxci, macro)
