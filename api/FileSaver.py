import os

def saveFile(control, fileName):
    """
    튜플 데이터를 지정된 파일에 저장합니다.
    (시간, 동작) 형태의 튜플을 저장
    """
    fileloc = f"data/{fileName}.txt"
    # 파일을 쓰기 모드로 열기
    with open(fileloc, "w", encoding="utf-8") as file:
        file.write(control)

    print(f"파일 저장 성공: {fileloc}")
    return True

def loadFile(fileName):
    """
    지정된 파일에서 튜플 데이터를 불러옵니다.
    (시간, 동작) 형태의 튜플을 불러옴
    """
    fileloc = f"data/{fileName}.txt"    
    # 파일을 읽기 모드로 열기
    with open(fileloc, "r", encoding="utf-8") as file:
        action_str = file.readlines()
    
    print(f"파일 로드 성공: {fileloc}")
    return action_str


# 지금까지 저장된 파일이름을 리스트로 반환

def getSavedFileNames():
    """
    data 디렉토리에서 저장된 파일 이름 목록을 반환합니다.
    """
    # 데이터 디렉토리가 없으면 빈 리스트 반환
    if not os.path.exists(f"data"):
        return []

    # 디렉토리 내 모든 파일 이름 반환
    return [os.path.splitext(file)[0] for file in os.listdir(f"data") if file.endswith(".txt")]

#파일목록가져오기
