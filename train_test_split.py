import os
import json
from shutil import copyfile
from sklearn.model_selection import train_test_split

root_folder = os.getcwd()
jsonl_file_path = os.path.join(root_folder, 'gt.jsonl')
table_dataset_split_folder = os.path.join(root_folder, 'Final Table Dataset Split')

os.makedirs(table_dataset_split_folder, exist_ok=True)

with open(jsonl_file_path, 'r', encoding='utf-8') as f:
    json_lines = f.readlines()

# Split the data into train and test sets (60:40 ratio)
train_data, test_data = train_test_split(json_lines, test_size=0.4, random_state=42)

# Function to update imgid and split values, and copy images to respective folders
def update_imgids_and_split(data, split_value, source_folder, train_folder, test_folder):
    updated_data = []
    for i, line in enumerate(data):
        try:
            obj = json.loads(line)
            obj['imgid'] = i
            obj['split'] = split_value
            updated_data.append(json.dumps(obj, ensure_ascii=False) + '\n')

            filename = obj['filename']
            source_path = os.path.join(source_folder, filename)
            destination_folder = train_folder if split_value == "train" else test_folder
            destination_path = os.path.join(destination_folder, filename)
            copyfile(source_path, destination_path)
        except json.JSONDecodeError as e:
            print(f"Error decoding line {i + 1}: {e}")
            continue
        except FileNotFoundError as e:
            print(f"Error copying file for line {i + 1}: {e}")
            continue
    return updated_data

# Define source and destination folders for images
source_images_folder = os.path.join(root_folder, 'Merged Dataset')
train_images_folder = os.path.join(table_dataset_split_folder, 'train')
test_images_folder = os.path.join(table_dataset_split_folder, 'val')

# Create train and test folders if they don't exist
os.makedirs(train_images_folder, exist_ok=True)
os.makedirs(test_images_folder, exist_ok=True)

# Update imgids and split values for train and test sets, and copy images
train_data = update_imgids_and_split(train_data, "train", source_images_folder, train_images_folder, test_images_folder)
test_data = update_imgids_and_split(test_data, "test", source_images_folder, train_images_folder, test_images_folder)

# Write the modified content back to the train and test JSON Lines files
train_output_path = os.path.join(table_dataset_split_folder, 'gt_train.jsonl')
test_output_path = os.path.join(table_dataset_split_folder, 'gt_test.jsonl')

with open(train_output_path, 'w', encoding='utf-8') as f:
    f.writelines(train_data)

with open(test_output_path, 'w', encoding='utf-8') as f:
    f.writelines(test_data)

print("Imgids and split values updated successfully, and data split into train and test sets.")
