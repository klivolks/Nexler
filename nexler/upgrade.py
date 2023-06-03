import os
import shutil
import urllib.request
import zipfile
import nexler  # import nexler to check its version
from git import Repo


def upgrade():
    try:
        # Step 1: Check the current version
        current_version = nexler.__version__

        # Step 2: Compare with the version from GitHub
        repo = Repo.clone_from("https://github.com/klivolks/Nexler.git", "temp_repo")
        temp_nexler_init_file = open("temp_repo/nexler/__init__.py", "r")
        lines = temp_nexler_init_file.readlines()
        for line in lines:
            if "__version__" in line:
                github_version = line.split("=")[-1].strip().strip("\"'")

        # Clean up the temp repo
        shutil.rmtree("temp_repo")

        # Check if the versions are different
        if github_version != current_version:
            # Step 3: If they are, download the new version from GitHub
            print(f"Upgrading Nexler from version {current_version} to {github_version}")
            print("Please wait...")

            url = "https://github.com/klivolks/Nexler/archive/refs/heads/main.zip"
            urllib.request.urlretrieve(url, "Nexler-main.zip")

            with zipfile.ZipFile("Nexler-main.zip", "r") as zip_ref:
                zip_ref.extractall("./")

            # Update the necessary files and folders
            folders_files_to_update = ["run.py", "setup.py", "nexler", "app/services", 
                                       "app/utils", "app/config", "docs", "tests/app/utils", 
                                       "tests/app/services", "README.md", "requirements.txt"]

            for item in folders_files_to_update:
                if os.path.exists(item):
                    shutil.rmtree(item)
                shutil.move(f"Nexler-main/{item}", "./")

            # Remove the downloaded zip file and the extracted folder
            os.remove("Nexler-main.zip")
            shutil.rmtree("Nexler-main")

            # Step 4: Install the new version
            os.system("pip install .")

        else:
            print("Nexler is up-to-date.")

    except Exception as e:
        print(f"An error occurred while upgrading Nexler: {e}")
