package WhiteSpaceCleanUp

import (
	"regexp"
	"strings"
	"unicode"
)
var codePatterns = []*regexp.Regexp{
    // Function definitions
    regexp.MustCompile(`^def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(`),
    
    // Class definitions
    regexp.MustCompile(`^class\s+[a-zA-Z_][a-zA-Z0-9_]*\s*[:\(]`),
    
    // Variable assignments with operators
    regexp.MustCompile(`^[a-zA-Z_][a-zA-Z0-9_]*\s*[+\-*/]?=\s*[^=]`),
    
    // Function calls
    regexp.MustCompile(`^[a-zA-Z_][a-zA-Z0-9_]*\s*\([^\)]*\)`),
    
    // Control flow with proper syntax
    regexp.MustCompile(`^if\s+.+:`),
    regexp.MustCompile(`^elif\s+.+:`),
    regexp.MustCompile(`^else\s*:`),
    regexp.MustCompile(`^while\s+.+:`),
    regexp.MustCompile(`^for\s+.+\s+in\s+.+:`),
    regexp.MustCompile(`^try\s*:`),
    regexp.MustCompile(`^except\s*.*:`),
    regexp.MustCompile(`^finally\s*:`),
    
    // List/dict comprehensions
    regexp.MustCompile(`\[\s*[a-zA-Z_][a-zA-Z0-9_]*\s+for\s+[a-zA-Z_][a-zA-Z0-9_]*\s+in\s+.+\]`),
    
    // Method calls
    regexp.MustCompile(`^[a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*\(`),
    
    // Multi-part operators that are rare in natural language
    regexp.MustCompile(`[a-zA-Z0-9_]\s*([+\-*/]?=|<=|>=|!=|==)\s*[a-zA-Z0-9_]`),
    
    // Common Python builtins with parentheses
    regexp.MustCompile(`(print|len|range|str|int|list|dict|set|tuple)\s*\(`),
    
    // Dictionary operations
    regexp.MustCompile(`^[a-zA-Z_][a-zA-Z0-9_]*\[[^\]]+\]\s*=`),
    
    // Return statements
    regexp.MustCompile(`^return\s+[a-zA-Z0-9_\[\{\(]`),
    
    // Import statements
    regexp.MustCompile(`^from\s+[a-zA-Z_][a-zA-Z0-9_.]*\s+import\s+`),
    regexp.MustCompile(`^import\s+[a-zA-Z_][a-zA-Z0-9_.]*\s*`),
}

// Replace more than 2 spaces with 2 spaces
var spaceRegex = regexp.MustCompile(` {3,}`)
// Replace more than 3 line breaks with 3 line breaks
var lineBreakRegex = regexp.MustCompile(`(\n){4,}`)

func CleanUp(code *string) {
	if code == nil {
		return
	}
	
	*code = spaceRegex.ReplaceAllString(*code, "  ")	
	*code = lineBreakRegex.ReplaceAllString(*code, "\n\n\n")
	
	// Strip leading and trailing spaces from each line
	lines := strings.Split(*code, "\n")
    cleanedLines := make([]string, 0)

	for i, line := range lines {
		lines[i] = strings.TrimSpace(line)
        commentFilteredLines := commentCleanUp(&line)
        cleanedLines = append(cleanedLines, commentFilteredLines)
	}

	*code = strings.Join(cleanedLines, "\n")
	
	// Ensure a single trailing newline at the end of the file
	*code = strings.TrimRight(*code, "\n") + "\n"
}


// isNonEnglish checks if a string contains any non-ASCII characters
func isNonEnglish(s string) bool {
    for _, r := range s {
        if r > unicode.MaxASCII {
            return true
        }
    }
    return false
}

// hasComment checks if a line contains a comment and returns it
// Returns: comment text (without #), remainingCode, hasComment
func hasComment(line string) (string, string, bool) {
    // Handle empty or nil cases
    if line == "" {
        return "", "", false
    }

    for i, char := range line {

        if char == '#'{
            comment := strings.TrimSpace(line[i+1:])
            code := strings.TrimSpace(line[:i])
            return comment, code, true

        }
    }
    
    return "", line, false
}

// isPythonCode checks if a string looks like Python code using more robust pattern matching
func isPythonCode(content string) bool {
    // Common patterns that strongly indicate code rather than natural language
    

    // Check for indentation (must be consistent spacing)
    if strings.HasPrefix(content, "    ") || strings.HasPrefix(content, "\t") {
        indentPattern := regexp.MustCompile(`^(\s+)[^\s]`)
        matches := indentPattern.FindStringSubmatch(content)
        if matches != nil {
            indent := matches[1]
            // Check if indentation is consistent (all spaces or all tabs)
            if strings.Count(indent, " ") == len(indent) || strings.Count(indent, "\t") == len(indent) {
                return true
            }
        }
    }

    // Check against all code patterns
    for _, pattern := range codePatterns {
        if pattern.MatchString(strings.TrimSpace(content)) {
            return true
        }
    }

    // Additional checks for compound statements and expressions
    compoundPatterns := []string{
        "and ", "or ", "not ",
        "True", "False", "None",
        "self.", "__init__",
    }

    // Count code indicators
    codeIndicatorCount := 0
    for _, pattern := range compoundPatterns {
        if strings.Contains(content, pattern) {
            codeIndicatorCount++
        }
    }

    // If we find multiple code indicators, it's likely code
    return codeIndicatorCount >= 2
}



// commentCleanUp processes a line according to the specified rules
func commentCleanUp(line *string) string{
	
    if line == nil || *line == "" {
        return ""
    }

    
    comment, code, hasComment := hasComment(*line)
    if comment == "" || !hasComment || isNonEnglish(comment) || isPythonCode(comment){
        return code
    }
    return *line
}