import requests
import base64

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Путь к файлу учетных данных сервисного аккаунта
SERVICE_ACCOUNT_FILE = "credentials.json"
# Области доступа
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# Получение учетных данных
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
# Создание сервиса для работы с Google Drive API
service = build("drive", "v3", credentials=credentials)

def upload_file(file_path, file_name):
    # Метаданные файла
    file_metadata = {"name": file_name}
    # Загрузка файла
    media = MediaFileUpload(file_path)
    # Создание файла в Google Drive
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"  # Исправлено имя аргумента
    ).execute()

    # Получение идентификатора файла
    file_id = file.get("id")

    # Установка прав доступа к файлу
    service.permissions().create(
        fileId=file_id,
        body={
            "role": "reader",
            "type": "anyone"
        }
    ).execute()

    return file_id

def get_links(url):
    try:
        request = requests.get(url)
        
        request.raise_for_status()
        json_data = request.json()

        links = json_data.get("links", [])
        encode_links(links)
    except Exception as error:
        logging.error(error)

def encode_links(links):
    encoded_links = [
        base64.b64encode(
            link.encode("utf-8")
        ).decode("utf-8") for link in links
    ]
    
    save_links(encoded_links)

def save_links(encoded_links):
    with open("subscription.txt", "w") as file:
        for link in encoded_links:
            file.write(f"{link}\n")

