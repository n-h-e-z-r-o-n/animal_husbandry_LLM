# Import the shutil module
import shutil

# Define the source folder and the destination folder
source = r"C:\Users\HEZRON WEKESA\Downloads\New folder"
nama = "KCSE DATASET"
destination = r"C:\Users\HEZRON WEKESA\Downloads\KCSE DATASET"+fr"\{nama}"

# Copy the entire folder and its contents
shutil.copytree(source, destination)

# Print a confirmation message
print(f"Successfully duplicated {source} as {destination}")
