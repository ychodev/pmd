# Written by Yongjoo Cho
# Last modified 2/23/2023

# 실행 결과 처리 추가
#

import re
import sys

CHAPTER_REGEXP=r"(?<=\@label\(chapter:)(\s[0-9]+)(?=\))"
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
REPL_REF_FIGURE_REGEXP   = "\\\\@ref\\(fig:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
REPL_REF_TABLE_REGEXP    = "\\\\@ref\\(table:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
REPL_REF_CODE_REGEXP     = "\\\\@ref\\(code:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
REPL_REF_RESULT_REGEXP     = "\\\\@ref\\(result:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
CODE_LINE_NUM_REGEXP     = r"\s*```[a-zA-Z_0-9가-핳\s]*\\\\@linenum\s*"

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

s = """\@label(chapter: 8)
![\@label(fig:_img_execution89_87_a    ) 고급 프로그래밍 언어로 작성한 프로그램을 실행하는 방법](figures/01/Execution.png)
![\@label(fig: _img_execution89_87_a2   ) 이미지 2](figures/02/E.png)
\@label(code:_code1)
```
print(123)
```
\@label(table: 표 캡션 1)
| a | b | c |
| --- | --- | --- |
| ab | abc | abcd |
| bc | bcd | bcd |

blah blah blah
"""

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
    postposition = subStr[-1]
    if postposition in eunList:
        line = re.sub(subStr + "\\s*는", subStr + "은", line)
        line = re.sub(subStr + "\\s*은", subStr + "은", line)  # 공백 제거
    elif postposition in neunList:
        line = re.sub(subStr + "\\s*은", subStr + "는", line)
        line = re.sub(subStr + "\\s*는", subStr + "는", line)  # 공백 제거
    return line

def replaceReferences(line, lineNum, chapterNumStr, label): #labels, labelName, regexp, replRegExp):
    matchedIterator = re.findall(label.getRefRegExp(), line)
    for m in matchedIterator:
        m = m[1].strip()
        if m and label.isInKeys(m):
            subStr = label.getValue(m)
            line = re.sub(label.getReplRefRegExp(), subStr, line)
            matchedIterator = re.findall(subStr + "\\s*는", line)
            matchedIterator2 = re.findall(subStr + "\\s*은", line)
            if matchedIterator:
                line = correctPostposition(line, subStr)
            elif matchedIterator2:
                line = correctPostposition(line, subStr)
        else:
            print(f"Error:{lineNum}:{m} is not in {labelName} labels")
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
            line = re.sub(label.getReplRegExp(), subStr, line)
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

def processAddLineNumsInCode(lines):
    for i in range(1, len(lines)):
        line = lines[i].strip()
        m = re.match(CODE_LINE_NUM_REGEXP, line)
        if m:
            lines[i] = line[:line.index("\\@linenum")] + "\n"
            numLines = countLines(lines, i + 1)
            insertLineNumbers(lines, i + 1, numLines)

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
    chapterNumStr = findChapterNum(lines[0])
    addChapterAndSectionNumber(lines, chapterNumStr)
    labelList = createLabelList()
    processAddLabels(lines, chapterNumStr, labelList)
    processReplaceReferences(lines, chapterNumStr, labelList)
    processAddLineNumsInCode(lines)
    writeNewFile(newFileName, lines, chapterNumStr == "")
