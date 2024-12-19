import os


#Runner에서 동작할 수 있는 데이터를 메모장 파일에 저장하는 함수
#메인의 gui를 통하여 입력받은 파일 이름으로 data 폴더에 저장한다.
#이때, control은 DataEncoder를 통해 문자열 형태로 가공됨.
def saveFile(control, fileName):
    #'data/'를 통하여 메모장 파일을 data 폴더에 저장.
    fileloc = f"data/{fileName}.txt"
    # 파일을 쓰기 모드로 열기
    # 문자열인 control을 저장
    with open(fileloc, "w", encoding="utf-8") as file:
        file.write(control)

    print(f"파일 저장 성공: {fileloc}")
    return True

#파일에서 문자열 형태로 저장된 데이터을 읽어오는 함수
#파일 이름은 메인 함수에서 받아온다.
def loadFile(fileName):
    fileloc = f"data/{fileName}.txt"    
    # 파일을 읽기 모드로 열기
    with open(fileloc, "r", encoding="utf-8") as file:
        action_str = file.readline()
    
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
    # os.listdir(파일 이름)으로 [ 
    return [os.path.splitext(file)[0] for file in os.listdir(f"data") if file.endswith(".txt")]

#파일목록가져오기
