# FRC-ML-Project-01
FRC - convert table PDF to Excel format from Annual Financial Report Documents

## Kaggle Notebook for initial inference
https://www.kaggle.com/code/sarwaarr/notebook0c4892e18b

## Data Annotation
* Convert pdf to images & download by running kaagle code
* After download, crop specific tables from those images and delete others 
* Use <code>PPOCRLabelv2</code> labeling tool to generate annotations for those table images 
  * Correct wrong text/numbers
  * Modify & correct excel
* Get Html for the modified Excel table using https://tableizer.journalistopia.com/ and remove -
  * css
  * <code>class="tableizer-table"</code>
  * <code>class="tableizer-firstrow"</code>
* Replace in the annotation file <code>gt.txt</code> -
  * <code>"structure":</code> / <code>"tokens":</code> with html stucture only
  * <code>"gt":</code> with the html code
