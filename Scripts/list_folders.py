import os
from pathlib import Path

def list_folders(path: str) -> list:
    """
    List all folders in the given path
    
    Args:
        path (str): Path to directory
        
    Returns:
        list: List of folder names
    """
    # Method 1: Using os.listdir
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    
    # Method 2: Using pathlib (more modern approach)
    # folders = [f.name for f in Path(path).iterdir() if f.is_dir()]
    
    return folders

def main():
    path = "./new-python-dataset"  # Replace with your path
    
    try:
        folders = list_folders(path)
        print(f"\nFolders in {path}:")
        print("=" * 50)
        for i, folder in enumerate(sorted(folders), 1):
            print(f"{i}. {folder}")
            
    except FileNotFoundError:
        print(f"Error: Path '{path}' not found")
    except PermissionError:
        print(f"Error: Permission denied to access '{path}'")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 