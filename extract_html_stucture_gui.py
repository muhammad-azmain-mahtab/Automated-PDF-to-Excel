import tkinter as tk
from tkinter import scrolledtext
import re
import pyperclip  # Import the pyperclip library for clipboard operations

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

def process_html():
    user_input = input_entry.get("1.0", "end-1c")  # Get user input from Text widget
    tokens_to_delete = ['<html>', '<body>', '<table>', '</table>', '</body>', '</html>']

    for token in tokens_to_delete:
        user_input = user_input.replace(token, '')

    spaced_tags = format_html(user_input)

    structure_list = []

    tokens = spaced_tags.split()
    for token in tokens:
        if token and token[0] != '<' and token[-1] == '>':
            match = re.match(r'([^>]+)>', token)
            if match:
                attribute_part = match.group(1)
                closing_bracket = '>'
                structure_list.append(attribute_part)
                structure_list.append(closing_bracket)
        else:
            structure_list.append(token)

    # Display the result in the Text widget
    result_text.config(state=tk.NORMAL)  # Set the Text widget state to normal to allow modification
    result_text.delete("1.0", tk.END)  # Clear previous content
    result_text.insert(tk.END, str(structure_list).replace("'", '"'))  # Display the result
    result_text.config(state=tk.DISABLED)  # Set the Text widget state to disabled to prevent further modification

def copy_to_clipboard():
    result = result_text.get("1.0", "end-1c")  # Get the result from Text widget
    pyperclip.copy(result)  # Copy the result to the clipboard

# Create the main window
window = tk.Tk()
window.title("HTML Structure List Extractor")

# Create an input Text widget
input_entry = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10)
input_entry.pack(pady=10)

# Create a button to process the HTML
process_button = tk.Button(window, text="Process HTML", command=process_html)
process_button.pack(pady=5)

# Create a Text widget to display the result
result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10, state=tk.DISABLED)
result_text.pack(pady=10)

# Create a button to copy the output text to the clipboard
copy_button = tk.Button(window, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=5)

# Run the Tkinter event loop
window.mainloop()
