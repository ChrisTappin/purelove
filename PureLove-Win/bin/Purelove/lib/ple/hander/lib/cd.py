
import os

#��ȡĿ¼cd -> path
cd_dir = ""
#�ж�Ŀ¼�Ƿ����
def cd_path(cd_dir):
    if os.path.exists(cd_dir):
        if os.path.isdir(cd_dir):
            os.chdir(cd_dir) #�ı�Ŀ¼λ��
            path_name = get_path()
            return parh_name
        else:
            err = "[!] {}: Is not a directory\n".format(cd_dir)
            return err
    else:
        err = "[!] {}: No such directory\n".format(cd_dir)
        return err
