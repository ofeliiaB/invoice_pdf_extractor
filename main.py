from fastapi import FastAPI, File, UploadFile
from extractor import Extractor

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(input_currency_symbol, file: UploadFile = File(...)):
    file_location = f"files/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    extractor = Extractor(file.filename, input_currency_symbol=input_currency_symbol)
    result = extractor.extract_structured_data()
    return result
