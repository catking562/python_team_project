import os

def saveFile(tup, fileName):
    """
    튜플 데이터를 지정된 파일에 저장합니다.
    (시간, 동작) 형태의 튜플을 저장
    """
    fileloc = f"data/{fileName}.txt"
    # 파일을 쓰기 모드로 열기
    with open(fileloc, "w", encoding="utf-8") as file:
        for item in tup:
            # 시간과 동작을 저장
            time = item[0]
            action = item[1]
            
            # 각 동작에 따른 튜플 내용 저장
            if action == "click":
                x, y, button, pressed = item[2], item[3], item[4], item[5]
                file.write(f"{time}:{action}:{x}:{y}:{button}:{pressed}\n")
            elif action == "scroll":
                x, y, dx, dy = item[2], item[3], item[4], item[5]
                file.write(f"{time}:{action}:{x}:{y}:{dx}:{dy}\n")
            elif action == "press" or action == "release":
                key = item[2]
                file.write(f"{time}:{action}:{key}\n")
    
    print(f"파일 저장 성공: {fileloc}")
    return True

def loadFile(fileName):
    """
    지정된 파일에서 튜플 데이터를 불러옵니다.
    (시간, 동작) 형태의 튜플을 불러옴
    """
    fileloc = f"data/{fileName}.txt"    
    tup = []
    # 파일을 읽기 모드로 열기
    with open(fileloc, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(":")
            time = float(parts[0])
            action = parts[1]
            
            # 각 동작에 따라 튜플을 다르게 파싱
            if action == "click":
                x, y, button, pressed = int(parts[2]), int(parts[3]), parts[4], bool(int(parts[5]))
                tup.append((time, action, x, y, button, pressed))
            elif action == "scroll":
                x, y, dx, dy = int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5])
                tup.append((time, action, x, y, dx, dy))
            elif action == "press" or action == "release":
                key = parts[2]
                tup.append((time, action, key))
    
    print(f"파일 로드 성공: {fileloc}")
    return tup


# 지금까지 저장된 파일이름을 리스트로 반환

def getSavedFileNames():
    """
    data 디렉토리에서 저장된 파일 이름 목록을 반환합니다.
    """
    # 데이터 디렉토리가 없으면 빈 리스트 반환
    if not os.path.exists(DATA_DIR):
        return []

    # 디렉토리 내 모든 파일 이름 반환
    return [os.path.splitext(file)[0] for file in os.listdir(DATA_DIR) if file.endswith(".txt")]

#파일목록가져오기
