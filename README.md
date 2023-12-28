# FRC-ML-Project-01
Convert table PDF to Excel format from Annual Financial Report Documents using Machine Learning

## Kaggle Notebook for initial inference
https://www.kaggle.com/mdazmainmahtab/ppocr-inference-chinese/edit

## Data Annotation
* Convert pdf to images & download by running code from https://www.kaggle.com/code/sarwaarr/notebook0c4892e18b
* After download, crop specific tables from those images
* Use <code>PPOCRLabelv2</code> labeling tool to generate annotations for those cropped table images 
  * Correct wrong text/numbers
  * Modify & correct excel
* Get Html for the modified Excel table using https://tableizer.journalistopia.com/ and remove -
  * css
  * <code>class="tableizer-table"</code>
  * <code>class="tableizer-firstrow"</code>
* Replace in the annotation file <code>gt.txt</code> -
  * <code>"structure":</code> / <code>"tokens":</code> with html stucture only
  * <code>"gt":</code> with the html code
