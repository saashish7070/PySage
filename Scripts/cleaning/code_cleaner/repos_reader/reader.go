package repos_reader
// given a string of json, convert the json object into a repo struct
// the repo struct is defined below
import (
	"fmt"
	"bufio"
	"os"
	"encoding/json"
)
// repo format
// {
//     "repo_name": <str>,
//     "repo_url": <str>,
//     "gha_language": <str>,
//     "files": [
//         {
//             "blob_id": <str>,
//             "path": <str>,
//             "content_id": <str>,
//             "language": <str>,
//             "length_bytes": <int>,
//             "detected_licenses": <list>,
//             "license_type": <str>,
//             "src_encoding": <str>,
//             "is_vendor": <bool>,
//             "is_generated": <bool>,
//             "alphanum_fraction": <float>,
//             "alpha_fraction": <float>,
//             "num_lines": <int>,
//             "avg_line_length": <float>,
//             "max_line_length": <int>,
//             "content": <str>
//         }
//     ]
// }

type File struct{
	Path string `json:"path"`
	Content string `json:"content"`
}

type Repo struct{
	RepoName string `json:"repo_name"`
	RepoUrl string `json:"repo_url"`
	GhaLanguage string `json:"gha_language"`
	Files []File `json:"files"`
}

func Convert(data string) (Repo, error){
	var r Repo
	err := json.Unmarshal([]byte(data), &r)

	return r, err
}

func ReadRepos(path string) ([]Repo, error){
	file, err := os.Open(path)
	if err != nil{
		fmt.Println("Error openning file", err)
		return nil, err
	}
	defer file.Close()

	var repos []Repo

	scanner := bufio.NewScanner(file)

	const maxCapacity = 60 * 1024 * 1024
	buf := make([]byte, maxCapacity)
	scanner.Buffer(buf, maxCapacity)
	
	for scanner.Scan(){
		if len(scanner.Bytes()) > 10 * 1024 * 1024 {
			fmt.Println("The size of text in MB is ", len(scanner.Bytes()) * 60 / maxCapacity )
		}
		repo, err := Convert(scanner.Text())
		if err != nil{
			fmt.Println("Eror converting repos", err)
			return nil, err
		}
		repos = append(repos, repo)
	}

	if err := scanner.Err(); err != nil{
		fmt.Println("Scanner error", err)
		return nil, err
	}

	return repos, nil
}
