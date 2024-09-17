import os
import re
from collections import defaultdict, deque

def has_dependency(fileA_content, fileB_name):
    """
    Check if fileA depends on fileB based on import statements.
    This function uses a regex to identify 'import' statements in Python.
    """
    import_pattern = re.compile(rf'import\s+{re.escape(fileB_name)}|from\s+{re.escape(fileB_name)}\s+import')
    return bool(import_pattern.search(fileA_content))

def parse_files(directory):
    """
    Parse Python files in a given directory to detect dependencies and
    build the adjacency list for dependency analysis.
    """
    files = [f for f in os.listdir(directory) if f.endswith('.py')]
    graphs = defaultdict(list)
    in_degree = defaultdict(int)
    file_contents = {}

    # Read the content of each file and store it in memory
    for file in files:
        with open(os.path.join(directory, file), 'r') as f:
            file_contents[file] = f.read()

    # Build the dependency graph and in-degree dictionary
    for fileA in files:
        for fileB in files:
            if fileA != fileB and has_dependency(file_contents[fileA], os.path.splitext(fileB)[0]):
                graphs[fileB].append(fileA)
                in_degree[fileA] += 1

    return files, graphs, in_degree 

def topological_sort(files, graphs, in_degree):
    """
    Perform topological sort based on the dependency graph.
    If cycles exist, pick the node with the minimal in-degree.
    """
    sorted_files = []
    queue = deque([file for file in files if in_degree[file] == 0])

    while queue:
        file = queue.popleft()
        sorted_files.append(file)

        for neighbor in graphs[file]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_files) != len(files):
        print("Cycle detected! Topological sort not possible.")
        return []

    return sorted_files

def analyze_project(directory):
    """
    Analyze the given directory of Python files to generate a sorted list
    based on their dependencies.
    """
    files, graphs, in_degree = parse_files(directory)
    sorted_files = topological_sort(files, graphs, in_degree)

    if sorted_files:
        print("Topologically sorted files:")
        for file in sorted_files:
            print(file)
    else:
        print("Unable to sort files due to a dependency cycle.")

# Example usage
directory = 'path/to/your/python/repository'
analyze_project(directory)
