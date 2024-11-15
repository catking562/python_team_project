def saveFile(dictionary, fileName):
    fileloc = "data\\" + fileName + ".txt";
    #fileloc에 dictionary데이터를 저장
    return True;

def loadFile(fileName):
    fileloc = "data\\" + fileName + ".txt";
    dictionary = {};
    #fileloc에 있는 데이터 dictionary로 저장
    return dictionary;