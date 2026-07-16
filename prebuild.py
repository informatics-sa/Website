import requests
import os
import argparse
import shutil

GITHUB_REPO = 'https://github.com/informatics-sa/WebsiteBuilder'

parser = argparse.ArgumentParser()
parser.add_argument("--path", required=False)

args = parser.parse_args()

from_github = False

if args.path is None:
    print("Collecting from github")
    from_github = True
else:
    print(f"Path: {args.path}")

def repo_to_api(github_repo: str) -> str:
    # Convert https://github.com/owner/repo → https://api.github.com/repos/owner/repo
    parts = github_repo.rstrip('/').split('github.com/')[-1]
    return f"https://api.github.com/repos/{parts}"

def list_files(github_repo: str, path: str = "") -> list[dict]:
    """Recursively list all files in the repo, returns list of {path, download_url}."""
    api_url = f"{repo_to_api(github_repo)}/contents/{path}"
    response = requests.get(api_url)
    response.raise_for_status()

    files = []
    for item in response.json():
        if item['type'] == 'file':
            files.append({'path': item['path'], 'download_url': item['download_url']})
        elif item['type'] == 'dir':
            files.extend(list_files(github_repo, item['path']))
    return files

def download_file(file: dict, dest_dir: str) -> None:
    """Download a single file and save it relative to dest_dir."""
    response = requests.get(file['download_url'])
    response.raise_for_status()

    dest_path = os.path.join(dest_dir, file['path'])
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'wb') as f:
        f.write(response.content)
    print(f"[COPY] {file['path']}")

def main():
    dest_dir = os.path.dirname(os.path.abspath(__file__))

    print(f"[INFO] Destination: {dest_dir}")
    
    if from_github:
        print(f"[INFO] Listing files from {GITHUB_REPO} ...")

        files = list_files(GITHUB_REPO)
        print(f"[INFO] Found {len(files)} file(s)\n")

        for f in files:
            if os.path.basename(f["path"]).lower() == "readme.md": continue
            download_file(f, dest_dir)
    else:
        source_dir = args.path

        print(f"[INFO] Listing files from {source_dir} ...")

        shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git", "README.md")) # copy from source_dir to dest_dir



    print(f"\n[DONE]")

main()
