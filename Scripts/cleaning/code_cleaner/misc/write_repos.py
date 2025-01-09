# write repos to a file

import os
import json

def write_repos(repos_dir, out_dir, num_files):

    count = 0
    repos_files = os.listdir(repos_dir)
    for repo_file in repos_files:
        with open(os.path.join(repos_dir, repo_file), 'r') as f:
        
            for repo in f:
                if count >= num_files:
                    break
                repo = json.loads(repo)
                repo_name = repo['repo_name']
                repo_name = repo_name.replace('/', '_')
                with open(os.path.join(out_dir, repo_name + '.py'), 'w') as out_file:
                    for file in repo['files']:
                        out_file.write('#' + file['path'] + "\n")
                        out_file.write(file.get('content', '') + "\n")
                count += 1

def main():
    repos_dir = './new-python-dataset/syntax_free_repos'
    out_dir = './new-python-dataset/view_repos'
    
    # create the directory if it doesn't exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    write_repos(repos_dir, out_dir, 10)

if __name__ == "__main__":
    main()