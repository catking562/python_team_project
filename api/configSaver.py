#파일 이름은 option.txt로 저장함!!!

def get(key):
    print("{key}값에 해당하는 데이터를 가져옴");

def put(key, value):
    print("{key}값에 해당하는 데이터를 {value}로 설정함");

def isKey(key):
    print("{key}값에 데이터가 있는지 확인");

def save():
    print("저장된 모든 {key:value} 데이터를 저장함");

def load():
    print("저장된 모든 데이터들을 불러옴");