// Written by Yongjoo Cho
// Last modified 3/29/2022

package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
	"strings"
)

const CHAPTER_REGEXP = "(\\\\@label\\(chapter:)(\\s[0-9]+)(\\))"

//영문/한글/숫자 캡션 가능
const (
	LABEL_FIGURE_REGEXP      = "(\\\\@label\\(fig:)(\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*)(\\))"
	LABEL_TABLE_REGEXP       = "(\\\\@label\\(table:)(\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*)(\\))"
	LABEL_CODE_REGEXP        = "(\\\\@label\\(code:)(\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*)(\\))"
	REF_FIGURE_REGEXP        = "(\\\\@ref\\(fig:)(\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*)(\\))"
	REF_TABLE_REGEXP         = "(\\\\@ref\\(table:)(\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*)(\\))"
	REF_CODE_REGEXP          = "(\\\\@ref\\(code:)(\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*)(\\))"
	REPL_LABEL_FIGURE_REGEXP = "\\\\@label\\(fig:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
	REPL_LABEL_TABLE_REGEXP  = "\\\\@label\\(table:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
	REPL_LABEL_CODE_REGEXP   = "\\\\@label\\(code:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
	REPL_REF_FIGURE_REGEXP   = "\\\\@ref\\(fig:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
	REPL_REF_TABLE_REGEXP    = "\\\\@ref\\(table:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
	REPL_REF_CODE_REGEXP     = "\\\\@ref\\(code:\\s*[a-zA-Z_가-핳]+[a-zA-Z_0-9가-핳]*\\s*\\)"
	CODE_LINE_NUM_REGEXP     = "\\s*\\\\@linenum\\s*```\\s*"
)

type Label struct {
	regExp        regexp.Regexp
	replRegExp    regexp.Regexp
	refRegExp     regexp.Regexp
	replRefRegExp regexp.Regexp
	//regExp        string
	// replRegExp    string
	// refRegExp     string
	// replRefRegExp string
	counter int
	name    string
	replStr string
	labels  map[string]string
}

var sectionNum int = 1

func findChapterNum(line string) string {
	regex := *regexp.MustCompile(CHAPTER_REGEXP)
	res := regex.FindAllStringSubmatch(line, -1)
	if res != nil {
		return strings.TrimSpace(res[0][2]) + "-"
		//		fmt.Printf("chap: %s\n", res[0][2])
	}
	return ""
}

// func replaceReferences(line string, lineNum int, chapterNumStr string, label Label) string { // }: #labels, labelName, regexp, replRegExp):
// 	//	regex := *regexp.MustCompile(label.refRegExp)
// 	res := label.refRegExp.FindAllStringSubmatch(line, -1)
// 	if res != nil {
// 		s := strings.TrimSpace(res[0][2])
// 		if val, ok := label.labels[s]; ok {
// 			//regex2 := *regexp.MustCompile(label.replRefRegExp)
// 			line = label.replRefRegExp.ReplaceAllString(line, val)
// 			//			fmt.Printf("val = %s\n", val)
// 		} else {
// 			fmt.Printf("Error: %d:%s is not in %s labels\n", lineNum, s, label.name)
// 		}
// 	}
// 	return line
// }

func correctPostposition(line string, val string) string {
	eunArr := []int{0, 1, 3, 6, 7, 8}
	neunArr := []int{2, 4, 5, 9}
	postposition := val[len(val)-1:]
	num, _ := strconv.Atoi(postposition)
	for _, n := range eunArr {
		if num == n {
			regex := *regexp.MustCompile(val + "\\s*는")
			regex2 := *regexp.MustCompile(val + "\\s*은")
			line = regex.ReplaceAllString(line, val+"은")
			line = regex2.ReplaceAllString(line, val+"은") // 공백 제거
			return line
		}
	}
	for _, n := range neunArr {
		if num == n {
			regex := *regexp.MustCompile(val + "\\s*는")
			regex2 := *regexp.MustCompile(val + "\\s*은")
			line = regex.ReplaceAllString(line, val+"는")
			line = regex2.ReplaceAllString(line, val+"는") // 공백 제거
			return line
		}
	}
	return line
}

func replaceReferences(line string, lineNum int, chapterNumStr string, label Label) string { // }: #labels, labelName, regexp, replRegExp):
	//	regex := *regexp.MustCompile(label.refRegExp)
	res := label.refRegExp.FindAllStringSubmatch(line, -1)
	if res != nil {
		s := strings.TrimSpace(res[0][2])
		if val, ok := label.labels[s]; ok {
			//regex2 := *regexp.MustCompile(label.replRefRegExp)
			line = label.replRefRegExp.ReplaceAllString(line, val)
			regex := *regexp.MustCompile(val + "\\s*는")
			regex2 := *regexp.MustCompile(val + "\\s*은")
			res1 := regex.FindAllStringSubmatch(line, -1)
			res2 := regex2.FindAllStringSubmatch(line, -1)
			if res1 != nil {
				line = correctPostposition(line, val)
			} else if res2 != nil {
				line = correctPostposition(line, val)
			}
			//			fmt.Printf("val = %s\n", val)
		} else {
			fmt.Printf("Error: %d:%s is not in %s labels\n", lineNum, s, label.name)
		}
	}
	return line
}

func addLabels(line string, lineNum int, chapterNumStr string, label *Label) string { //: #labels, labelName, counter, replStr, regexp, replRegExp):
	//	regex := *regexp.MustCompile(label.regExp)
	res := label.regExp.FindAllStringSubmatch(line, -1)
	if res != nil {
		s := strings.TrimSpace(res[0][2])
		if _, ok := label.labels[s]; ok {
			fmt.Printf("Error:%d:duplicate %s label:%s\n", lineNum, label.name, s)
		} else {
			subStr := label.replStr + chapterNumStr + strconv.Itoa(label.counter)
			//			fmt.Printf("s = %s, subStr = %s\n", s, subStr)
			label.labels[s] = subStr
			label.counter++
			//regex2 := *regexp.MustCompile(label.replRegExp)
			line = label.replRegExp.ReplaceAllString(line, subStr)
		}
	}
	return line
}

func processAddLabels(lines []string, chapterNumStr string, labels []Label) {
	for i := 1; i < len(lines); i++ {
		for _, label := range labels {
			line := addLabels(lines[i], i+1, chapterNumStr, &label)
			if line != lines[i] {
				lines[i] = line
			}
		}
	}
}

func processReplaceReferences(lines []string, chapterNumStr string, labels []Label) {
	for i := 1; i < len(lines); i++ {
		for _, label := range labels {
			line := replaceReferences(lines[i], i+1, chapterNumStr, label)
			if line != lines[i] {
				lines[i] = line
			}
		}
	}
}

// readLines and writeLines are copied from stackoverflow
// https://stackoverflow.com/questions/5884154/read-text-file-into-string-array-and-write
// Read a whole file into the memory and store it as array of lines
func readFile(filename string) (lines []string, err error) {
	var (
		file   *os.File
		part   []byte
		prefix bool
	)
	if file, err = os.Open(filename); err != nil {
		fmt.Printf("Error:opening file %s failed\n", filename)
		return
	}
	defer file.Close()

	reader := bufio.NewReader(file)
	buffer := bytes.NewBuffer(make([]byte, 0))
	for {
		if part, prefix, err = reader.ReadLine(); err != nil {
			break
		}
		buffer.Write(part)
		if !prefix {
			lines = append(lines, buffer.String())
			buffer.Reset()
		}
	}
	if err == io.EOF {
		err = nil
	}
	return
}

func writeNewFile(filename string, lines []string, startFromFirstLine bool) (err error) {
	var (
		file *os.File
	)

	if file, err = os.Create(filename); err != nil {
		fmt.Printf("Error:creating %s failed\n", filename)
		return
	}
	defer file.Close()

	//writer := bufio.NewWriter(file)
	start := 1
	if startFromFirstLine {
		start = 0
	}
	for i := start; i < len(lines); i++ {
		//fmt.Println(item)
		_, err := file.WriteString(strings.TrimSpace(lines[i]) + "\n")
		//file.Write([]byte(item));
		if err != nil {
			//fmt.Println("debug")
			fmt.Println(err)
			break
		}
	}
	/*content := strings.Join(lines, "\n")
	  _, err = writer.WriteString(content)*/
	return
}

func addChapterAndSectionNumber(lines []string, chapterNumStr string) {
	for i := 0; i < len(lines); i++ {
		line := strings.TrimSpace(lines[i])
		if strings.Index(line, "## ") == 0 {
			lines[i] = "## " + chapterNumStr[:len(chapterNumStr)-1] + "." + strconv.Itoa(sectionNum) + " " + line[3:]
			sectionNum++
		} else if strings.Index(line, "# ") == 0 {
			lines[i] = "# " + chapterNumStr[:len(chapterNumStr)-1] + ". " + line[2:]
		}
	}
}

func countLines(lines []string, startLineIdx int) int {
	count := 0
	for startLineIdx < len(lines) {
		line := strings.TrimSpace(lines[startLineIdx])
		if line == "```" {
			break
		}
		count += 1
		startLineIdx += 1
	}
	return count
}

func getNumLength(n int) int {
	count := 1
	for n/10 > 0 {
		count = count + 1
		n = n / 10
	}
	return count

}

func insertLineNumbers(lines []string, startLineIdx int, numLines int) {
	numLen := getNumLength(numLines)

	//    fmt = "{:0" + str(numLen) + "d}"
	count := 1
	for i := startLineIdx; i < startLineIdx+numLines; i++ {
		f := fmt.Sprintf("%0*d", numLen, count)
		lines[i] = f + "    " + lines[i]
		count += 1
	}
}

func processAddLineNumsInCode(lines []string) {
	for i := 1; i < len(lines); i++ {
		matched, _ := regexp.MatchString(CODE_LINE_NUM_REGEXP, lines[i])
		if matched {
			lines[i] = "```\n"
			numLines := countLines(lines, i+1)
			insertLineNumbers(lines, i+1, numLines)
		}
	}
}

func main() {
	newFileName := ""
	if len(os.Args) < 2 {
		fmt.Printf("Usage: %s original_file [new_file]\n", os.Args[0])
		fmt.Println("If [new_file] is omitted, \"preprocessed_\" will be prefixed to the original_file name.")
		os.Exit(0)
	} else if len(os.Args) < 3 {
		newFileName = "preprocessed_" + os.Args[1]
	} else {
		newFileName = os.Args[2]
	}

	//labelFigureRegexp :=
	labels := []Label{
		{*regexp.MustCompile(LABEL_FIGURE_REGEXP), *regexp.MustCompile(REPL_LABEL_FIGURE_REGEXP),
			*regexp.MustCompile(REF_FIGURE_REGEXP), *regexp.MustCompile(REPL_REF_FIGURE_REGEXP),
			1, "figure", "그림 ", make(map[string]string)},
		{*regexp.MustCompile(LABEL_TABLE_REGEXP), *regexp.MustCompile(REPL_LABEL_TABLE_REGEXP),
			*regexp.MustCompile(REF_TABLE_REGEXP), *regexp.MustCompile(REPL_REF_TABLE_REGEXP),
			1, "table", "표 ", make(map[string]string)},
		{*regexp.MustCompile(LABEL_CODE_REGEXP), *regexp.MustCompile(REPL_LABEL_CODE_REGEXP),
			*regexp.MustCompile(REF_CODE_REGEXP), *regexp.MustCompile(REPL_REF_CODE_REGEXP),
			1, "code", "코드 ", make(map[string]string)}}

	lines, err := readFile(os.Args[1])
	if err != nil {
		fmt.Println(err)
		os.Exit(-1)
	}
	chapterNumStr := findChapterNum(lines[0])
	// if chapterNumStr != "" {
	// 	fmt.Printf("chap num: %s\n", chapterNumStr)
	// }
	addChapterAndSectionNumber(lines, chapterNumStr)
	processAddLabels(lines, chapterNumStr, labels)
	processReplaceReferences(lines, chapterNumStr, labels)
	processAddLineNumsInCode(lines)
	_ = writeNewFile(newFileName, lines, chapterNumStr == "")
}
