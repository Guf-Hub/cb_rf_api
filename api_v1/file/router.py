from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse


import pandas as pd
import io

router = APIRouter(tags=["File"])

# https://habr.com/ru/articles/710376/


@router.get("/download", summary="Скачать файл", response_class=FileResponse)
def download_file():
    return FileResponse(
        path="cost_price.xlsx",
        filename="Статистика покупок.xlsx",
        media_type="multipart/form-data",
    )


@router.post(
    "/upload-bytes",
    summary="Загрузить файл в байтах",
)
def upload_file_bytes(file_bytes: bytes = File()):
    return {"file_bytes": str(file_bytes)}


@router.post(
    "/upload-file",
    summary="Загрузить файл",
)
def upload_file(file: UploadFile):

    try:
        # Прочитать содержимое файла в байтовый поток
        data = io.BytesIO(file.file.read())

        # Определяем формат файла на основе content_type
        if (
            file.content_type
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            df = pd.read_excel(data)
        elif file.content_type == "text/csv":
            df = pd.read_csv(data)
        elif file.content_type == "application/json":
            df = pd.read_json(data)
        else:
            raise HTTPException(
                status_code=400,
                detail="Неподдерживаемый формат файла. Поддерживаемые форматы: XLSX, CSV, JSON.",
            )

        # Убираем дубликаты
        df = df.drop_duplicates()

        # Проверяем наличие необходимых столбцов
        # if "date_from" not in df.columns or "barcode" not in df.columns:
        #     raise HTTPException(
        #         status_code=400,
        #         detail="Отсутствуют необходимые столбцы: 'date_from' и 'barcode'.",
        #     )
        if "date_from" in df.columns or "barcode" in df.columns:
            # Обработка даты и типа баркода
            df["date_from"] = pd.to_datetime(
                df["date_from"], errors="coerce"
            ).dt.date  # Преобразуем в дату, игнорируем ошибки
            df["barcode"] = df["barcode"].astype(str)

        # Конвертация DataFrame в список словарей
        data = df.to_dict("records")

        # Возвращаем результат

        # async with async_session_factory() as session:
        #     await async_create_db()
        #     result = [TechCostPrice(**item) for item in data]
        #     session.add_all(result)
        #     await session.commit()

        return {"data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {str(e)}")
