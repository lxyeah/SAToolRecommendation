import os.path

from bs4 import BeautifulSoup
import src.utils.write_to_xls as wt
import src.configure as c


def init_folder():
    if not os.path.exists(c.type_uniform_table_path):
        os.mkdir(c.type_uniform_table_path)
    if not os.path.exists(c.type_uniform_checkstyle_table_path):
        os.mkdir(c.type_uniform_checkstyle_table_path)
    if not os.path.exists(c.type_uniform_findbugs_table_path):
        os.mkdir(c.type_uniform_findbugs_table_path)
    if not os.path.exists(c.type_uniform_pmd_table_path):
        os.mkdir(c.type_uniform_pmd_table_path)


def get_map_table_by_id(tool_id):
    print(tool_id)
    print('------------------------------------------------')
    res = {}
    head = []
    contents = []

    h1 = bs.find(id=tool_id)
    table = h1.nextSibling.nextSibling
    for i in table.thead.tr.children:
        text = i.text
        if text != '\n' and text != '' and text != 'Redefinable':
            head.append(text)
            print(text)

    for i in table.tbody.children:
        if i.text != '\n' and i.text != '':
            content = []
            for td in i.children:
                text = td.text
                if text != '\n' and text != '' and text != 'Yes' and text != 'No':
                    content.append(text)
                    print(text)
            contents.append(content)

    print('---------------------------------------------------')
    res['head'] = head
    res['contents'] = contents
    return res


def generate_map_table_main():
    init_folder()

    html_file = open(c.type_uniform_html_path, 'rb')
    html = html_file.read()
    bs = BeautifulSoup(html, 'html.parser')

    checkstyle_table = get_map_table_by_id('checkstyle-version-6.6')
    findbugs_table = get_map_table_by_id('findbugs-filters-version-3.0.1')
    pmd_table = get_map_table_by_id('pmd-version-5.7.0')

    wt.save_as_csv(checkstyle_table['head'], checkstyle_table['contents'],
                   c.type_uniform_checkstyle_table_path + 'checkstyle_map_table.csv')
    wt.save_as_csv(findbugs_table['head'], findbugs_table['contents'],
                   c.type_uniform_findbugs_table_path + 'findbugs_map_table.csv')
    wt.save_as_csv(pmd_table['head'], pmd_table['contents'], c.type_uniform_pmd_table_path + 'pmd_map_table.csv')


if __name__ == '__main__':
    generate_map_table_main()
