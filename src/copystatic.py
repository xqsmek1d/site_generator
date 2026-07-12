import os
import shutil

def copystatic(static_path: str = "./static", public_path: str = "./public") -> None:
    if not os.path.exists(static_path):
        raise Exception("Error: invalid static path directory!")

    # Delete all the contents of the destination directory (public) to ensure clean copy
    if os.path.exists(public_path):
        print("Warning: deleting and overwriting current public_path directory")
        shutil.rmtree(public_path)
    os.mkdir(public_path)

    for file in os.listdir(static_path):
        static_fpath = os.path.join(static_path,file)
        public_fpath = os.path.join(public_path,file)
        if os.path.isfile(static_fpath):
            print(f"Copying: {static_fpath} to {public_fpath}")
            shutil.copy(static_fpath, public_fpath)
        if os.path.isdir(static_fpath):
            print(f"Entering directory: {static_fpath} to copy files from here to {public_fpath}")
            copystatic(static_fpath, public_fpath)
