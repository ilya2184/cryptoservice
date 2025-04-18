
import os
from file_storage import FILES_DIR
import gostcrypto.gosthash as ghosthash

# Маппинг поддерживаемых алгоритмов
ALGORITHMS = {
    "GOST R 34.11-2012 256": "streebog256",
    "GOST R 34.11-2012 512": "streebog512",
}

def hash_file(params):
    """
    params: dict с полями 'data' (имя файла), 'algorithm', 'inverted_halfbytes', 'client'
    Возвращает: status ("success"/"fail"), data (hash или описание ошибки)
    """
    filename = params.get('data')
    algorithm = params.get('algorithm')
    # Проверки на обязательные параметры
    if not filename or not algorithm:
        return "fail", "Missing required parameter(s): data or algorithm"

    if algorithm not in ALGORITHMS:
        return "fail", f"Unsupported algorithm: {algorithm}"

    file_path = os.path.join(FILES_DIR, filename)
    if not os.path.isfile(file_path):
        return "fail", "File not found"

    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
        algo = ALGORITHMS[algorithm]
        # Получаем хеш через gostcrypto.gosthash
        hash_obj = ghosthash.new(algo, data=file_data)
        h = hash_obj.hexdigest()
        # Если нужно что-то с inverted_halfbytes — пока игнорируем
        return "success", h
    except Exception as e:
        return "fail", str(e)
