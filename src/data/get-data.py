import requests
from loguru import logger
from src.config import settings


def write_file(response: requests.Response) -> None:
    """
    Writes the content of a response to a file.

    Opens a file in binary write mode at the path specified by the
    Settings class, combining `data_path` and `data_filename`.
    Iterates over the response content in chunks and writes each
    chunk to the file.

    Args:
        response: The HTTP response object whose content is to be written.
    """
    with open(settings.data_path / settings.data_filename, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)


if __name__ == "__main__":
    response = requests.get(settings.data_url, stream=True)
    if response.status_code == 200:
        write_file(response)
        logger.success(
            f"File downloaded successfully and stored at {settings.data_path / settings.data_filename}"
        )
    else:
        logger.error(
            f"Failed to download file. HTTP status code: {response.status_code}"
        )
