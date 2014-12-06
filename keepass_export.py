#from xml.dom import minidom
import xml.etree.ElementTree as ET
import re
import sys
from subprocess import Popen, PIPE, STDOUT
import subprocess

def dump(obj):
    '''return a printable representation of an object for debugging'''
    newobj=obj
    if '__dict__' in dir(obj):
        newobj=obj.__dict__
        if ' object at ' in str(obj) and not newobj.has_key('__type__'):
            newobj['__type__']=str(obj)
        for attr in newobj:
            newobj[attr]=dump(newobj[attr])
    return newobj



tree = ET.parse(sys.argv[1])
root = tree.getroot().find("Root")
pattern = re.compile(ur' ')
subst = u"-"

def recurse_entry(entry, groupName, nbEntry):
    strings = entry.findall("String")
    password = ""
    entryName = groupName + ""
    history = entry.find("History")
    for s in strings:
        title = s.find("Key")
        val = s.find("Value")
        if title.text == "Title" and nbEntry == 1:
            entryName = re.sub(pattern, subst, entryName + "." + val.text)
            print("\t"+entryName)
        if title is not None and val is not None and title.text is not None and title.text != "Title" and val.text is not None:
            password = password + title.text + " : " + val.text + "\n"
        if title.text == "Notes":
            password = password + "\n\n"
    if history is not None and len(history.findall("Entry")) > 0:
        print("nbHistory of "+entryName+" : "+str(len(history.findall("Entry"))))
        print("HISTORY")
        for previous_entrys in history.findall("Entry"):
            nbEntry = nbEntry+1
            recurse_entry(previous_entrys, entryName, nbEntry)
        nbEntry = nbEntry + 1
    subprocess.call("mkdir /tmp/aurorePasswords/"+entryName, shell=True)
    print("CREATING "+entryName+str(nbEntry))
    p = Popen("cat > /tmp/aurorePasswords/"+entryName+"/"+str(nbEntry), stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
#            ~/bin/aurorepasswords --roles aurore -f -e "+entryName.encode("utf-8"), stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
    sortie_aurore = p.communicate(input=password.encode("utf-8"))[0]
    #print(sortie_aurore.decode("utf-8"))

def recurse_groups(element, grpname):
    groups = element.findall("Group")
    for child in groups:
        groupName = child.find("Name").text
        if groupName is None or groupName == "KeePass" or groupName == "KeepPass":
            groupName = ""
        bla = grpname
        if bla != "":
            bla = bla + "."
        groupName = bla + groupName
#        print("\n\n\n"+groupName)
        groupName = re.sub(pattern, subst, groupName)
        print(groupName)
        entries = child.findall("Entry")
        for entry in entries:
            recurse_entry(entry, groupName, 1)
        recurse_groups(child, groupName)

recurse_groups(root, "")

#xmldoc = minidom.parse('testKeepassExport.xml')
#itemlist = xmldoc.getElementsByTagName('Group') 
#print len(itemlist)
#for s in itemlist :
#    if len(s.getElementsByTagName('Name')) > 0 and s.getElementsByTagName('Name')[0].firstChild is not None:
#        print(s.getElementsByTagName('Name')[0].firstChild.nodeValue)
#        print(len(s.getElementsByTagName('Entry')))
#        print("\n")
