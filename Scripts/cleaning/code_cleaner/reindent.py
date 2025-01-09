import tokenize
import multiprocessing as mp
import os
import sys
from typing import List, Dict, Any, Generator
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('reindent.log'),
        logging.StreamHandler()
    ]
)

# Count number of leading blanks.
def getlspace(line):
    i, n = 0, len(line)
    while i < n and line[i] == " ":
        i += 1
    return i

def usage(msg=None):
    if msg is None:
        msg = __doc__
    print(msg, file=sys.stderr)


def errprint(*args):
    sys.stderr.write(" ".join(str(arg) for arg in args))
    sys.stderr.write("\n")






def _rstrip(line, JUNK='\n \t'):
    """Return line stripped of trailing spaces, tabs, newlines.

    Note that line.rstrip() instead also strips sundry control characters,
    but at least one known Emacs user expects to keep junk like that, not
    mentioning Barry by name or anything <wink>.
    """

    i = len(line)
    while i > 0 and line[i - 1] in JUNK:
        i -= 1
    return line[:i]


class Reindenter:
    def __init__(self):
        pass

    def run(self, code, space_per_indent):
        self.level=0    # current indent level
        self.find_stmt = 1 # next token begins a fresh stmt?
        self.index=1    # index into self.lines of next line

        # List of (lineno, indentlevel) pairs, one for each stmt and
        # comment line.  indentlevel is -1 for comment lines, as a
        # signal that tokenize doesn't know what to do about them;
        # indeed, they're our headache!
        self.stats=[]
        self.raw = code.splitlines()
        self.lines =[_rstrip(line).expandtabs() + "\n"
                    for line in self.raw]
        self.lines.insert(0, None)

        tokens = tokenize.generate_tokens(self.getline)
        try: 
    
            for _token in tokens:
                self.tokeneater(*_token)
        except Exception as e:
            raise("An exception occurred ", e)
            
        # Remove trailing empty lines.
        lines = self.lines
        while lines and lines[-1] == "\n":
            lines.pop()
        # Sentinel.
        stats = self.stats
        stats.append((len(lines), 0))
        # Map count of leading spaces to # we want.
        have2want = {}
        # Program after transformation.
        after = self.after = []
        # Copy over initial empty lines -- there's nothing to do until
        # we see a line with *something* on it.
        i = stats[0][0]
        after.extend(lines[1:i])
        for i in range(len(stats) - 1):
            thisstmt, thislevel = stats[i]
            nextstmt = stats[i + 1][0]
            have = getlspace(lines[thisstmt])
            want = thislevel * space_per_indent
            if want < 0:
                # A comment line.
                if have:
                    # An indented comment line.  If we saw the same
                    # indentation before, reuse what it most recently
                    # mapped to.
                    want = have2want.get(have, -1)
                    if want < 0:
                        # Then it probably belongs to the next real stmt.
                        for j in range(i + 1, len(stats) - 1):
                            jline, jlevel = stats[j]
                            if jlevel >= 0:
                                if have == getlspace(lines[jline]):
                                    want = jlevel * space_per_indent
                                break
                    if want < 0:           # Maybe it's a hanging
                                           # comment like this one,
                        # in which case we should shift it like its base
                        # line got shifted.
                        for j in range(i - 1, -1, -1):
                            jline, jlevel = stats[j]
                            if jlevel >= 0:
                                want = have + (getlspace(after[jline - 1]) -
                                               getlspace(lines[jline]))
                                break
                    if want < 0:
                        # Still no luck -- leave it alone.
                        want = have
                else:
                    want = 0
            assert want >= 0
            have2want[have] = want
            diff = want - have
            if diff == 0 or have == 0:
                after.extend(lines[thisstmt:nextstmt])
            else:
                for line in lines[thisstmt:nextstmt]:
                    if diff > 0:
                        if line == "\n":
                            after.append(line)
                        else:
                            after.append(" " * diff + line)
                    else:
                        remove = min(getlspace(line), -diff)
                        after.append(line[remove:])
        return self.after



    # Line-getter for tokenize.
    def getline(self):
        if self.index >= len(self.lines):
            line = ""
        else:
            line = self.lines[self.index]
            self.index += 1
        return line

    # Line-eater for tokenize.
    def tokeneater(self, type, token, slinecol, end, line,
                   INDENT=tokenize.INDENT,
                   DEDENT=tokenize.DEDENT,
                   NEWLINE=tokenize.NEWLINE,
                   COMMENT=tokenize.COMMENT,
                   NL=tokenize.NL):

        if type == NEWLINE:
            # A program statement, or ENDMARKER, will eventually follow,
            # after some (possibly empty) run of tokens of the form
            #     (NL | COMMENT)* (INDENT | DEDENT+)?
            self.find_stmt = 1

        elif type == INDENT:
            self.find_stmt = 1
            self.level += 1

        elif type == DEDENT:
            self.find_stmt = 1
            self.level -= 1

        elif type == COMMENT:
            if self.find_stmt:
                self.stats.append((slinecol[0], -1))
                # but we're still looking for a new stmt, so leave
                # find_stmt alone

        elif type == NL:
            pass

        elif self.find_stmt:
            # This is the first "real token" following a NEWLINE, so it
            # must be the first token of the next program statement, or an
            # ENDMARKER.
            self.find_stmt = 0
            if line:   # not endmarker
                self.stats.append((slinecol[0], self.level))

def load_data(
    file_path: str, 
    previous_idx: int = 0, 
    chunk_size: int = 3000
) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Load data from JSONL file in chunks.
    
    Args:
        file_path (str): Path to JSONL file
        previous_idx (int): Index to start reading from
        chunk_size (int): Number of lines to read
    
    Returns:
        Generator yielding lists of repository data
    """
    try:
        with open(file_path, 'r') as f:
            # Skip to previous index
            for _ in range(previous_idx):
                next(f, None)
            
            code = []
            for line in f:
                json_code = json.loads(line)
                code.append(json_code)
                
                if len(code) == chunk_size:
                    yield code
                    code = []
            if code:
                yield code
        
    except IOError as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return []
def write_repos(repos: List[str], output_path: str):
    """
    Write syntax-free repository names to a file.
    
    Args:
        repos (List[str]): Repository names
        output_path (str): Path to output file
    """
    with open(output_path, 'a') as f:
        for repo in repos:
            f.write(json.dumps(repo) + '\n')

def process_task(idx, file, output_path, file_prefix ):
    generator = load_data(file, 0, 2000)
    for repos in generator:
        reindented_repos = []
        for repo in repos:
            reindented_files = []
            try:
                for file in repo['files']:
                    reindented_code = r.run(file['content'], SPACE_PER_INDENT)

                    file['content'] = reindented_code
                
                    reindented_files.append(file)
                
                repo['files'] = reindented_files
                    
            except Exception as e:
                    logging.error(f"Error while reindenting file {file} : {e}")
                    print(f"Cannot reindnent file {file} with repo  name {repo['repo_name']}")


            # repo['files'] = reindented_files

            reindented_repos.append(repo)

        write_repos(reindented_repos, os.path.join(output_path, f"{file_prefix}_{idx}.jsonl"))

r = Reindenter()
SPACE_PER_INDENT=4
if __name__ == '__main__':
    inDir = './new-python-dataset/syntax_free_repos'
    outDir = './code-data/'

    files = os.listdir(inDir)

    num_workes = min(mp.cpu_count(), len(files))
    
    
    with mp.Pool(processes=num_workes) as pool:
        pool.starmap(process_task, [(i, os.path.join(inDir, file), outDir, "code") for i, file in enumerate(files)])
