import os
import sys
import xml.etree.ElementTree as ET
import hashlib

dumpPath = "E:/PROJECTS/Basic Applications/Corruption Checker/hashes.xml"

def store(argv):
    f = open(argv[2], 'r')
    hash256 = hashlib.sha256((f.read()).encode()).hexdigest();
    print(hash256)

    if os.path.isfile(dumpPath) == False:
        data = ET.Element('data', {})
        data.text = ""
        fo = open(dumpPath, 'wb')
        fo.write(ET.tostring(data))
        fo.close()
    
    data = ET.parse(dumpPath)
    root = data.getroot()

    for ele in root.findall('File'):
        if ele.get('Path') == argv[2]:
            ele.set('Hash', hash256)
            data.write(dumpPath)
            return

    FileItem = ET.SubElement(root, 'File')
    FileItem.set('Path', argv[2])
    HashItem = ET.SubElement(FileItem, 'Hash')
    HashItem.text = hash256
    data.write(dumpPath)

def check(argv):
    if os.path.isfile(argv[2]) == False:
        print("No such file exists")
        return

    tree = ET.parse(dumpPath)
    root = tree.getroot()

    flag = False
    for ele in root.findall('File'):
        if ele.get('Path') == argv[2]:
            flag = True
            f = open(argv[2], 'r')
            hash256 = hashlib.sha256((f.read()).encode()).hexdigest();

            if hash256 == ele.find('Hash').text:
                print("Hashes match. File is not corrupted.")
            else:
                print("File is corrupted.")
            return

    if flag == False:
        print("Hash not found")
        return
    
def helpText():
    print("\n**************************************\n")
    print("Welcome to Corruption Checker")
    print("The List of commands are:")
    print("\tstore  -To store the hash of a file")
    print("\tcheck  -To check if the file is corrupted")
    print("\tfile  -To specify that the command should run on a file")
    print('Example: cptchk store file "<Path to the file>"')
    print("\n**************************************\n")

def main(argv):
    if len(argv) == 0:
        helpText()
    elif argv[0] == 'store':
        store(argv)
    elif argv[0] == 'check':
        check(argv)
    else:
        helpText()

if __name__ == "__main__":
    main(sys.argv[1:])