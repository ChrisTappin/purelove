
import os

#��ȡĿ¼cd -> path
cd_dir = receive(client_socket)
#�ж�Ŀ¼�Ƿ����
if os.path.exists(cd_dir):
    if os.path.isdir(cd_dir):
        os.chdir(cd_dir) #�ı�Ŀ¼λ��
        path_name = get_path()
        resp = "Directory change successful"
        client.send(client_socket, resp)
    else:
        err = "[!] {}: Is not a directory\n".format(cd_dir)
        client.send(client_socket, err)
else:
    err = "[!] {}: No such directory\n".format(cd_dir)
    client.send(client_socket,err)
