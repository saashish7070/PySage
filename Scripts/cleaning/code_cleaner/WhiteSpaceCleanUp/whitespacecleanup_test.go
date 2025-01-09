package WhiteSpaceCleanUp

import (
	"fmt"
	"testing"
)

func TestWhitespacecleanup(t *testing.T){
// Test cases with Python code
    test := "# 1)Дан массив из словарей\u2028"
	
	copyTest := test


	CleanUp(&test)
	fmt.Println(copyTest)
	fmt.Println("#######################################################")
	fmt.Println(test)
}
