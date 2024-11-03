import generate_map_table as gmt
import uniform_tool_table as utt
import src.utils.write_to_xls as wt
import src.configure as c

if __name__ == '__main__':
    # gmt.generate_map_table_main()
    # utt.uniform_tool_table_main()
    uniform_checkstyle_path = c.type_uniform_checkstyle_uniform_path + '/uniform_checkstyle.csv'
    uniform_findbugs_path = c.type_uniform_findbugs_uniform_path + '/uniform_findbugs.csv'
    uniform_pmd_path = c.type_uniform_pmd_uniform_path + '/uniform_pmd.csv'

    checkstyle_res = wt.get_from_csv(uniform_checkstyle_path)[1:]
    findbugs_res = wt.get_from_csv(uniform_findbugs_path)[1:]
    pmd_res = wt.get_from_csv(uniform_pmd_path)[1:]

    for i in checkstyle_res:
        i.append('checkstyle')
    for i in findbugs_res:
        i.append('findbugs')
    for i in pmd_res:
        i.append('pmd')

    total_res = checkstyle_res + findbugs_res + pmd_res
    total_dic = {}
    for i in total_res:
        key = i[0] + '&' + i[1] + '&' + i[2]
        if key not in total_dic.keys():
            total_dic[key] = [1, [i[3]]]
        else:
            total_dic[key][0] += 1
            total_dic[key][1].append(i[3])
    for i in total_dic.keys():
        if total_dic.get(i)[0] != 1:
            print(i + ': ' + str(total_dic.get(i)))