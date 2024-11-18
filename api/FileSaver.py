import os

def saveFile(dictionary, fileName):
    """
    dictionary 데이터를 지정된 파일에 저장합니다.
    """
    fileloc = f"data/{fileName}.txt"
    try:
        # 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(fileloc), exist_ok=True)

        with open(fileloc, "w", encoding="utf-8") as file:
            for delay, action in dictionary.items():
                # 파일에 데이터를 기록
                file.write(f"{delay}:{action}\n")
        print(f"파일 저장 성공: {fileloc}")
        return True
    except Exception as e:
        print(f"파일 저장 실패: {e}")
        return False


def loadFile(fileName):
    """
    지정된 파일에서 dictionary 데이터를 불러옵니다.
    """
    fileloc = f"data/{fileName}.txt"
    dictionary = {}
    try:
        if not os.path.exists(fileloc):
            print(f"파일이 존재하지 않습니다: {fileloc}")
            return {}

        with open(fileloc, "r", encoding="utf-8") as file:
            for line in file:
                if ":" in line:
                    delay, action = line.strip().split(":", 1)
                    dictionary[float(delay)] = action
        print(f"파일 로드 성공: {fileloc}")
        return dictionary
    except Exception as e:
        print(f"파일 로드 실패: {e}")
        return {}
