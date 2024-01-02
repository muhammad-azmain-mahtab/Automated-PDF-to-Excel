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
  * Correct wrong text/numbers
  * Modify & correct excel
* Get Html for the modified Excel table using https://tableizer.journalistopia.com/
  * Tick <code>no css</code> button
  * Remove <code>class="tableizer-table"</code>
  * Remove <code>class="tableizer-firstrow"</code>
* Replace in the annotation file <code>gt.txt</code> -
  * <code>"gt":</code> with the html code
  * <code>"structure":</code> / <code>"tokens":</code> with html stucture extracted from the html code using <code>[extract_html_stucture_gui.exe](https://github.com/AzmainO7/FRC-ML-Project-01/releases/download/Preview/extract_html_stucture_gui.exe)</code>

