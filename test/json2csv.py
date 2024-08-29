import json
import csv

# 读取 JSON 文件
json_file_path = 'files/mme_lib.json'
csv_file_path = 'v1-1/dist/main/lib.csv'

with open(json_file_path, 'r',encoding='utf-8') as json_file:
    data_list = json.load(json_file)
    for data in data_list:
        if "," in data["writer"]:
            data["writer"] = data["writer"].replace(",", "/")

# 写入 CSV 文件

with open(csv_file_path, 'w', newline='',encoding='utf-8-sig') as csv_file:
    fieldnames = data_list[0].keys() if data_list else []  # 获取表头字段
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    # 写入表头
    csv_writer.writeheader()
    # 写入数据
    csv_writer.writerows(data_list)

print(f'Data has been saved to {csv_file_path}')
