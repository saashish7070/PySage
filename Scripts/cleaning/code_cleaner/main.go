package main

import (
	reader "code_cleaner/repos_reader"
	"code_cleaner/NormalizeStrings"
	"code_cleaner/WhiteSpaceCleanUp"
	"fmt"
	"os"
	"sync"
	"encoding/json"
	re "regexp"
)
const stringPlaceHolder = "STRING_PLACEHOLDER"
var stringRegex = re.MustCompile(`"""(?:[^\\]|\\.|\n)*?"""|"(?:[^\\]|\\.)*?"|'(?:[^\\]|\\.)*?'|'''(?:[^\\]|\\.|\n)*?'''`)
var stringPlaceHolderR = re.MustCompile(stringPlaceHolder)



func processRepo(repo reader.Repo) reader.Repo{
	cleanedRepo := repo

	for i, file := range repo.Files {
		stringContent := string(file.Content)
		stringMatches := make([]string, 0)
			
		// store and replace all the matches
		stringRegex.ReplaceAllStringFunc(stringContent, func(s string) string{
			stringMatches = append(stringMatches, s)
			return stringPlaceHolder
		})

		englishOnlyString := make([]string, 0)
		for _, s := range stringMatches {
			if NormalizeStrings.DetectNonEnglish(&s) {
				// string literal consist of non english tokens
				englishOnlyString = append(englishOnlyString, "\"\"\"\"\"\"")

			}else{
				englishOnlyString = append(englishOnlyString, s)
			}
		}


		// code cleaning pipeline
		// process all the single quote matches
		NormalizeStrings.NormalizeStringQuotes(&englishOnlyString)
		WhiteSpaceCleanUp.CleanUp(&stringContent)
		// end of processing
		

		matchIndex := 0 // to keep count of the index of the match
		stringPlaceHolderR.ReplaceAllStringFunc(stringContent, func(s string) string{
			res := englishOnlyString[matchIndex]
			matchIndex++
			return res
		})

		cleanedRepo.Files[i].Content = stringContent
	}

	return cleanedRepo

}

func processFile(idx int, file string, outputPath string){
	var cleanedRepos [] reader.Repo
	// read the file
	repos, err := reader.ReadRepos(file)
	if err != nil {
		fmt.Println("Error reading repos")
		return 
	}
	for _, repo := range repos{
		res := processRepo(repo)
		cleanedRepos = append(cleanedRepos, res)
	}
	
	outFile, err := os.Create(fmt.Sprintf("%s/data_%d.jsonl", outputPath, idx))
	if err != nil {
		fmt.Println("Error creating file:", err)
		return 
	}
	
	defer outFile.Close()
	
	
	for _, repo := range cleanedRepos {
		jsonData, err := json.Marshal(repo)
		if err != nil {
			fmt.Printf("Error marshalling repo: %v\n", err)
			return	
		}

		outFile.Write(append(jsonData, '\n'))
	}
}


func main(){
	codeDataPath := "../../../new-python-dataset/syntax_free_repos"
	// var output_path = "../../../new-python-dataset/cleaned_data"
	outputPath := "../../../new-python-dataset/cleaned_data"
	// determine files
	files, err := os.ReadDir(codeDataPath)
	
	if err != nil {
		return
	}

	// concurrently process each file
	wg := sync.WaitGroup{}

	for i, file := range files{
		// process each file
		filePath := fmt.Sprintf("%s/%s", codeDataPath, file.Name())
		wg.Add(1)
		go func(idx int, file string){
			defer wg.Done()
			processFile(idx, file, outputPath)
		}(i, filePath)
	}
	wg.Wait()
}
