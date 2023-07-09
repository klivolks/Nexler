import os
import shutil
import urllib.request
import zipfile
import nexler  # import nexler to check its version
from git import Repo
import traceback


def check_and_create_dir(path):
    """
    Check if the given path exists and if not create it.
    :param path: The path to check and create.
    :return: None
    """
    if not os.path.exists(path):
        os.makedirs(path)


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
                                       "app/utils", "tests/app/utils",
                                       "tests/app/services", "requirements.txt", "migrations", ".env-example",
                                       "environment.py"]

            for item in folders_files_to_update:
                # If it is a file or directory and exists in the current location, remove it
                if os.path.exists(item):
                    if os.path.isfile(item):
                        os.remove(item)
                    elif os.path.isdir(item):
                        shutil.rmtree(item)

                # If it exists in the downloaded package, move it to the correct location
                if os.path.exists(f"Nexler-main/{item}"):
                    dir_part = os.path.dirname(item)
                    if bool(dir_part):
                        check_and_create_dir(dir_part)  # create directories if they don't exist

                    shutil.move(f"Nexler-main/{item}", f"./{item}")  # move item to the correct directory

                else:
                    print(f"{item} does not exist in the downloaded package.")

            # check and create required directories for further enhancement and services
            directories_needed = [
                "app/templates/email",
                "app/templates/sms"
            ]
            for items in directories_needed:
                check_and_create_dir(items)

            # Remove the downloaded zip file and the extracted folder
            os.remove("Nexler-main.zip")
            shutil.rmtree("Nexler-main")

            # Step 4: Install the new version
            os.system("pip install .")

        else:
            print("Nexler is up-to-date.")

    except Exception as e:
        print(f"An error occurred while upgrading Nexler: {e}")
        # Print detailed error traceback
        traceback.print_exc()
        # Clean up if anything went wrong
        if os.path.exists("Nexler-main.zip"):
            os.remove("Nexler-main.zip")
        if os.path.exists("Nexler-main"):
            shutil.rmtree("Nexler-main")
