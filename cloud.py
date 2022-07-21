from fastapi import FastAPI, UploadFile, File, Form

app = FastAPI()

@app.post('/')
def plant(my_file: UploadFile = File(...)):
    # return {'name': my_file.filename, 'first': first}
    if my_file is not None:
        return {'plant': 'Photo Provided'}
    else:
        return {'plant': 'No Photo Provided'}