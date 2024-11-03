import os


def find_file_in_folder(target_file, root_path):
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file == target_file:
                print(os.path.abspath(os.path.join(root, file)))
                return os.path.abspath(os.path.join(root, file))
    return False


if __name__ == '__main__':
    find_file_in_folder('SynchronousCommandTransport.java', 'E:\\data_info\\projects\\remoting\\unzip_repos\\remoting-A\\remoting-remoting-2.21')