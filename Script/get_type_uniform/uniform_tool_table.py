import src.configure as c
import src.utils.write_to_xls as wt
import os


def init_folder():
    if not os.path.exists(c.type_uniform_uniform_path):
        os.mkdir(c.type_uniform_uniform_path)
    if not os.path.exists(c.type_uniform_checkstyle_uniform_path):
        os.mkdir(c.type_uniform_checkstyle_uniform_path)
    if not os.path.exists(c.type_uniform_findbugs_uniform_path):
        os.mkdir(c.type_uniform_findbugs_uniform_path)
    if not os.path.exists(c.type_uniform_pmd_uniform_path):
        os.mkdir(c.type_uniform_pmd_uniform_path)


def get_map_table_from_csv(tool_name):
    map_table_csv = wt.get_from_csv(c.type_uniform_table_path + tool_name + '/{}_map_table.csv'.format(tool_name))[1:]
    return map_table_csv


def grt_warning_list_from_csv(tool_name):
    warning_list = wt.get_from_csv(c.res_path + c.pro_name + '/{}_res'.format(tool_name) + c.csv_res + '/{}.csv'.format(c.pro_name))[1:]
    return warning_list


def construct_map_dict(map_table):
    map_dict = {}
    for i in map_table:
        map_dict[i[0]] = i[1]
    return map_dict


def get_map_dict(tool_name):
    map_table_csv = get_map_table_from_csv(tool_name)
    map_table = []
    if tool_name == 'findbugs':
        map_table = map_table_csv
        return construct_map_dict(map_table)
    elif tool_name == 'checkstyle':
        map_table = map_table_csv
        return construct_map_dict(map_table)
    elif tool_name == 'pmd':
        for i in map_table_csv:
            pmd_type = str(i[0])
            if pmd_type.endswith('.xml'):
                continue
            else:
                pmd_type = pmd_type.split('/')[1]
                i[0] = pmd_type
                map_table.append(i)
        return construct_map_dict(map_table)
    else:
        print('Error Tool!!')


def get_adjust_warning_list(tool_name):
    warning_list = grt_warning_list_from_csv(tool_name)
    adjust_warning_list = []
    if tool_name == 'findbugs':
        for i in warning_list:
            path = i[c.findbugs_index['file_path']]
            start = i[c.findbugs_index['lstart']]
            warning_type = i[c.findbugs_index['category']]
            adjust_warning_list.append([path, start, warning_type])
        return adjust_warning_list
    elif tool_name == 'checkstyle':
        for i in warning_list:
            path = i[c.checkstyle_index['file']].split('java/')[1]
            start = i[c.checkstyle_index['line']]
            warning_type = i[c.checkstyle_index['source']].split('.')[-1].split('Check')[0]
            adjust_warning_list.append([path, start, warning_type])
        return adjust_warning_list
    elif tool_name == 'pmd':
        for i in warning_list:
            path = i[c.pmd_index['File']].split('java/')[1].replace('/', '/')
            start = i[c.pmd_index['Line']]
            warning_type = i[c.pmd_index['Rule']]
            adjust_warning_list.append([path, start, warning_type])
        return adjust_warning_list
    else:
        print('Error Tool!!')


def uniform(tool_name):
    map_dict = get_map_dict(tool_name)
    warning_list = get_adjust_warning_list(tool_name)
    for i in warning_list:
        warning_type = i[2]
        uniform_warning_type = map_dict.get(warning_type)
        i[2] = uniform_warning_type
    wt.save_as_csv(c.uniform_head, warning_list, c.type_uniform_uniform_path + tool_name + '/' + 'uniform_{}'.format(tool_name) + '.csv')


def uniform_tool_table_main():
    init_folder()

    uniform('checkstyle')
    uniform('findbugs')
    uniform('pmd')


if __name__ == '__main__':
    uniform_tool_table_main()

