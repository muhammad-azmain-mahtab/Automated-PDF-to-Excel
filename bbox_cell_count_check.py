import json

def check_counts(json_data):
    bbox_count = len(json_data["html"]["cells"])
    th_count = json_data["html"]["structure"]["tokens"].count("<th>")
    td_count = json_data["html"]["structure"]["tokens"].count("<td>")

    return bbox_count, th_count, td_count 

file_path = r"F:\Anaconda\Jupyter Notebooks\PaddleOCR\PaddleOCR\train_data\Dataset 100\gt.jsonl"
with open(file_path, "r") as file:
    correct_count = 0
    error_count = 0
    for line in file:
        json_data = json.loads(line)
        bbox_count, th_count, td_count= check_counts(json_data)
        if bbox_count != th_count + td_count:            
            print("Box count: ", bbox_count)
            print("Cell count: ", th_count + td_count)
            print("The counts do not match for", json_data["filename"])
            error_count += 1
        else:            
            correct_count += 1            

print("")  
print("Correct count: ", correct_count)
print("Error count: ", error_count)