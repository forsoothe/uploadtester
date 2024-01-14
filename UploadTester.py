import requests
import argparse
import io

previousExtensions = ["1.ada","2.ada","3dm","3ds","3g2","3gp","7z","a","aac","aaf","ada","adb","ads","ai","aiff","ape","apk","ar","asf","asm","au","avchd","avi","azw","azw1","azw3","azw4","azw6","bas","bash","bat","bin","bmp","bz2","c","c++","cab","cbl","cbr","cbz","cc","class","clj","cob","command","cpio","cpp","crx","cs","csh","css","csv","cxx","d","dds","deb","diff","dmg","doc","docx","drc","dwg","dxf","e","ebook","egg","el","eot","eps","epub","exe","f","f77","f90","fish","flac","flv","for","fth","ftn","gif","go","gpx","groovy","gsm","gz","h","hh","hpp","hs","htm","html","hxx","ics","iso","it","jar","java","jpeg","jpg","js","jsp","jsx","kml","kmz","ksh","kt","less","lha","lhs","lisp","log","lua","m","m2v","m3u","m4","m4a","m4p","m4v","mar","max","md","mid","mkv","mng","mobi","mod","mov","mp2","mp3","mp4","mpa","mpe","mpeg","mpg","mpv","msg","msi","mxf","nim","nsv","odp","slide","ods","odt","ogg","ogm","ogv","org","otf","pages","pak","patch","pdf","pea","php","pl","pls","png","po","pp","ppt","slide","ps","psd","py","qt","r","ra","rar","rb","rm","rmvb","roq","rpm","rs","rst","rtf","s","s3m","s7z","scala","scss","sh","shar","sid","srt","svg","svi","swg","swift","tar","tbz2","tex","tga","tgz","thm","tif","tiff","tlz","ttf","txt","v","vb","vcf","vcxproj","vob","war","wasm","wav","webm","webp","whl","wma","wmv","woff","woff2","wpd","wps","xcf","xcodeproj","xls","xlsx","xm","xml","xpi","xz","yuv","zip","zipx","zsh"]

specialChars = ["%20","%0a","%00","%0d%0a","/","\\","...","...."]

junkData = ["%00","\x00","%0a","%0d%0a","#","junk"]

contentType = ""

failedUpload = ['sorry', 'file was not uploaded']

magicNumbers = {'pcap': b"\xA1\xB2\x3C\x4D",
                'rpm': b"\xED\xAB\xEE\xDB",
                'sqlitedb': b"\x53\x51\x4C\x69\x74\x65\x20\x66\x6F\x72\x6D\x61\x74\x20\x33\x00",
                'ico': b"\x00\x00\x01\x00",
                'tar.z(LZH)': b"\x1F\xA0",
                'tar.z(LZW)': b"\x1F\x9D",
                'lzh(0)': b"\x2D\x68\x6C\x30\x2D",
                'lzh(5)': b"\x2D\x68\x6C\x3d\x2D",
                'bz2': b"\x42\x5A\x68",
                'gif(87a)': b"\x47\x49\x46\x38\x37\x61",
                'gif(89a)': b"\x47\x49\x46\x38\x39\x61",
                'tif': b"\x49\x49\x2A\x00",
                'tiff': b"\x4D\x4D\x00\x2A",
                'cr2': b"\x49\x49\x2A\x00\x10\x00\x00\x00\x43\x52",
                'cin': b"\x80\x2A\x5F\xD7",
                'bpg': b"\x42\x50\x47\xFB",
                'jpeg(1)': b"\xFF\xD8\xFF\xDB",
                'jpeg(2)': b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01",
                'jpeg(3)': b"\xFF\xD8\xFF\xEE",
                'jpg(1)': b"\xFF\xD8\xFF\xE0",
                'jpg2(2)': b"\xFF\x4F\xFF\x51",
                'exe(MZ)': b"\x4D\x5A",
                'jpg2(1)': b"\x00\x00\x00\x0C\x6A\x5020\x20\x0D\x0A\x87\x0A",
                'zip': b"\x50\x4B\x03\x04",
                'zip(Empty)': b"\x50\x4B\x05\x06",
                'zip(Spanned)': b"\x50\x4B\x05\x08",
                'rar(v1.5)': b"\x52\x61\x72\x21\x1A\x07\x00",
                'rar(v5.0)': b"\x52\x61\x72\x21\x1A\x07\x01\x00",
                'elf': b"\x7F\x45\x4C\x46",
                'png': b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A",
                'class': b"\xCA\xFE\xBA\xBE",
                'txt(UTF-8)': b"\xEF\xBB\xBF",
                'txt(UTF-16LE)': b"\xFF\xFE",
                'txt(UTF-16BE)': b"\xFF\xFF",
                'txt(UTF-32LE)': b"\xFF\xFE\x00\x00",
                'txt(UTF-32BE)': b"\x00\x00\xFE\xFF",
                'ps': b"\x25\x21\x50\x53",
                'pdf': b"\x25\x50\x44\x46\x2D",
                'oog': b"\x4F\x67\x67\x53",
                'mp3': b"\xFF\xFB",
                'bmp': b"\x42\x4D",
                'iso(ISO9660)': b"\x43\x44\x30\x30\x31",
                'flag': b"\x66\x4C\x61\x43",
                'midi': b"\x4D\x54\x68\x64",
                'doc': b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1",
                'dmg': b"\x6B\x6F\x6C\x79",
                'tar(1)': b"\x75\x73\x74\x61\x72\x00\x30\x30",
                'tar(2)': b"\x75\x73\x74\x61\x72\x20\x20\x00",
                '7z': b"\x37\x7A\xBC\xAF\x27\x1C",
                'tar.gz': b"\x1F\x8B",
                'pub': b"\x2D\x2D\x2D\x2D\x2D\x42\x45\x47\x49\x4E\x20\x53\x53\x48\x32\x20\x4B\x45\x59\x2D\x2D\x2D\x2D\x2D",
                'xml(1)': b"\x3C\x3F\x78\x6D\x6C\x20",
                'deb': b"\x21\x3C\x61\x72\x63\x68\x3E\x0A",
                'rtf': b"\x7B\x5C\x72\x74\x66\x31",
                'mpg(Transport Stream)': b"\x47",
                'mpg(Program Stream)': b"\x00\x00\x01\xBA",
                'mpg(Video)': b"\x00\x00\x01\xB3",
                'mp4(Video)': b"\x66\x74\x79\x70\x4D\x53\x4E\x56"
                }

parser = argparse.ArgumentParser(
                    prog='Upload Tester',
                    description='Upload Tester analyzes and probes file upload sites.',
                    epilog='Example: ./uploadTester www.10.10.10.10/upload.php')

def stringList(arg):
    return arg.split(',')

parser.add_argument('PARAMETER',help='Upload file parameter')
parser.add_argument('URL',help='URL of upload site (INCLUDE HTTP or HTTPS)')


parser.add_argument('-A',help='All Tests',required=False)
parser.add_argument('-S',help='Seperate Tests',required=False)

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

#TODO: Randomize file names
def createTestFile(uploadParameter,dataBytes,dataExtension):
    data = io.BytesIO(dataBytes)
    requestsFile = {uploadParameter:('test.'+dataExtension,data)}
    return requestsFile

#Capitlizes everything after first character:
def capitlizeExtensions(extensionList):
    for item in range(len(extensionList)):
        extensionList[item] = extensionList[item][:1:1]+extensionList[item][1::1].upper()
    return extensionList

#TODO: Change to append Special Characters
def appendNull(extensionList):
    for item in range(len(extensionList)):
        extensionList[item] = extensionList[item]+'%00'
    return extensionList

def breakFileNameLimit():
    print('todo')

#TODO: Make sure requests does actually upload file not just checking a . ok
def uploadTest(uploadURL, uploadFile={},uploadCookies={},uploadHeader={}):
    req = requests.post(uploadURL,files=uploadFile,cookies=uploadCookies,headers=uploadHeader)
    if req.ok:
            for item in failedUpload:
                if(req.text.lower().find(item) != -1):
                    #print("Upload Failed",uploadFile)
                    return False
                else:
                    print("Upload Success",uploadFile)
                    return True
    else:
        print("Upload Failed: " + req.raise_for_status())
        return False

if __name__ == '__main__':
    #Later if using custom extensions can input own list?
    print("URL",args.URL)
    print("PARAMETER",args.PARAMETER)
    
    testExtenstions = previousExtensions
    testURL = args.URL
    testParameter = args.PARAMETER
    userExtenstion = 'jpg'

    alltests=True
    #Scopes of work
    #All tests
    #Run seperated or mutated?
    if alltests:
        #Test Extenstions
        for item in capitlizeExtensions(testExtenstions):
            uploadTest(testURL,createTestFile(testParameter,b'test',item)) 
        #Test Null
        for item in appendNull(testExtenstions):
            uploadTest(testURL,createTestFile(testParameter,b'test',item))
        for item in magicNumbers.values():
            #For magic number need to get user input?
            uploadTest(testURL,createTestFile(testParameter,item,userExtenstion))
        print("TESTS DONE")

    #uploadTest("http://localhost/upload.php",createTestFile("fileToUpload"))
