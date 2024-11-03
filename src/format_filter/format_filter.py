import src.utils.write_to_xls as wtx
import os
import src.configure as c


def findbugs_format_filter(file_path):
    lines = wtx.read_csv(file_path)
    res = []
    for line in lines:
        if line[3].split('.')[-1].split('$')[0].endswith('Test'):
            continue
        else:
            res.append(line)
    wtx.write_csv(file_path, res)


def pmd_format_filter(file_path):
    lines = wtx.read_csv(file_path)
    res = []
    for line in lines:
        print(line)
        type = line[6]
        if type == 'Documentation' or type == 'Code Style':
            continue
        else:
            res.append(line)
    wtx.write_csv(file_path, res)


if __name__ == '__main__':
    report_path = c.report_path
    for i in os.listdir(report_path):
        for j in os.listdir(os.path.join(report_path, i)):
            if j.endswith('_findbugs.csv'):
                findbugs_format_filter(os.path.join(report_path, i, j))
            elif j.endswith('_pmd.csv'):
                pmd_format_filter(os.path.join(report_path, i, j))
            else:
                continue
