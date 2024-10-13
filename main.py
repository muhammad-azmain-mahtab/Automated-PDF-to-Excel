from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import zipfile
import io
from io import BytesIO
import fitz
from PIL import Image
import os
import subprocess
from tqdm import tqdm
import shutil
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2
import csv

import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

app = FastAPI()

@app.post("/process_pdf/")

async def process_pdf(pdf_file: UploadFile = File(...)):
    try:
        content = await pdf_file.read()
        
        images = convert_pdf_to_images(content)
        pdf_name = pdf_file.filename.split(".")[0]

        output_dir = "PaddleOCR\inference\images"
        os.makedirs(output_dir, exist_ok=True)

        for idx, img_bytes in tqdm(enumerate(images, start=1), desc='Converting PDF to images'):
            rgb_image = Image.open(BytesIO(img_bytes))
            gray_image = rgb_image.convert("L")

            image_name = f"{pdf_name}_page{idx}.png"
            gray_image_path = os.path.join(output_dir, image_name)
            gray_image.save(gray_image_path, dpi=(150, 150))
            
        print("pdf to image conversion complete.")
        
        # Load the model
        model = YOLO('PaddleOCR\inference\yolov8s-table-detect.pt') 

        crop_dir = 'PaddleOCR\inference\cropped images'
        if not os.path.exists(crop_dir):
            os.makedirs(crop_dir)

        image_list = os.listdir(output_dir)

        # Load the classification model
        classification_model = YOLO("PaddleOCR\inference\yolov8n-table-classify.pt")
        pathlib.PosixPath = temp

        # Loop through each image in the directory
        for image_name in tqdm(image_list, desc="Detecting Tables"):
            # Construct the full image path
            image_path = os.path.join(output_dir, image_name)
            
            # Open the image
            img = Image.open(image_path)

            # Convert image to array
            img_array = np.array(img)

            # Convert grayscale to RGB if necessary
            if len(img_array.shape) == 2:  # Grayscale image
                img_array = np.stack((img_array,) * 3, axis=-1)  # Convert to RGB
            
            # Perform inference
            results = model.predict(img_array, conf=0.80, iou=0.50, agnostic_nms=False, max_det=2, verbose=False)
            
            # Check if any tables were detected
            if results[0].boxes.shape[0] > 0:  # if there are any boxes detected
                # Loop through each detected table
                for box in results[0].boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()  # Convert tensor to list
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to int
                    # Cropping
                    cropped_image = img.crop((x1, y1, x2, y2))  # Crop the image
                    # Save the cropped image with a unique name
                    crop_path = os.path.join(crop_dir, f"{image_name.split('.')[0]}.png")
                    cropped_image.save(crop_path)
                    
        classified_dir = "PaddleOCR\inference\classified tables"
        if not os.path.exists(classified_dir):
            os.makedirs(classified_dir)

        csv_file_path = os.path.join(classified_dir, 'classification_results.csv')
        # Create the CSV file and write the header
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Filename', 'Class'])

        # Classify detected tables
        for image_name in tqdm(os.listdir(crop_dir), desc="Classifying Tables"):
            # Construct the full image path
            image_path = os.path.join(crop_dir, image_name)
            
            # Open the cropped image
            cropped_img = Image.open(image_path)
            
            # Convert cropped image to array
            cropped_img_array = np.array(cropped_img)

            # Convert grayscale to RGB if necessary
            if len(cropped_img_array.shape) == 2:  # Grayscale image
                cropped_img_array = np.stack((cropped_img_array,) * 3, axis=-1) 
            
            # Perform classification
            classification_results = classification_model.predict(cropped_img_array, verbose=False)

            top_class_index = classification_results[0].probs.top1
            top_class_label = classification_results[0].names[top_class_index]
            top_class_confidence = classification_results[0].probs.top1conf

            # Add the text to the image
            text = f'Prediction: {top_class_label}: {top_class_confidence:.2f}'
            position = (10, 30)
            font_scale = 0.5
            thickness = 1
            cv2.putText(cropped_img_array, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), thickness, cv2.LINE_AA)
    
            classified_table_path = os.path.join(classified_dir, image_name)
            cv2.imwrite(classified_table_path, cropped_img_array)

            # Append the filename and classification result to the CSV file
            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([image_name, top_class_label])

        run_ocr(crop_dir)

        output_dir = os.path.join(os.path.dirname(os.getcwd()),"inference", "images")
        shutil.rmtree(output_dir)

        cropped_dir = os.path.join(os.path.dirname(os.getcwd()),"inference", "cropped images")
        shutil.rmtree(cropped_dir)

        zip_path = os.path.join(os.path.dirname(os.getcwd()), "inference", "output.zip")
        output_dir = os.path.join(os.path.dirname(os.getcwd()), "inference", "output")
        # print(output_dir)

        structure_dir = os.path.join(output_dir, "structure")

        # Move files from subdirectories of structure to directly inside output_dir
        for root, dirs, files in os.walk(structure_dir):
            for dirname in dirs[:]:
                dir_path = os.path.join(root, dirname)
                if os.path.isdir(dir_path):
                    shutil.move(dir_path, output_dir)

        # Function to check if a directory contains any .xlsx files
        def contains_xlsx_files(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(".xlsx"):
                        return True
            return False
        
        # Function to remove non-xlsx files from a directory
        def remove_non_xlsx_files(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if not file.endswith(".xlsx"):
                        os.remove(os.path.join(root, file))

        # Create folders for each class and move the existing folders/files
        class_dirs = {}
        with open(os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), csv_file_path), mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                image_name = row['Filename']
                class_name = row['Class']

                # Extract the relevant part of the filename
                folder_name = os.path.splitext(image_name)[0]
                
                # Create class directory if it doesn't exist
                if class_name not in class_dirs:
                    class_dir = os.path.join(os.path.dirname(os.getcwd()), "inference", "output", class_name)
                    # print(class_dir)
                    os.makedirs(class_dir, exist_ok=True)
                    class_dirs[class_name] = class_dir
                
                # Move the folder corresponding to the extracted part of the filename into the class folder
                image_folder_path = os.path.join(os.path.dirname(os.getcwd()), "inference", "output", folder_name)
                # print(image_folder_path)
                if os.path.isdir(image_folder_path):
                    shutil.move(image_folder_path, class_dirs[class_name])

        # Iterate through each directory in output_dir
        for dirpath, dirnames, filenames in os.walk(output_dir):
            for dirname in dirnames:
                dir_path = os.path.join(dirpath, dirname)
                if not contains_xlsx_files(dir_path):
                    print(f"Deleting empty directory: {dir_path}")
                    shutil.rmtree(dir_path)
                else:
                    remove_non_xlsx_files(dir_path) 

        def stream_zip_file(file_path):
            with open(file_path, "rb") as file:
                while True:
                    chunk = file.read(65536)  # Read 64 KB at a time
                    if not chunk:
                        break
                    yield chunk

        @app.post("/download_zip/")
        async def download_zip():
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, output_dir))

            return StreamingResponse(
                stream_zip_file(zip_path),
                media_type="application/x-zip-compressed",
                headers={"Content-Disposition": "attachment; filename=output.zip"}
            )

    except Exception as e:
        return {"error": str(e)}

def convert_pdf_to_images(content: bytes):
    images = []
    with fitz.open(stream=BytesIO(content)) as pdf_document:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(150 / 72, 150 / 72))      
            img_buffer = io.BytesIO()
            pix.pil_save(img_buffer, format="PNG")
            img_buffer.seek(0)
            images.append(img_buffer.getvalue())
    return images

def run_ocr(output_dir):
    os.chdir("PaddleOCR/ppstructure")
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    output_dir = parent_directory + '\\' + output_dir.split('\\', 1)[1]

    for root, dirs, files in os.walk(output_dir):
        for file in tqdm(files, desc="Processing images"):
            if file.endswith(".png"):
                image_path = os.path.join(root, file)
                print("\nImage Path:", image_path)
                print(os.getcwd())
                command = [
                    "conda", "run", "-n", "paddle_env",
                    "python", "predict_system.py",
                    f"--det_model_dir={parent_directory}\\inference\\ch_PP-OCRv4_det_infer",
                    f"--rec_model_dir={parent_directory}\\inference\\ch_PP-OCRv4_rec_infer",
                    f"--table_model_dir={parent_directory}\\inference\\SLANet_best_accuracy_omar158",
                    f"--layout_model_dir={parent_directory}\\inference\\picodet_lcnet_x1_0_layout_infer",
                    f"--image_dir={image_path}",
                    f"--rec_char_dict_path={parent_directory}\\ppocr\\utils\\ppocr_keys_v1.txt",
                    f"--table_char_dict_path={parent_directory}\\ppocr\\utils\\dict\\table_structure_dict.txt",
                    f"--output={parent_directory}\\inference\\output",
                    f"--vis_font_path={parent_directory}\\doc\\fonts\\simfang.ttf"
                ]
                res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # print(f"COMMAND:\n{' '.join(res.args)}")
                print(f"STDERR: {repr(res.stderr)}")
                print(f'STDOUT: {res.stdout}')
                print(f'RETURN CODE: {res.returncode}')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
