from azure.storage.blob import BlobServiceClient
from app.config.settings import AZURE_STORAGE_CONNECTION_STRING

CONTAINER_NAME = "documents"


def get_blob_service_client() -> BlobServiceClient:
    return BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)


def create_container_if_not_exists() -> None:
    client = get_blob_service_client()
    container_client = client.get_container_client(CONTAINER_NAME)
    if not container_client.exists():
        container_client.create_container()


def upload_file_to_blob(file_bytes: bytes, file_name: str) -> str:
    client = get_blob_service_client()
    blob_client = client.get_blob_client(
        container=CONTAINER_NAME,
        blob=file_name
    )
    blob_client.upload_blob(file_bytes, overwrite=True)
    return blob_client.url