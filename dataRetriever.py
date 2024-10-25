# import os
# import pandas as pd

# # Danh sách các thư mục chứa file txt
# folder_paths = os.listdir('Data')
# folder_paths.remove('duc')
# print(folder_paths)

# # Danh sách để lưu dữ liệu từ tất cả các file
# all_data = []

# # Duyệt qua từng thư mục và từng file
# for folder in folder_paths:
#     for filename in os.listdir(f"Data/{folder}"):
#         if filename.endswith(".txt"):
#             file_path = os.path.join("Data", folder, filename)
            
#             # Đọc dữ liệu từ file txt và lưu vào list
#             with open(file_path, 'r') as file:
#                 data = file.read().split()  # Chia dữ liệu thành từng số
#                 data = [float(x) for x in data]  # Chuyển thành dạng số thực nếu cần
            
#             # Kiểm tra dữ liệu có đủ 1024 điểm không
#             if len(data) == 1024:
#                 all_data.append(data)
#             else:
#                 print(f"File {file_path} không có đủ 1024 điểm dữ liệu.")

# # Chuyển dữ liệu thành DataFrame và lưu vào CSV
# df = pd.DataFrame(all_data)
# df.to_csv("output.csv", index=False, header=False)

# print("Dữ liệu đã được lưu vào output.csv")


import os
import pandas as pd

# Thư mục mẹ chứa các thư mục con
parent_folder = 'Data'

# Lấy danh sách các thư mục con trong thư mục mẹ
folder_paths = [os.path.join(parent_folder, folder) for folder in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, folder))]
folder_paths.remove('Data/duc')

print(folder_paths)

# Danh sách để lưu dữ liệu từ tất cả các file
all_data = []


# Duyệt qua từng thư mục con và từng file trong đó
for folder in folder_paths:
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder, filename)
            
            if file_path.endswith("results.txt"):
                continue
            # Đọc dữ liệu từ file txt và lưu vào list
            with open(file_path, 'r') as file:
                data = file.read().split()  # Chia dữ liệu thành từng số
                data = [float(x) for x in data]  # Chuyển thành dạng số thực nếu cần
            
            # Kiểm tra dữ liệu có đủ 1024 điểm không
            if len(data) == 1024:
                # Lấy tên thư mục và tên file
                folder_name = os.path.basename(folder)  # Tên thư mục
                row = [folder_name, filename] + data  # Thêm tên folder và filename
                all_data.append(row)
                print(len(all_data))
            else:
                print(f"File {file_path} không có đủ 1024 điểm dữ liệu.")

print(len(all_data))

# Tạo DataFrame và thêm 2 cột đầu là tên folder và tên file
column_names = ['Folder', 'Filename'] + [f'Point_{i}' for i in range(1, 1025)]
df = pd.DataFrame(all_data, columns=column_names)

# Lưu DataFrame vào file CSV
df.to_csv("output.csv", index=False)

print("Dữ liệu đã được lưu vào output_with_folder_and_filename.csv")
