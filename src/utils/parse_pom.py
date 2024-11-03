import xml.etree.ElementTree as ET
import os


def get_modules(root_path):
    res = []
    tree = ET.ElementTree(file=root_path + 'pom.xml')
    root = tree.getroot()
    for child in root:
        if child.tag.endswith('modules'):
            for module in child:
                print(module.text)
                res.append(module.text)
    return res


def get_module_info(root_path, root_module, res):
    pom_path = root_path + 'pom.xml'
    if os.path.exists(pom_path):
        modules = get_modules(root_path)
        if len(modules) == 0:
            res.append(root_module)
        else:
            temp = []
            for module in modules:
                get_module_info(root_path + '/' + module + '/', module, temp)
            res.append(temp)


if __name__ == '__main__':
    root_path = 'D:/data_info/projects/Achilles/unzip_repos/Achilles-E/Achilles-achilles-2.0.10-dse/'
    res = ['Achilles-E']
    get_module_info(root_path, 'Achilles-E', res)
    print(res)