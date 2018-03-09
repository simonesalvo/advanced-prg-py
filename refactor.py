import os
import re
import sys
from datetime import datetime
from subprocess import Popen, PIPE
from urllib2 import Request, urlopen, URLError

print "Python version: " + sys.version

methodNameRegex = r"(\w*)[(]"
substitutionRegex = r"(System.out.println\()((\w*\s*\S*\W*)*)(\);)"
givenClassNameRegex = r"(\w*)(.)(java)"

snippetMethodName = ""

url = raw_input('enter a valid URL ')
user_input = raw_input("Enter the path of your file: ")
assert os.path.exists(user_input), "I did not find the file at, " + str(user_input)

req = Request(url)
try:
    refactoringClassFile = urlopen(req)
except URLError, e:
    if hasattr(e, 'reason'):
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    elif hasattr(e, 'code'):
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
else:
    matches = re.search(givenClassNameRegex, url)
    givenClassName = matches.group(1)
    justOnceCheck = 1
    snippetFile = open(user_input, 'r+')
    currentDateTime = datetime.now()
    javaFileName = "testResults/" + givenClassName + ".java"
    javaFile = open(javaFileName, "w+")

    refactoringClassLine = refactoringClassFile.readline()
    # Copying the snippet inside the class defined in the remote file
    while refactoringClassLine:
        javaFile.write(refactoringClassLine)
        if justOnceCheck and refactoringClassLine.find("class") >= 0:
            if refactoringClassLine.find("{") >= 0:
                snippetLine = snippetFile.readline()
                justOnceCheck = 0
                if not snippetMethodName:
                    matches = re.search(methodNameRegex, snippetLine)
                    snippetMethodName = matches.group(1)
                while snippetLine:
                    javaFile.write(snippetLine)
                    snippetLine = snippetFile.readline()
                javaFile.write("\n")
                snippetFile.close()
        if refactoringClassLine.find("System.out.println("):
            matches = re.search(substitutionRegex, refactoringClassLine)
            if matches:
                refactoredLine = matches.group(1) + snippetMethodName + "(" + matches.group(2) + ")" + matches.group(4)
                javaFile.write(refactoredLine)

        refactoringClassLine = refactoringClassFile.readline()
    refactoringClassFile.close()
    javaFile.close()

    # Compile the refactored file and manage errors;
    cmd = '/usr/bin/javac ' + javaFileName
    proc = Popen(cmd, shell=True, stdout=PIPE)

    out, err = proc.communicate()

    if err is None and not out:
        cmd = '/usr/bin/java -cp ' + "testResults " + givenClassName
        proc = Popen(cmd, shell=True, stdout=PIPE)
        out, err = proc.communicate()
        if err is None:
            runningOutputFile = open("testResults/OUTPUT.txt", "w+")
            runningOutputFile.write(out)
            runningOutputFile.close()
        else:
            runningErrorOutputFile = open("testResults/ERROR.txt", "w+")
            runningErrorOutputFile.write(out)
            runningErrorOutputFile.close()
    else:
        print "Error on compiling \n"
        compilingErrorOutputFile = open("testResults/COMP_ERR.txt", "w+")
        compilingErrorOutputFile.write(out)
        compilingErrorOutputFile.close()
