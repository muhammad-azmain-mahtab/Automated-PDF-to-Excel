Convert table PDF to Excel format from Annual Financial Report Documents using Machine Learning

## Kaggle Notebook for initial inference
https://www.kaggle.com/mdazmainmahtab/ppocr-inference-chinese

# Instructions

## Install PPOCRLabelv2
* Download and install <code>Anaconda</code> https://www.anaconda.com/download
* Run <code>Anaconda Prompt</code> and use the following commands
  * conda env remove --name paddle_env
  * conda create -n paddle_env python=3.10
  * activate paddle_env
  * python -m pip install paddlepaddle==2.5.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
  * pip install PPOCRLabel
  * pip install pywin32
  * PPOCRLabel

## Prepare Table Data for Annotation
* PDF name format - <code>tradingcode-year.pdf</code>
* Create a folder and add it to windows defender exclusion list
* Convert pdf to images using <code>[pdf_to_image_gui.exe](https://github.com/AzmainO7/FRC-ML-Project-01/releases/download/Preview/pdf_to_image_gui.exe)</code>
  <!-- * Run <code>Anaconda Prompt</code>
  * Copy & paste <code>activate paddle_env && python "...\pdf_to_image_gui.py"</code>, replace "...\pdf_to_image_gui.py" with the actual path where <code>pdf_to_image_gui.py</code> is stored in your device -->
  * In the opened window select PDF folder and press convert
  * Once completed "Conversion completed" message will be shown below
* After conversion, crop specific tables from those images
  
## Data Annotation
* Ensure Microsoft Excel is installed on your system
* Use <code>PPOCRLabelv2</code> labeling tool to generate annotations for those cropped table images
  * <code>activate paddle_env && PPOCRLabel</code> use this command on anaconda prompt to run PPOCRLabelv2
  * Go to the top left <code>File</code> section and click <code>Open Dir</code> to open the folder where the cropped images are stored
  * After opening a table picture, click on the <code>Table Recognition</code> button in the upper right corner of PPOCRLabel, which will call the table recognition model in PP-Structure to automatically label the table and pop up Excel at the same time.
  * Save and close Excel after making adjustments and correcting errors
  * Correct wrong text/numbers on the <code>Recognition Results</code> section on the right side
  * Adjust cell order: Drag all the results under the <code>Recognition Results</code> column on the right side of the software interface to make the box numbers are arranged from left to right, top to bottom
  * Finally click on <code>Check</code> button on the bottom right and move on to another table image
  * Once all the images are done and checked, go to the top left <code>File</code> section and click <code>Export Table Label</code> which will generate the <code>gt.txt</code> file
* Get Html for the modified Excel table using https://tableizer.journalistopia.com/
  * Tick <code>no css</code> button
  * Remove <code>class="tableizer-table"</code>
  * Remove <code>class="tableizer-firstrow"</code>
* Replace in the annotation file <code>gt.txt</code> -
  * <code>"gt":</code> with the html code
  * <code>"structure":</code> / <code>"tokens":</code> with html stucture extracted from the html code using <code>[extract_html_stucture_gui.exe](https://github.com/AzmainO7/FRC-ML-Project-01/releases/download/Preview/extract_html_stucture_gui.exe)</code>

