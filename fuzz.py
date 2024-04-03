import os
import shutil
import subprocess

# Initialize a list to store the crashes
crashes = []

def deleteRepo(dirName, type_):
    print(':::' + type_ + ':::Deleting ', dirName)
    try:
        if os.path.exists(dirName):
            shutil.rmtree(dirName)
    except OSError:
        print('Failed deleting, will try manually')

# Generate crashes by passing invalid directory names
try:
    deleteRepo(None, 'INVALID_DIRECTORY_NAME')
except Exception as e:
    crashes.append(f"deleteRepo: {type(e).__name__}: {str(e)}")

try:
    deleteRepo('', 'EMPTY_DIRECTORY_NAME')
except Exception as e:
    crashes.append(f"deleteRepo: {type(e).__name__}: {str(e)}")

try:
    deleteRepo('nonexistent_dir', 'NONEXISTENT_DIRECTORY')
except Exception as e:
    crashes.append(f"deleteRepo: {type(e).__name__}: {str(e)}")

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP )
    fileToWrite.close()
    return str(os.stat(fileP).st_size)

# Generate crashes by passing invalid file paths
try:
    dumpContentIntoFile("test", None)
except Exception as e:
    crashes.append(f"dumpContentIntoFile: {type(e).__name__}: {str(e)}")

try:
    dumpContentIntoFile("test", '')
except Exception as e:
    crashes.append(f"dumpContentIntoFile: {type(e).__name__}: {str(e)}")

def makeChunks(the_list, size_):
    for i in range(0, len(the_list), size_):
        yield the_list[i:i+size_]

# Generate crashes by passing an invalid size (0)
try:
    for chunk in makeChunks([1, 2, 3], 0):
        print(chunk)
except Exception as e:
    crashes.append(f"makeChunks: {type(e).__name__}: {str(e)}")

def cloneRepo(repo_name, target_dir):
    cmd_ = "git clone " + repo_name + " " + target_dir
    try:
       subprocess.check_output(['bash','-c', cmd_])
    except subprocess.CalledProcessError:
       print('Skipping this repo ... trouble cloning repo:', repo_name )


# Generate crashes by passing invalid repository names or target directories
try:
    cloneRepo(None, 'target')
except Exception as e:
    crashes.append(f"cloneRepo: {type(e).__name__}: {str(e)}")

try:
    cloneRepo('', 'target')
except Exception as e:
    crashes.append(f"cloneRepo: {type(e).__name__}: {str(e)}")

try:
    cloneRepo('invalid_repo_name', 'target')
except Exception as e:
    crashes.append(f"cloneRepo: {type(e).__name__}: {str(e)}")


def checkPythonFile(path2dir):
    usageCount = 0
    patternDict = ['sklearn', 'h5py', 'gym', 'rl', 'tensorflow', 'keras', 'tf', 'stable_baselines', 'tensorforce', 'rl_coach', 'pyqlearning', 'MAMEToolkit', 'chainer', 'torch', 'chainerrl']
    for root_, dirnames, filenames in os.walk(path2dir):
        for file_ in filenames:
            full_path_file = os.path.join(root_, file_)
            if(os.path.exists(full_path_file)):
                if ((file_.endswith('py')) or (file_.endswith('ipynb')))  :
                    f = open(full_path_file, 'r', encoding='latin-1')
                    pythonFileContent = f.read()
                    pythonFileContent = pythonFileContent.split('\n')
                    pythonFileContent = [z_.lower() for z_ in pythonFileContent if z_!='\n' ]
                    for content_ in pythonFileContent:
                        for item_ in patternDict:
                            if(item_ in content_):
                                usageCount = usageCount + 1
                                print('item_->->->',  content_)
    return usageCount

# Generate crashes by passing invalid directory names
try:
    checkPythonFile(None)
except Exception as e:
    crashes.append(f"checkPythonFile: {type(e).__name__}: {str(e)}")

try:
    checkPythonFile('')
except Exception as e:
    crashes.append(f"checkPythonFile: {type(e).__name__}: {str(e)}")

try:
    checkPythonFile('nonexistent_dir')
except Exception as e:
    crashes.append(f"checkPythonFile: {type(e).__name__}: {str(e)}")


# Print crashes at the end
print("\nCrashes:")
for crash in crashes:
    print(crash)
