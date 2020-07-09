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


    # item = ET.SubElement(data, 'File')
    # pathF = ET.SubElement(item, 'Path')
    # hashF = ET.SubElement(item, 'Hash')
    # pathF.text = argv[2]
    # hashF.text = hash256
    # f = open(dumpPath, 'wb')
    # f.write(ET.tostring(data))
    

def main(argv):
    if argv[0] == 'store':
        store(argv)
    elif argv[0] == 'check':
        check(argv)

if __name__ == "__main__":
    main(sys.argv[1:])