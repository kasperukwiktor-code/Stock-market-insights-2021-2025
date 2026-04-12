import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
CONTAINER_NAME = "raw-data"
DATA_FOLDER = "data"


def upload_files():
    client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container = client.get_container_client(CONTAINER_NAME)

    for file_name in os.listdir(DATA_FOLDER):
        if file_name.endswith(".csv"):
            file_path = os.path.join(DATA_FOLDER, file_name)
            print(f"Uploading {file_name}...")
            with open(file_path, "rb") as data:
                container.upload_blob(name=file_name, data=data, overwrite=True)
            print(f"Done: {file_name}")

    print("All files uploaded.")


if __name__ == "__main__":
    upload_files()