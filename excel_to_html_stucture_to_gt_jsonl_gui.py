import os
import json
import pandas as pd
import re
import glob
from tkinter import Tk, filedialog, Button, Label, Text, CENTER, DISABLED, NORMAL, END
from tkinter import ttk

def format_html(html):
    formatted_html = ""
    in_tag = False

    for char in html:
        if char == '<':
            in_tag = True
        elif char == '>':
            in_tag = False
            formatted_html += char + ' '

        if in_tag:
            formatted_html += char

    return formatted_html.strip()

def process_excel_to_html(root_folder, print_message):
    table_rec_folder = os.path.join(root_folder, 'tableRec_excel_output')
    output_folder = os.path.join(root_folder, 'output_files')
    os.makedirs(output_folder, exist_ok=True)

    excel_files = glob.glob(os.path.join(table_rec_folder, '*.xlsx'))

    for excel_file_path in excel_files:
        directory = os.path.dirname(excel_file_path)
        file_name = os.path.splitext(os.path.basename(excel_file_path))[0]
        df = pd.read_excel(excel_file_path, header=0, keep_default_na=False)
        html_table = df.to_html(index=False, header=True)

        output_html_path = os.path.join(output_folder, f"{file_name}_output.html")
        with open(output_html_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_table)

        html_table = re.sub(r'\sclass="[^"]*"', '', html_table)
        html_table = re.sub(r'\sstyle="[^"]*"', '', html_table)
        html_table = re.sub(r'\sborder="[^"]*"', '', html_table)

        tokens_to_delete = ['<table>', '</table>']

        for token in tokens_to_delete:
            html_table = html_table.replace(token, '')

        spaced_tags = format_html(html_table)
        structure_list = []

        tokens = spaced_tags.split()
        for token in tokens:
            if token[0] != '<' and token[-1] == '>':
                match = re.match(r'([^>]+)>', token)
                if match:
                    attribute_part = match.group(1)
                    closing_bracket = '>'
                    structure_list.append(attribute_part)
                    structure_list.append(closing_bracket)
            else:
                structure_list.append(token)

        output_tokens_path = os.path.join(output_folder, f"{file_name}_structure_tokens.txt")
        with open(output_tokens_path, 'w', encoding='utf-8') as output_file:
            for token in structure_list:
                output_file.write(token + '\n')

        print_message(f"Processed: {file_name}")

    print_message("Excel to HTML conversion complete.")

def process_gt_file(root_folder, print_message):
    input_file_path = os.path.join(root_folder, 'gt.txt')
    output_file_path = os.path.join(root_folder, 'gt.jsonl')

    with open(input_file_path, 'r', encoding="utf8") as f:
        lines = f.readlines()

    data = []
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
            for cell in obj['html']['cells']:
                cell['bbox'] = [cell['bbox'][0][0], cell['bbox'][0][1], cell['bbox'][2][0], cell['bbox'][2][1]]
            obj.pop('gt', None)
            obj['split'] = 'train'
            obj['imgid'] = i
            data.append(obj)
        except json.JSONDecodeError as e:
            print_message(f"Error decoding line {i + 1}: {e}")
            print_message(f"Problematic part of line: {line[e.pos - 20:e.pos + 20].strip()}")
            continue

    with open(output_file_path, 'w', encoding='utf-8') as f:
        for obj in data:
            json.dump(obj, f, ensure_ascii=False)
            f.write('\n')

    print_message("'gt' key removed and 'split', 'imgid' key added and converted to gt.jsonl.")

    # Load data from gt.jsonl
    input_jsonl_path = os.path.join(root_folder, 'gt.jsonl')
    with open(input_jsonl_path, 'r', encoding='utf-8') as jsonl_file:
        data = [json.loads(line) for line in jsonl_file]

    output_folder = os.path.join(root_folder, 'output_files')
    # Iterate through the output_folder to update gt.jsonl with tokens information
    for tokens_file in glob.glob(os.path.join(output_folder, '*_structure_tokens.txt')):
        file_name = os.path.splitext(os.path.basename(tokens_file))[0].rsplit('_structure_tokens', 1)[0]

        # Read the content of the structure tokens file
        with open(tokens_file, 'r', encoding='utf-8') as f:
            tokens_list = f.read().splitlines()

        # Update the corresponding entry in gt.jsonl with 'tokens' field
        for obj in data:
            if obj['filename'] == file_name+".png":
                obj['html']['structure']['tokens'] = tokens_list

    # Write the updated content to gt1.jsonl
    output_jsonl_path = os.path.join(root_folder, 'gt_final.jsonl')
    with open(output_jsonl_path, 'w', encoding='utf-8') as f:
        for obj in data:
            json.dump(obj, f, ensure_ascii=False)
            f.write('\n')

    # print_message("HTML Stucture Token added to gt_final.jsonl.")

def display_messages(print_message):
    print_message("HTML Stucture Token added to gt_final.jsonl.")

def create_gui():
    def browse_folder():
        folder_selected = filedialog.askdirectory()
        label_folder.config(text=f"Selected Folder: {folder_selected}")
        process_button.config(state=NORMAL)

    def process_folder():
        root_folder = label_folder.cget("text").replace("Selected Folder: ", "")
        process_excel_to_html(root_folder, print_message)
        process_button.config(state=DISABLED)
        generate_gt_button.config(state=NORMAL)

    def generate_gt_file():
        root_folder = label_folder.cget("text").replace("Selected Folder: ", "")
        process_gt_file(root_folder, print_message)
        generate_gt_button.config(state=DISABLED)
        display_messages(print_message)

    def print_message(message):
        text_output.config(state=NORMAL)
        text_output.insert(END, message + "\n")
        text_output.see(END)
        text_output.config(state=DISABLED)

    root = Tk()
    root.title("Data Processing GUI")

    # Center window and set size
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)

    root.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

    # Style configuration
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", highlightcolor="#52aed9", background="#ccc")
    style.configure("TLabel", padding=6, background="#52aed9")
    style.configure("TFrame", padding=6, background="#eee")

    label_folder = ttk.Label(root, text="Select the folder containing PDF images", style="TLabel")
    label_folder.pack(pady=10)

    browse_button = ttk.Button(root, text="Browse Folder", command=browse_folder, style="TButton")
    browse_button.pack()

    process_button = ttk.Button(root, text="Process Excel to HTML", command=process_folder, state=DISABLED, style="TButton")
    process_button.pack(pady=10)

    generate_gt_button = ttk.Button(root, text="Generate gt.jsonl", command=generate_gt_file, state=DISABLED, style="TButton")
    generate_gt_button.pack(pady=10)

    text_output = Text(root, height=10, width=60, state=DISABLED)
    text_output.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
