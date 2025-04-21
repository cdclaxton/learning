# Populate a Word document from an Excel file

The data in `dataset.xlsx` is read by the Word template `Populate from Excel.dotm`. The dataset has five rows (one header row and four data rows) and four columns, as shown below.

![Dataset in Excel](./images/Dataset%20in%20Excel.png)

The Word template contains two placeholders in which content from the Excel file is inserted.

![Template Word document](./images/Template%20Word%20document.png)

By following the instructions below, the template will be auto-populated with the data from the Excel file to produce a document as shown below.

![Populated Word document](./images/Populated%20Word%20document.png)

## Instructions

1. Double-click `Populate from Excel.dotm` to create a new document from the template.
2. Once the document is loaded, a file dialog box will appear with the title 'Select Excel file to read'.
3. Select the file `dataset.xlsx` and click 'OK'.
4. The Word document will be auto-populated by data from the Excel file using VBA macros.
5. Save the populated Word document (as the opened file is a `.dotm` template, pressing Ctrl+S will automatically bring up the Save File dialog box).
