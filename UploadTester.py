import requests
import argparse
import io
from random import choice

previousExtensions = ["1.ada","2.ada","3dm","3ds","3g2","3gp","7z","a","aac","aaf","ada","adb","ads","ai","aiff","ape","apk","ar","asf","asm","au","avchd","avi","azw","azw1","azw3","azw4","azw6","bas","bash","bat","bin","bmp","bz2","c","c++","cab","cbl","cbr","cbz","cc","class","clj","cob","command","cpio","cpp","crx","cs","csh","css","csv","cxx","d","dds","deb","diff","dmg","doc","docx","drc","dwg","dxf","e","ebook","egg","el","eot","eps","epub","exe","f","f77","f90","fish","flac","flv","for","fth","ftn","gif","go","gpx","groovy","gsm","gz","h","hh","hpp","hs","htm","html","hxx","ics","iso","it","jar","java","jpeg","jpg","js","jsp","jsx","kml","kmz","ksh","kt","less","lha","lhs","lisp","log","lua","m","m2v","m3u","m4","m4a","m4p","m4v","mar","max","md","mid","mkv","mng","mobi","mod","mov","mp2","mp3","mp4","mpa","mpe","mpeg","mpg","mpv","msg","msi","mxf","nim","nsv","odp","slide","ods","odt","ogg","ogm","ogv","org","otf","pages","pak","patch","pdf","pea","php","pl","pls","png","po","pp","ppt","slide","ps","psd","py","qt","r","ra","rar","rb","rm","rmvb","roq","rpm","rs","rst","rtf","s","s3m","s7z","scala","scss","sh","shar","sid","srt","svg","svi","swg","swift","tar","tbz2","tex","tga","tgz","thm","tif","tiff","tlz","ttf","txt","v","vb","vcf","vcxproj","vob","war","wasm","wav","webm","webp","whl","wma","wmv","woff","woff2","wpd","wps","xcf","xcodeproj","xls","xlsx","xm","xml","xpi","xz","yuv","zip","zipx","zsh"]

specialChars = ["%20","%0a","%00","%0d%0a","/","\\","...","...."]

junkData = ["%00","\x00","%0a","%0d%0a","#","junk"]

contentType = ""

magicNumbers = ""

parser = argparse.ArgumentParser(
                    prog='Upload Tester',
                    description='Upload Tester analyzes and probes file upload sites.',
                    epilog='Example: ./uploadTester www.10.10.10.10/upload.php')


def stringList(arg):
    return arg.split(',')

parser.add_argument('URL',help='URL of upload site')
parser.add_argument('-x','--extension',help='File Extension',required=False)
parser.add_argument('-H','--header',help='Header and Values',required=False,type=stringList)
parser.add_argument('-C','--cookie',help='Cookie and Value',required=False,type=stringList)
parser.add_argument('-v','--verbose',required=False)
args = parser.parse_args()

def convertToDict(inputList):
    dictReturn = {}
    for item in inputList:
        if len(item.split(':')) != 2:
            return False
        else:
            key,value = item.split(':')
            dictReturn[key] = value
    return dictReturn

def createTestFile(uploadParameter):
    data = io.BytesIO(b"some test data: \x00\x01")
    requestsFile = {uploadParameter:('test.jpg',data)}
    return requestsFile

#Capitlize everything after first character:
def capitlizeExtensions(extensionList):
    for item in range(len(extensionList)):
        extensionList[item] = extensionList[item][:1:1]+extensionList[item][1::1].upper()
    return extensionList

def appendNull(extensionList):
    for item in range(len(extensionList)):
        extensionList[item] = extensionList[item]+'%00'
    return extensionList

def breakFileNameLimit():
    print('todo')



def uploadTest(uploadURL, uploadFile={},uploadCookies={},uploadHeader={}):
    req = requests.post(uploadURL,files=uploadFile,cookies=uploadCookies,headers=uploadHeader)
    if req.ok:
        print("Upload Success")
        return True
    else:
        print("Upload Failed: " + req.raise_for_status())
        return False

if __name__ == '__main__':
    uploadTest("http://localhost/upload.php",createTestFile("fileToUpload"))
