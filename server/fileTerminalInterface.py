from os import walk


def getFilesArray(path):
    f = []

    for (dirpath, dirname, filenames) in walk(path):
        f.extend(filenames)
        break

    return f

class FileInterface:
    def __init__(self) -> None:
        self.files = getFilesArray('./files')
    
    def getFileAdress (self, fileName):

        if fileName not in self.files:
            return f"{fileName} não existe no nosso banco de dados"
        
        return f"./files/{fileName}"
    
    def showFilesNames (self):

        string = f"<DATA>"
        
        for e in self.files:
            string = string + (f"{e}<DATA>")

        return string


