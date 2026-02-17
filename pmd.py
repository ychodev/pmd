# Written by Yongjoo Cho
# Last modified 2/17/2026

# 2/17/26 '이', '가', '나', '이나'로 끝날 때 처리 코드 추가
# 2/16/26 번호 앞뒤로 [] 추가
# 2/16/26 을/를 처리 코드 추가.
# 9/19/23 코드의 \\@linenum이 > 뒤에 나올 때 처리 가능
# 9/29/23 같은 줄에 \@ref()가 두 개 이상 나올 때 처리 가능

# 7/3/23 Chapter 또는 chapter tag 사용 가능

# 실행 결과 처리 추가

import re
import sys

CHAPTER_REGEXP=r"(?<=\@label\([c|C]hapter:)(\s[0-9]+)(?=\))"
#영문/한글/숫자 캡션 가능
LABEL_FIGURE_REGEXP      = "(\\\\@label\\(fig:)(\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*)(\\))"
LABEL_TABLE_REGEXP       = "(\\\\@label\\(table:)(\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*)(\\))"
LABEL_CODE_REGEXP        = "(\\\\@label\\(code:)(\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*)(\\))"
LABEL_RESULT_REGEXP      = "(\\\\@label\\(result:)(\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*)(\\))"
REF_FIGURE_REGEXP        = "(\\\\@ref\\(fig:)(\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*)(\\))"
REF_TABLE_REGEXP         = "(\\\\@ref\\(table:)(\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*)(\\))"
REF_CODE_REGEXP          = "(\\\\@ref\\(code:)(\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*)(\\))"
REF_RESULT_REGEXP          = "(\\\\@ref\\(result:)(\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*)(\\))"
REPL_LABEL_FIGURE_REGEXP = "\\\\@label\\(fig:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
REPL_LABEL_TABLE_REGEXP  = "\\\\@label\\(table:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
REPL_LABEL_CODE_REGEXP   = "\\\\@label\\(code:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
REPL_LABEL_RESULT_REGEXP   = "\\\\@label\\(result:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
#REPL_REF_FIGURE_REGEXP   = "\\\\@ref\\(fig:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
#REPL_REF_TABLE_REGEXP    = "\\\\@ref\\(table:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
#REPL_REF_CODE_REGEXP     = "\\\\@ref\\(code:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
#REPL_REF_RESULT_REGEXP     = "\\\\@ref\\(result:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
REPL_REF_FIGURE_REGEXP   = "\\\\@ref\\(fig:\\s*#####\\s*\\)"
REPL_REF_TABLE_REGEXP    = "\\\\@ref\\(table:\\s*#####\\s*\\)"
REPL_REF_CODE_REGEXP     = "\\\\@ref\\(code:\\s*#####\\s*\\)"
REPL_REF_RESULT_REGEXP     = "\\\\@ref\\(result:\\s*#####\\s*\\)"
TEXT_BOX_CODE_REGEXP     = r">\s*```"
TEXT_BOX_CODE_LINE_NUM_REGEXP     = r"[>\s]*```[a-zA-Z_0-9가-핳\s]*\\\\@linenum\s*"
TEXT_BOX_CODE_NO_LINE_NUM_REGEXP     = r"[>\s]*```[a-zA-Z_0-9가-핳\s]*\\\\@nolinenum\s*"
CODE_REGEXP              = r"```"
CODE_LINE_NUM_REGEXP     = r"```[a-zA-Z_0-9가-핳\s]*\\\\@linenum\s*"
CODE_NO_LINE_NUM_REGEXP  = r"```[a-zA-Z_0-9가-핳\s]*\\\\@nolinenum\s*"

class Label:
    def __init__(self, name, replStr, regExp, replRegExp, refRegExp, replRefRegExp):
        self.regExp = regExp
        self.replRegExp = replRegExp
        self.refRegExp = refRegExp
        self.replRefRegExp = replRefRegExp
        self.counter = 1
        self.name = name
        self.replStr = replStr
        self.labels = {}

    def increaseCounter(self):
        self.counter += 1

    def getCounter(self):
        return self.counter

    def getName(self):
        return self.name

    def getReplStr(self):
        return self.replStr

    def getRegExp(self):
        return self.regExp

    def getReplRegExp(self):
        return self.replRegExp

    def getRefRegExp(self):
        return self.refRegExp

    def getReplRefRegExp(self):
        return self.replRefRegExp

    def isInKeys(self, s):
        return s in self.labels.keys()

    def addValue(self, key, s):
        self.labels[key] = s

    def getValue(self, key):
        return self.labels[key]

# 캡션으로 공백 아닌 모든 문자 포함 가능
#LABEL_FIGURE_REGEXP = r"(?<=\@label\(fig:)(\s*\S*\s*)(?=\))"
#LABEL_TABLE_REGEXP=r"(?<=\@label\(table:)(\s*\S\s*)(?=\))"
#LABEL_CODE_REGEXP=r"(?<=\@label\(code:)(\s*\S*\s*)(?=\))"
#REF_FIGURE_REGEXP = r"(?<=\@ref\(fig:)(\s*\S*\s*)(?=\))"
#REF_TABLE_REGEXP=r"(?<=\@ref\(table:)(\s*\S\s*)(?=\))"
#REF_CODE_REGEXP=r"(?<=\@ref\(code:)(\s*\S\s*)(?=\))"

#s = """\@label(chapter: 8)
#![\@label(fig:_img_execution89_87_a    ) 고급 프로그래밍 언어로 작성한 프로그램을 실행하는 방법](figures/01/Execution.png)
#![\@label(fig: _img_execution89_87_a2   ) 이미지 2](figures/02/E.png)
#\@label(code:_code1)
#```
#print(123)
#```
#\@label(table: 표 캡션 1)
#| a | b | c |
#| --- | --- | --- |
#| ab | abc | abcd |
#| bc | bcd | bcd |
#
#blah blah blah
#"""

sectionNumber = 1

def findChapterNum(line):
    chap = re.search(CHAPTER_REGEXP, line)
    if chap:
        chapterNumStr = chap.group().strip() + "-"
    else:
        chapterNumStr = ""
    return chapterNumStr

def correctPostposition(line, subStr):
    eunList = [ '0', '1', '3', '6', '7', '8' ]
    neunList = [ '2', '4', '5', '9' ]
    print(subStr, line)
    postposition = subStr[-1]  # 마지막 숫자를 확인
    replSubStr = "\\[" + subStr + "\\]"
    newSubStr = "[" + subStr + "]"
    if postposition in eunList:
        line = re.sub(replSubStr + "\\s*는", newSubStr + "은", line)
        line = re.sub(replSubStr + "\\s*은", newSubStr + "은", line)  # 공백 제거
        line = re.sub(replSubStr + "\\s*와", newSubStr + "과", line)
        line = re.sub(replSubStr + "\\s*과", newSubStr + "과", line)  # 공백 제거
        line = re.sub(replSubStr + "\\s*를", newSubStr + "을", line)
        line = re.sub(replSubStr + "\\s*을", newSubStr + "을", line)  # 공백 제거
        line = re.sub(replSubStr + "\\s*가", newSubStr + "이", line)
        line = re.sub(replSubStr + "\\s*이", newSubStr + "이", line)  # 공백 제거
        line = re.sub(replSubStr + "\\s*나", newSubStr + "이나", line)
        line = re.sub(replSubStr + "\\s*이나", newSubStr + "이나", line)  # 공백 제거
    elif postposition in neunList:
        line = re.sub(replSubStr + "\\s*은", newSubStr + "는", line)
        line = re.sub(replSubStr + "\\s*는", newSubStr + "는", line)  # 공백 제거
        line = re.sub(replSubStr + "\\s*과", newSubStr + "와", line)
        line = re.sub(replSubStr + "\\s*와", newSubStr + "와", line)  # 공백 제거
        line = re.sub(replSubStr + "\\s*을", newSubStr + "를", line)
        line = re.sub(replSubStr + "\\s*를", newSubStr + "를", line)  # 공백 제거
        line = re.sub(replSubStr + "\\s*이", newSubStr + "가", line)
        line = re.sub(replSubStr + "\\s*가", newSubStr + "가", line)  # 공백 제거
        line = re.sub(replSubStr + "\\s*이나", newSubStr + "나", line)
        line = re.sub(replSubStr + "\\s*가", newSubStr + "가", line)  # 공백 제거
    return line

def replaceReferences(line, lineNum, chapterNumStr, label): #labels, labelName, regexp, replRegExp):
    matchedIterator = re.findall(label.getRefRegExp(), line)
    for m in matchedIterator:
        m = m[1].strip()
        if m and label.isInKeys(m):
            subStr = label.getValue(m)
            
#            print("VALUE: " + label.getValue())
#"\\\\@ref\\(code:\\s*" + m + "\\s*\\)", subStr, line) 
            refRegExp = label.getReplRefRegExp()
            refRegExp = refRegExp.replace("#####", m)
            newSubStr = '[' + subStr + ']'
            line = re.sub(refRegExp, newSubStr, line)
#            print(line)
            replSubStr = "\\[" + subStr + "\\]"
            matchedIterator = True
            postpositionList = [ "\\s*는", "\\s*은", "\\s*와", "\\s*과", "\\s*을", "\\s*를", "\\s*가", "\\s*이", "\\s*나", "\\s*이나" ]
            for postposition in postpositionList:
                matchedIterator = matchedIterator or re.findall(replSubStr + postposition, line)
                if matchedIterator == False:
                    break
            if matchedIterator:
                line = correctPostposition(line, subStr)
        else:
            print(f"Error:{lineNum}:{m} is not in labels")
    return line

def addLabels(line, lineNum, chapterNumStr, label): #labels, labelName, counter, replStr, regexp, replRegExp):
    matchedIterator = re.findall(label.getRegExp(), line)
    for m in matchedIterator:
#        print(m)
        m = m[1].strip()
        if m and label.isInKeys(m):
            print(f"Error:{lineNum}:duplicate {label.getName()} label:{m}")
        else:
            subStr = label.getReplStr() + chapterNumStr + str(label.getCounter()) 
            label.addValue(m, subStr)
            label.increaseCounter()
            line = re.sub(label.getReplRegExp(), '[' + subStr + ']', line)
    return line

def readFile(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return lines
    except FileNotFoundError:
        print(f"File \"{filename}\" does not exist.")
    except UnicodeDecodeError:
        print(f"File \"{filename}\" is saved with non-UTF-8 encoding")
    return None

def createLabelList():
    lst = list()
    lst.append(Label("figure", "그림 ", LABEL_FIGURE_REGEXP, REPL_LABEL_FIGURE_REGEXP,
                     REF_FIGURE_REGEXP, REPL_REF_FIGURE_REGEXP))
    lst.append(Label("table", "표 ", LABEL_TABLE_REGEXP, REPL_LABEL_TABLE_REGEXP,
                     REF_TABLE_REGEXP, REPL_REF_TABLE_REGEXP))
    lst.append(Label("code", "코드 ", LABEL_CODE_REGEXP, REPL_LABEL_CODE_REGEXP,
                     REF_CODE_REGEXP, REPL_REF_CODE_REGEXP))
    lst.append(Label("result", "실행 결과 ", LABEL_RESULT_REGEXP, REPL_LABEL_RESULT_REGEXP,
                     REF_RESULT_REGEXP, REPL_REF_RESULT_REGEXP))
    return lst

def processAddLabels(lines, chapterNumStr, labelList):
    for i in range(1, len(lines)):
        for label in labelList:
            line = addLabels(lines[i], i + 1, chapterNumStr, label)
            if line != lines[i]:
                lines[i] = line;

def processReplaceReferences(lines, chapterNumStr, labelList):
    for i in range(1, len(lines)):
        for label in labelList:
            line = replaceReferences(lines[i], i + 1, chapterNumStr, label)
            if line != lines[i]:
                lines[i] = line

def countLines(lines, startLineIdx):
    count = 0
    while startLineIdx < len(lines):
        line = lines[startLineIdx].strip()
        if line == "```":
            break
        count += 1
        startLineIdx += 1
    return count

def countLinesInTextBox(lines, startLineIdx):
    count = 0
    while startLineIdx < len(lines):
        line = lines[startLineIdx].strip()
        m = re.match(TEXT_BOX_CODE_REGEXP, line)
        #if line == "> ```":
        if m:
            break
        count += 1
        startLineIdx += 1
    return count

def getNumLength(n):
    count = 1
    while n // 10 > 0:
        count = count + 1
        n = n // 10
    return count

def insertLineNumbers(lines, startLineIdx, numLines):
    numLen = getNumLength(numLines)
    fmt = "{:0" + str(numLen) + "d}"
    count = 1
    for i in range(startLineIdx, startLineIdx + numLines):
        f = fmt.format(count)
        lines[i] = f + "    " + lines[i]
        count += 1

def insertLineNumbersInTextBox(lines, startLineIdx, numLines):
    numLen = getNumLength(numLines)
    fmt = "{:0" + str(numLen) + "d}"
    count = 1
    for i in range(startLineIdx, startLineIdx + numLines):
        f = fmt.format(count)
        idx = lines[i].find("> ")
        lines[i] = lines[i][idx:2] + f + "    " + lines[i][idx + 2:]
#        lines[i] = f + "    " + lines[i]
        count += 1

def processAddLineNumsInCode(lines):
    codeOpen = False
    for i in range(1, len(lines)):
        line = lines[i].strip()
        if codeOpen == True and line == "```":
            lines[i] = line + "\n"
            codeOpen = False
        else: 
            m = re.match(CODE_NO_LINE_NUM_REGEXP, line)
            m2 = re.match(CODE_LINE_NUM_REGEXP, line)
            if m == None:
                if (m2 or (m2 == None and line == "```")):
                    codeOpen = True
                    lines[i] = "```\n"
                    numLines = countLines(lines, i + 1)
                    insertLineNumbers(lines, i + 1, numLines)

def processAddLineNumsInTextBoxCode(lines):
    for i in range(1, len(lines)):
        line = lines[i].strip()
        m = re.match(TEXT_BOX_CODE_NO_LINE_NUM_REGEXP, line)
        if m:
            lines[i] = line[:line.find("\\\\@nolinenum")] + "\n"
        m2 = re.match(TEXT_BOX_CODE_LINE_NUM_REGEXP, line)
        #m3 = re.match(TEXT_BOX_CODE_REGEXP, line)        
        if m2:
            lines[i] = line[:line.find("\\\\@linenum")] + "\n"               
            numLines = countLinesInTextBox(lines, i + 1)
            print(f"i + 1: {i + 1}, numLines: {numLines}")
            insertLineNumbersInTextBox(lines, i + 1, numLines)

def writeNewFile(filename, lines, startFromFirstLine):
    if startFromFirstLine:
        start = 0
    else:
        start = 1
    with open(filename, "w", encoding="utf-8") as wf:
        for i in range(start, len(lines)):
            wf.write(lines[i])

def addChapterAndSectionNumber(lines, chapterNumStr):
    global sectionNumber

    inCodeSection = False  # 코드 영역 안에 있는지 확인하기 위함

    for i in range(len(lines)):
        line = lines[i]
        line = line.strip()
        if line.count("```") % 2 == 1:
            inCodeSection = not inCodeSection
        if inCodeSection == False:
            if "## " in line and line.index("## ") == 0:
                print(line)
                line = line[:3] + chapterNumStr[:-1] + "." + str(sectionNumber) + " " + line[3:]
                lines[i] = line
                sectionNumber += 1
            elif "# " in line and line.index("# ") == 0:
                line = line.strip()
                line = line[:2] + chapterNumStr[:-1] + ". " + line[2:]
                lines[i] = line

if __name__ == "__main__":
    newFileName = ""
    if len(sys.argv) < 2:
        print("Usage: python pmd.py original_file [new_file]")
        print("If [new file] is omitted, \"preprocessed_\" will be prefixed to the original file name.")
        exit()
    elif len(sys.argv) < 3:
        newFileName = "preprocessed_" + sys.argv[1]
    else:
        newFileName = sys.argv[2]

    lines = readFile(sys.argv[1])
#    lines = readFile("temp.md")
    chapterNumStr = findChapterNum(lines[0])
    addChapterAndSectionNumber(lines, chapterNumStr)
    labelList = createLabelList()
    processAddLabels(lines, chapterNumStr, labelList)
    processReplaceReferences(lines, chapterNumStr, labelList)
    processAddLineNumsInCode(lines)
    processAddLineNumsInTextBoxCode(lines)
    writeNewFile(newFileName, lines, chapterNumStr == "")
