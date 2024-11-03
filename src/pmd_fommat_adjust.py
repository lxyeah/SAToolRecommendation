import os
import csv
import configure as c

data_dir = c.data_dir

for i in os.listdir(data_dir):
    pro_dir = data_dir + '/' + i
    for j in os.listdir(pro_dir):
        if j.endswith('pmd_labeled.csv'):
            res = []
            file_path = pro_dir + '/' + j
            with open(file_path, 'r', errors='ignore') as f:
                reader = csv.reader(f)
                for k in reader:
                    if len(k) == 11:
                        res.append(k)
                    elif len(k) == 12:
                        k[10] = k[11]
                        res.append(k[:11])
            f.close()

            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(res)
            f.close()