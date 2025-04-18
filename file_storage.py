
import os
import hashlib

FILES_DIR = './files'
MAX_FILES = 999                  # Максимальное число файлов в каталоге
MAX_FILE_SIZE = 5 * 1024 * 1024  # Максимальный размер файла в байтах (5 МБ)

class FileSizeLimitError(Exception):
    pass

def ensure_files_dir_exists():
    os.makedirs(FILES_DIR, exist_ok=True)

def cleanup_files_dir():
    """
    Если в каталоге FILES_DIR больше MAX_FILES файлов,
    удаляет самый старый файл (по времени последнего изменения).
    """
    ensure_files_dir_exists()
    files = [os.path.join(FILES_DIR, f) for f in os.listdir(FILES_DIR)]
    files = [f for f in files if os.path.isfile(f)]
    if len(files) > MAX_FILES:
        oldest = min(files, key=lambda f: os.path.getmtime(f))
        os.remove(oldest)

def save_binary_file(data: bytes) -> str:
    """
    Сохраняет бинарные данные в каталог FILES_DIR с именем по sha256 хешу.
    Если файл уже есть — не сохраняет второй раз.
    Если размер файла превышает MAX_FILE_SIZE — возбуждает исключение.
    Возвращает имя файла (sha256).
    """
    if len(data) > MAX_FILE_SIZE:
        raise FileSizeLimitError("File size exceeds the maximum allowed limit")
    ensure_files_dir_exists()
    cleanup_files_dir()
    file_hash = hashlib.sha256(data).hexdigest()
    file_path = os.path.join(FILES_DIR, file_hash)
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(data)
    return file_hash
