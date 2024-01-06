import fitz  # PyMuPDF
import os
from PIL import Image
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog
import threading

# Define conversion_thread globally
conversion_thread = None

def convert_pdfs_to_images(pdf_folder, output_folder, dpi, color):
    os.makedirs(output_folder, exist_ok=True)

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            pdf_output_folder = os.path.join(output_folder, os.path.splitext(pdf_file)[0])
            os.makedirs(pdf_output_folder, exist_ok=True)

            doc = fitz.open(pdf_path)
            for page_num in tqdm(range(doc.page_count), desc=f"Processing {pdf_file}"):
                page = doc.load_page(page_num)

                # Get the pixel dimensions for the current page
                pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                if color == "Grayscale":
                    # Convert the image to grayscale
                    img = img.convert('L')

                # Save the image with specified DPI
                image_filename = f"{os.path.splitext(pdf_file)[0]}-{page_num + 1}.png"
                image_path = os.path.join(pdf_output_folder, image_filename)
                img.save(image_path, dpi=(dpi, dpi))

def select_pdf_folder():
    folder_path = filedialog.askdirectory()
    pdf_folder_var.set(folder_path)

def convert_and_display():
    global conversion_thread  # Declare conversion_thread as global
    pdf_folder = pdf_folder_var.get()
    dpi = int(dpi_var.get())
    output_folder = os.path.join(pdf_folder, "output")
    color_mode = color_var.get()  # Get the selected color mode

    # Run the PDF conversion in a separate thread
    conversion_thread = threading.Thread(target=convert_pdfs_to_images, args=(pdf_folder, output_folder, dpi, color_mode))
    conversion_thread.start()

    # Check the thread status every 100 milliseconds
    window.after(100, check_thread_status)

def check_thread_status():
    global conversion_thread  # Declare conversion_thread as global
    # Check if the thread is still alive
    if conversion_thread and conversion_thread.is_alive():
        # If the thread is still running, check again after 100 milliseconds
        window.after(100, check_thread_status)
    else:
        # If the thread has finished, update the result label
        result_label.config(text="Conversion completed.")

# Create the main window
window = tk.Tk()
window.title("PDF to Image Converter")

# Get screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate position for the window to be in the center
x = (screen_width - window.winfo_reqwidth()) / 2
y = (screen_height - window.winfo_reqheight()) / 2

# Set the window position
window.geometry("+%d+%d" % (x, y))

# Variables to store user input
pdf_folder_var = tk.StringVar()
dpi_var = tk.StringVar(value="150")
color_var = tk.StringVar(value="Grayscale")  # Default color mode is RGB

# GUI components
tk.Label(window, text="PDF Folder:").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(window, textvariable=pdf_folder_var, width=40).grid(row=0, column=1, padx=5, pady=5)
tk.Button(window, text="Select Folder", command=select_pdf_folder).grid(row=0, column=2, padx=5, pady=5)

tk.Label(window, text="DPI:").grid(row=1, column=0, padx=5, pady=5)
dpi_combo = tk.Spinbox(window, from_=1, to=1000, textvariable=dpi_var, width=10)
dpi_combo.grid(row=1, column=1, padx=5, pady=5)

# Helper text for DPI
dpi_helper_text = "DPI (Dots Per Inch) determines the resolution of the image. Higher DPI results in higher quality but larger file size. \nRecommended - '150'"
tk.Label(window, text=dpi_helper_text, wraplength=300, justify="center").grid(row=2, column=1, padx=1, pady=5, sticky="w")

# Dropdown for selecting color mode
tk.Label(window, text="Color Mode:").grid(row=3, column=0, padx=5, pady=5)
color_options = ["RGB", "Grayscale"]
color_dropdown = tk.OptionMenu(window, color_var, *color_options)
color_dropdown.grid(row=3, column=1, padx=5, pady=5)

convert_button = tk.Button(window, text="Convert", command=convert_and_display)
convert_button.grid(row=4, column=0, columnspan=3, pady=10)

result_label = tk.Label(window, text="")
result_label.grid(row=5, column=0, columnspan=3, pady=5)

# Start the GUI main loop
window.mainloop()
