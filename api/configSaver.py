import os

# 설정 파일 경로
CONFIG_FILE = "option.txt"

# 내부 저장소
_config_data = {}


def get(key):
    """키에 해당하는 값을 반환."""
    global _config_data
    return _config_data.get(key, None)


def put(key, value):
    """키에 해당하는 값을 설정."""
    global _config_data
    _config_data[key] = value


def isKey(key):
    """키가 존재하는지 확인."""
    global _config_data
    return key in _config_data


def save():
    """내부 저장소 데이터를 옵션 파일에 저장."""
    global _config_data
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        for key, value in _config_data.items():
            file.write(f"{key} = {value}\n")
    print("저장된 모든 데이터를 파일에 저장했습니다.")


def load():
    """옵션 파일을 읽어 내부 저장소를 초기화."""
    global _config_data
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    key, value = line.split("=", 1)
                    _config_data[key.strip()] = value.strip()
    print("파일에서 모든 데이터를 로드했습니다.")