package reindent
import (
	"testing"
	"fmt"

)

func TestReindent(t *testing.T){
	code := `def example():
     x = 5 + \
         3
     if x > 0:
          print("positive")
          return ( my_object
		  			.prepare_data()
					.transform_data()
					.finalize()
		  )
     return None`
	fmt.Println(code)
	ReindentCode(&code, 4)
	fmt.Println("#######################################################")
	fmt.Println(code)

}