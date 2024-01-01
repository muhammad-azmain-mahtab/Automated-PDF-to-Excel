import tkinter as tk
from tkinter import scrolledtext

def extract_tags(html):
    tags = []
    in_tag = False
    current_tag = ""

    ignore_count = 0
    max_ignore = 3

    for char in html:
        if char == '<':
            in_tag = True
            current_tag = "<"
        elif char == '>':
            in_tag = False
            current_tag += ">"
            if ignore_count < max_ignore:
                ignore_count += 1
            else:
                tags.append(current_tag)
            current_tag = ""
        elif in_tag and ignore_count >= max_ignore:
            current_tag += char

    # Remove the last three tags
    tags = tags[:-3]

    return tags

def extract_and_display_tags():
    html_content = text_widget.get("1.0", tk.END)
    html_tags = extract_tags(html_content)
    
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, str(html_tags).replace("'", '"'))

# Create the main window
root = tk.Tk()
root.title("HTML Tag Extractor")

# Text input for HTML
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
text_widget.grid(row=0, column=0, padx=10, pady=10)

# Button to extract tags
extract_button = tk.Button(root, text="Extract Tags", command=extract_and_display_tags)
extract_button.grid(row=1, column=0, pady=5)

# Text output for result
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
result_text.grid(row=2, column=0, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
