package NormalizeStrings

import(
	"fmt"
	"testing"
)

func TestNormalizeStringQuotes(t *testing.T) {

	stringLiterals := []string{
		`'''很长的中文 Hello how are you""'''`,
		`"""Hello how are you'' ?"""`,
		`'Hello "world"'`,
		`"Python's awesome"`,
		`'''Multi-line "string"'''`,
		`"""Another 'multi-line' string"\""""`,
		`"""Hello how are you'' ?"""`,
		`"Hello \"world\""`,
		`"Python\'s awesome"`,
		`"""Multi-line "string\""""`,
		`"""Another 'multi-line' string"""`,

	}

	copyStringLiterals := stringLiterals

	NormalizeStringQuotes(&stringLiterals)

	// 
	fmt.Printf("%-40s|%-40s|%s\n","Original String", "Normalized String", "isEngilsh")
	for i, s := range stringLiterals {
		fmt.Printf("%-40s|%-40s|%t\n", copyStringLiterals[i], s, !DetectNonEnglish(&s))
	}


}