import logging
import os
from datetime import datetime
import yaml

# === Loglama Ayarları ===
LOG_FILE = "logs/app.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_info(message):
    print(f"INFO: {message}")
    logging.info(message)

def log_error(message):
    print(f"ERROR: {message}")
    logging.error(message)

# === YAML Dosyası Yükleyici ===
def load_yaml_config(file_path):
    """YAML dosyalarını yükler."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# === Zaman Hesaplayıcı ===
def timeit(func):
    """Fonksiyonun çalışma süresini hesaplar."""
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        duration = datetime.now() - start_time
        log_info(f"{func.__name__} çalıştı. Süre: {duration.total_seconds()} saniye")
        return result
    return wrapper
