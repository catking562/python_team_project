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
            # 튜플 (시간, 동작)을 파일에 기록
            file.write(f"{item[0]}:{item[1]}\n")
    
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
            if ":" in line:
                delay, action = line.strip().split(":", 1)
                # 튜플 (시간, 동작)으로 변환하여 리스트에 저장
                tup.append((float(delay), action))
    
    print(f"파일 로드 성공: {fileloc}")
    return tup
