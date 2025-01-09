package reindent

import (
	// "fmt"
	"strings"
	re "regexp"
)

var tabR = re.MustCompile("\t")
// Helper function to create indent string
func makeIndent(level int, spacesPerIndent int) string{
	return strings.Repeat(" ", level * spacesPerIndent)
}


// Helper function to count the no. of leading spaces
func countLSpaces(line string) int {
		// If no tabs, count spaces
		spaceCount := len(line) - len(strings.TrimLeft(line, " "))
		return spaceCount
}
func ReindentCode(code *string, spacesPerIndent int) {
	if code == nil {
		return
	}
	*code = tabR.ReplaceAllString(*code, makeIndent(1, spacesPerIndent))

	lines := strings.Split(*code, "\n")
	var result []string
	var continuation bool
	var currentIndent int = 0
	var currentIndentSpaces int = 0

	for i := 0; i < len(lines); i++ {
		line := strings.TrimRight(lines[i], " ")
		
		// Handle empty lines
		if len(strings.TrimSpace(line)) == 0 {
			result = append(result, "")
			continue
		}

		// Handle line continuation
		if continuation {
			result = append(result, makeIndent(currentIndent+1, spacesPerIndent) + strings.TrimLeft(line, " "))
			continuation = strings.HasSuffix(line, "\\")
			continue
		}

		// Check for line continuation
		if strings.HasSuffix(line, "\\") {
			continuation = true
			result = append(result, makeIndent(currentIndent, spacesPerIndent) + strings.TrimLeft(line, " \t"))
			continue
		}

		trimmedLine := strings.TrimSpace(line)

		// Look ahead for indentation changes
		if i < len(lines)-1 {
			nextLine := strings.TrimRight(lines[i+1], " \t")
			if len(strings.TrimSpace(nextLine)) > 0 {	// the line isn't empty
				nextIndentSpaces := countLSpaces(nextLine)

				result = append(result, makeIndent(currentIndent, spacesPerIndent) + trimmedLine)
				if nextIndentSpaces > currentIndentSpaces {
					currentIndent++
					currentIndentSpaces = nextIndentSpaces
				} else if nextIndentSpaces < currentIndentSpaces {
					currentIndent--
					currentIndentSpaces = nextIndentSpaces
				}
			}
			continue
		}

		// Regular line
		result = append(result, makeIndent(currentIndent, spacesPerIndent) + trimmedLine)
	}

	*code = strings.Join(result, "\n")
}
