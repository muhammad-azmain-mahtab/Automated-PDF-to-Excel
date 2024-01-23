import os
import shutil

def merge_gt_files(root_folder, output_file):
    folders = [folder for folder in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, folder))]
    merged_content = ""
    merged_images_folder = os.path.join(root_folder, 'merged_images')

    if not os.path.exists(merged_images_folder):
        os.makedirs(merged_images_folder)

    for folder in folders:
        folder_path = os.path.join(root_folder, folder)
        gt_file_path = os.path.join(folder_path, "gt_final.jsonl")

        if os.path.exists(gt_file_path):
            print(gt_file_path)
            with open(gt_file_path, 'r') as file:
                current_content = file.read()

            merged_content += f"{current_content}"

            # Copy all files from the subfolder to the merged_images_folder
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    print(file_path)
                    shutil.copy(file_path, merged_images_folder)

    with open(output_file, 'w') as output_file:
        output_file.write(merged_content)

if __name__ == "__main__":
    root_folder = os.getcwd()
    output_file = os.path.join(root_folder, 'merged_gt.jsonl')
    merge_gt_files(root_folder, output_file)
