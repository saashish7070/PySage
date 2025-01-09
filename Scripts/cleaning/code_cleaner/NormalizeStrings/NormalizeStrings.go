package NormalizeStrings

import (
	"strings"
	re "regexp"
)

var rNonEnglishPattern = re.MustCompile(`[^\x00-\x7F]`)
// modifing to make it work with predetermined strings found in the code
func NormalizeStringQuotes(str *[]string) {
	// assumes the string is valid a valid python string
	var output []string
	
	
	for _, s := range *str {
		if s[0] == '"' {
			output = append(output, s)
			continue
		}
		
		var result strings.Builder
		runes := []rune(s)
		// var rawString bool
		var isTripleQuoted bool = false // if the string is enclosed by -> '
		var runeStart int = 1
		var runeEnd int = len(runes) - 1

	

		// determine if the string is single quoted or triple quoted
		if len(s) >= 6 && s[0] == '\'' && s[1] == '\'' && s[2] == '\'' {
			isTripleQuoted = true
		}
		
		// strip the quotes based on the type of the string
		if isTripleQuoted{
			runeStart = 3
			runeEnd = len(runes)-3
			result.WriteString("\"\"\"")
		}
		
		for i := runeStart; i < runeEnd; i++ {
			char := runes[i]

			// handle escaped characters
			if char == '\\' {
				// check if the character is a quote which we are trying to escape
				if (runes[i+1] == '\''){
					// no need to escape as we are enclosing in double quotes
					result.WriteRune('\'')
				}else{
					result.WriteRune('\\')
					result.WriteRune(runes[i+1])
				}
				i++
				continue
			}


			// Handle quote escaping
			if char == '"' {
				if isTripleQuoted && (i == runeStart || i == runeEnd-1) {
					// Escape only if it's a triple-quoted string and the quote appears at the start or end
					result.WriteString("\\\"")
				} else if !isTripleQuoted {
					// Always escape quotes for non-triple-quoted strings
					result.WriteString("\\\"")
				} else{
					result.WriteRune(char)
				}
				continue
			}

			result.WriteRune(char)
	
		}
		
		// add the quotes back to the string, infront and behind the string
		if isTripleQuoted{
			result.WriteString("\"\"\"")
		}else{
			result.WriteString("\"")
		}

		output = append(output, result.String())
	}
	*str = output
}

// cleans the string if it consists of non english characters
func DetectNonEnglish(s* string) bool{
	return rNonEnglishPattern.MatchString(*s)
}
