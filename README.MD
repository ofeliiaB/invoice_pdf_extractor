### Extractor Endpoint

Extracts data about items listed in pdf files and returns the data in a structured format.

### Requirements

`pip install pdfplumber`
<br>`pip install python-multipart`
<br>To run:
<br>`uvicorn main:app --reload`
<br>To test the endpoint:
<br>`http://ip:port/docs`
<br>The project should have directory called "files".

### Potential Issues (Possible Future Improvements)

- Doesn't work with identical descriptions of items (all descr have to be different).
- Doesn't work with exactly the same price and quantity for different items.
- Works only if item's description fits into 1 line.
- Works only if item description doesn't contain numbers (can work in this case if only string lines are needed as
  output, for this functionality dont run the json structuring function structure_final_result()).
- Works for 1 page pdf only.

### Notes

- The files on which the project was tested/works successfully are in "tested_files" directory.

