# FRC-ML-Project-01
Convert table PDF to Excel format from Annual Financial Report Documents using Machine Learning

## Kaggle Notebook for initial inference
https://www.kaggle.com/mdazmainmahtab/ppocr-inference-chinese

## Data Annotation
* Convert pdf to images & download by running code from https://www.kaggle.com/code/sarwaarr/notebook0c4892e18b
* After download, crop specific tables from those images
* Use <code>PPOCRLabelv2</code> labeling tool to generate annotations for those cropped table images
  * <code>activate paddle_env && PPOCRLabel</code> use this command on anaconda prompt to run PPOCRLabelv2
  * Correct wrong text/numbers
  * Modify & correct excel
* Get Html for the modified Excel table using https://tableizer.journalistopia.com/ and remove -
  * css
  * <code>class="tableizer-table"</code>
  * <code>class="tableizer-firstrow"</code>
* Replace in the annotation file <code>gt.txt</code> -
  * <code>"structure":</code> / <code>"tokens":</code> with html stucture only
  * <code>"gt":</code> with the html code

## How to install PPOCRLabelv2
* Download and install <code>Ancaonda</code> https://www.anaconda.com/download
* Run <code>Ancaonda Prompt</code> and use the following commands
  * conda env remove --name paddle_env
  * conda create -n paddle_env python=3.10
  * activate paddle_env
  * python -m pip install paddlepaddle==2.5.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
  * pip install PPOCRLabel
  * pip install pywin32
  * PPOCRLabel
