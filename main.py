from utils.gemini import chat_with_gemini_as_astronomy_expert
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    Response,
    StreamingResponse,
)
from fastapi import FastAPI, Request, File, UploadFile, Form
from schemas.schemas import ModelInputForm, ChatMessage
from utils.utils import get_models, get_models_names
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from utils.constants import Constants
from io import BytesIO
import os
from typing import List
from utils.model_creator import ExoplanetRandomForestModelGenerator
import pandas as pd
import time

app = FastAPI()

models = get_models()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=Constants.TEMPLATE_DIR)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "models": get_models_names(),
            "required_features": Constants.FEATURES_REQUIRED_TO_PREDICT_STRING,
        },
    )


@app.get("/learn", response_class=HTMLResponse)
async def transit(request: Request):
    return templates.TemplateResponse(request=request, name="learn.html")


@app.post("/predict/manual", response_class=JSONResponse)
async def predict_manual(request: Request, form: ModelInputForm):
    try:
        assert len(form.to_list()) == Constants.LENGTH_OF_FEATURES_REQUIRED_TO_PREDICT
        assert None not in form.to_list()
        return {"prediction": models[form.model].predict(form.to_list())}
    except Exception as e:
        return {"error": str(e)}


@app.post("/predict/csv")
async def predict_csv(
    request: Request, model: str = Form(...), file: UploadFile = File(...)
):
    count_confirmed, count_candidate, count_false_positive = 0, 0, 0
    if not file.filename.endswith(".csv"):
        return {"message": "Invalid file type. Please upload a CSV file."}

    contents = await file.read()

    data_buffer = BytesIO(contents)
    df = pd.read_csv(data_buffer, comment="#")
    if len(df) > 100:
        return Response(
            status_code=413,  # 413 Payload Too Large
        )
    columns = df.columns.tolist()
    missing_features = list(set(Constants.FEATURES_REQUIRED_TO_PREDICT) - set(columns))
    if len(missing_features) > 0:
        return JSONResponse(
            status_code=422,
            content={
                "message": f"Missing required features: {', '.join(missing_features)}"
            },
        )
    data_buffer.close()

    def process_row(row):
        prediction = models[model].predict(
            ModelInputForm(**row.to_dict(), model=model).to_list()
        )
        if prediction == "Confirmed":
            nonlocal count_confirmed
            count_confirmed += 1
        elif prediction == "Candidate":
            nonlocal count_candidate
            count_candidate += 1
        else:
            nonlocal count_false_positive
            count_false_positive += 1
        return prediction

    df["prediction"] = df.apply(lambda row: process_row(row), axis=1)

    await file.close()
    data = {
        "data": df,
        "columns": columns,
        "num_rows": len(df),
        "count_confirmed": count_confirmed,
        "count_candidate": count_candidate,
        "count_false_positive": count_false_positive,
        "total_count": len(df),
    }
    return templates.TemplateResponse(
        request=request,
        name="components/dataset_result_table.html",
        context=data,
    )


@app.post("api/predict/csv", response_class=JSONResponse)
async def predict_csv_api(request: Request, model: str, file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return {"message": "Invalid file type. Please upload a CSV file."}

    contents = await file.read()

    data_buffer = BytesIO(contents)

    df = pd.read_csv(data_buffer, comment="#")
    if len(df) > 100:
        return Response(
            {
                "message": "File too large. Please upload a CSV file with less than 100 rows."
            },
            status_code=413,
        )

    data_buffer.close()

    df["prediction"] = df.apply(lambda row: models[model].predict(row), axis=1)

    await file.close()
    return df["prediction"].tolist()


@app.get("/model-info", response_class=HTMLResponse)
async def model_info(request: Request):
    return templates.TemplateResponse(request=request, name="model-info.html")


@app.get("/model/{model_name}")
async def get_model_info(model_name: str):
    if model_name not in models:
        return JSONResponse(status_code=404, content={"message": "Model not found"})

    model = models[model_name]
    return {
        "model_name": model_name,
        "features": model.features,
        "target": model.target,
        "description": model.description,
    }


@app.get("/train", response_class=JSONResponse)
async def train_model(request: Request):
    def train():
        # 1. preprocessing
        yield "Preprocessing data"
        time.sleep(2)  # Simulate time-consuming task
        # 2. training
        yield "Training model"
        time.sleep(3)  # Simulate time-consuming task
        # 3. evaluation
        yield "Evaluating model"
        time.sleep(4)  # Simulate time-consuming task
        yield "Model training complete"

    return StreamingResponse(train(), media_type="text/event-stream")


@app.get("/tales-from-the-stars")
async def tales_from_the_stars(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="tales-from-the-stars.html",
    )


@app.get("/test-model")
async def test_model(request: Request, model: str, file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return {"message": "Invalid file type. Please upload a CSV file."}

    contents = await file.read()

    data_buffer = BytesIO(contents)

    df = pd.read_csv(data_buffer, comment="#")
    if len(df) > 100:
        return Response(
            {
                "message": "File too large. Please upload a CSV file with less than 100 rows."
            },
            status_code=413,
        )

    data_buffer.close()

    df["prediction"] = df.apply(lambda row: models[model].predict(row), axis=1)

    await file.close()
    # check the predictions
    df["prediction"].tolist()
    return templates.TemplateResponse(
        request=request,
        name="test-model.html",
        context={
            "models": get_models_names(),
        },
    )


@app.post("/chat")
async def chat(msg: ChatMessage):
    print(msg.message)
    return {"reply": chat_with_gemini_as_astronomy_expert(msg.message)}


@app.get("/model/{model_name}/confusion-matrix", response_class=JSONResponse)
async def get_confusion_matrix(model_name: str):
    if model_name not in models:
        return JSONResponse(status_code=404, content={"message": "Model not found"})

    model = models[model_name]
    cm = getattr(model, "confusion_matrix", None)
    if cm is None:
        return {
            "confusion_matrix": [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ]
        }

    try:
        cm_list = cm.tolist() if hasattr(cm, "tolist") else cm
    except Exception:
        cm_list = cm

    return {"confusion_matrix": cm_list}


@app.post("/custom-model/train", response_class=JSONResponse)
async def train_custom_model(
    request: Request,
    model_name: str = Form(...),
    files: List[UploadFile] = File(...),
):
    # Save uploaded CSVs into dataset/content
    dataset_dir = os.path.join("dataset", "content")
    os.makedirs(dataset_dir, exist_ok=True)

    saved_paths = []
    for f in files:
        if not f.filename.endswith(".csv"):
            return JSONResponse(status_code=422, content={"message": "Only CSV files are allowed."})
        contents = await f.read()
        save_path = os.path.join(dataset_dir, f.filename)
        with open(save_path, "wb") as out:
            out.write(contents)
        saved_paths.append(save_path)
        await f.close()

    try:
        generator = ExoplanetRandomForestModelGenerator(csv_paths=saved_paths, target_col="koi_disposition")
        generator.load_and_validate()
        X_train_res, X_test, y_train_res, y_test = generator.preprocess()
        generator.train(X_train_res, y_train_res)
        generator.evaluate(X_test, y_test)
        generator.save(output_name=model_name, output_dir="models")
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    # refresh models cache
    global models
    models = get_models()

    return {"status": "ok", "model": model_name}
