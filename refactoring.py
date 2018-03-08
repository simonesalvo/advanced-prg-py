from urllib2 import Request, urlopen, URLError
import os
from datetime import datetime

url = "http://pages.di.unipi.it/corradini/Didattica/AP-17/PROG-ASS/03/ClassWithTest.java"
user_input = "testFiles/snip1.java" #raw_input("Enter the path of your file: ")
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
    justOnceCheck = 1
    snippetFile = open(user_input, 'r+')
    currentDateTime = datetime.now()
    javaFile = open("testResults/" + datetime.now().strftime("%Y%m%d%H%M%S") + ".java", "w+")

    refactoringClassLine = refactoringClassFile.readline()
    # Copying the snippet inside the class defined in the remote file
    while refactoringClassLine:
        print refactoringClassLine
        javaFile.write(refactoringClassLine)
        if justOnceCheck and refactoringClassLine.find("class") >= 0:
            if refactoringClassLine.find("{") >= 0:
                snippetLine = snippetFile.readline()
                justOnceCheck = 0
                while snippetLine:
                    javaFile.write(snippetLine)
                    snippetLine = snippetFile.readline()
                javaFile.write("\n")
                snippetFile.close()
        refactoringClassLine = refactoringClassFile.readline()
    refactoringClassFile.close()

    # Perform a refactoring of all the invocations of System.out.println with an argument

    javaFile.close()

    # Compile the refactored file;
