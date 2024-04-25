# Applied Techniques:

# 1: Git Hooks for reporting all security weaknesses upon any commit:
## What we did:
- Created a git hook named pre-commit which runs everytime the user attempts to commit to github
- Edited that hook to run bandit security checks recursivelly on all files
- We then output that security report to security_report.csv in our repository and inform the user that security vulnerabilities were found
- We also created a script to install the hooks on a new github repo user's machine due to the fact that hooks are not tracked in repositories
- That pre-commit hook can be found in the git_hooks folder, and the script is called setup-hooks-sh

## Results:
- We successfully created a hook to report bandit vulnerabilities upon commiting 
- Our bandit output includes the following issues:
1. blacklist : empirical/dataset.stats.py line 12
1. start_process_with_partial_path : empirical/dataset.stats.py line 59
1. subprocess_without_shell_equals_true : empirical/dataset.stats.py line 59
1. blacklist : mining/git.repo.miner.py line 10
1. blacklist : mining/git.repo.miner.py line 15
1. start_process_with_partial_path : mining/git.repo.miner.py line 37
1. subprocess_without_shell_equals_true : mining/git.repo.miner.py line 37
1. blacklist : mining/mining.py line 7
1. start_process_with_partial_path : mining/mining.py line 43
1. subprocess_without_shell_equals_true : mining/mining.py line 43
1. start_process_with_partial_path : mining/mining.py line 81
1. subprocess_without_shell_equals_true : mining/mining.py line 81

## What we learned:
- We learned that a few of our files have security issues that need to be addressed:
1. empirical/dataset.stats.py
1. mining/git.repo.miner.py
1. mining/mining.py

- These files have issues with the following descriptions:
1. Consider possible security implications associated with the subprocess module.
1. Starting a process with a partial executable path
1. subprocess call - check for execution of untrusted input.
1. Using minidom to parse untrusted XML data is known to be vulnerable to XML attacks. Replace minidom with the equivalent defusedxml package, or make sure defusedxml.defuse_stdlib() is called.

- To ensure our code base cannot be attacked or used maliciously, we would need to address these concerns and use more secure processes to run the desired code
- Git hooks can be used to ensure that everytime new code is commited, we can track and identify new security issues that need to be addressed



# 2: Created a Fuzz file to Fuzz 5 methods:
## What we did:
- We selected 5 methods from the MLForensics-farzana repository to implement fuzz testing in order to find bugs and vulnerabilities.
- We created a python script named fuzz.py in our repository in order to automate the testing with invalid inputs and to print the exceptions.

1. deleteRepo(dirName, type_): Inputs - `None`, Empty string (''), Nonexistent directory name ('nonexistent_dir')
2. dumpContentIntoFile(strP, fileP): Inputs - 'test' (content) and `None`, 'test' (content) and Empty string ('') (file path)
3. makeChunks(the_list, size_): Inputs - List `[1, 2, 3]` (the_list) and Size 0 (size_)
4. cloneRepo(repo_name, target_dir): Inputs - `None`, Empty string (''), 'invalid_repo_name' (repo_name) and 'target' (target_dir)
5. checkPythonFile(path2dir): Inputs - `None`, Empty string (''), Nonexistent directory ('nonexistent_dir')

- We set up GitHub Actions to run fuzz.py automatically when there is a push into the main branch. 

fuzz.yml:
name: Fuzz Testing

on:
  push:
    branches:
      - main

jobs:
  fuzz:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'

    - name: Run fuzz.py
      run: python fuzz.py


## Results:
- The GitHub is able to correctly run fuzz.py and here are is the output:

-> Run python fuzz.py
fatal: repository 'target' does not exist
fatal: repository 'invalid_repo_name' does not exist
:::INVALID_DIRECTORY_NAME:::Deleting  None
:::EMPTY_DIRECTORY_NAME:::Deleting  
:::NONEXISTENT_DIRECTORY:::Deleting  nonexistent_dir
Skipping this repo ... trouble cloning repo: 
Skipping this repo ... trouble cloning repo: invalid_repo_name

Crashes:
deleteRepo: TypeError: stat: path should be string, bytes, os.PathLike or integer, not NoneType
dumpContentIntoFile: TypeError: expected str, bytes or os.PathLike object, not NoneType
dumpContentIntoFile: FileNotFoundError: [Errno 2] No such file or directory: ''
makeChunks: ValueError: range() arg 3 must not be zero
cloneRepo: TypeError: can only concatenate str (not "NoneType") to str
checkPythonFile: TypeError: expected str, bytes or os.PathLike object, not NoneType

## What we learned
1. Repository Existence Verification: Encountered fatal errors when attempting to clone repositories 'target' and 'invalid_repo_name' that did not exist.
2. Handling of Invalid Directory Names: Detected and handled cases where invalid directory names (None, empty string, nonexistent directories) were provided as inputs.
3. Error Handling in File Operations: Discovered errors in file operations, such as writing content to files with invalid paths (resulting in FileNotFoundError) and passing None as the file path.
4. Encountered a TypeError when attempting to concatenate a NoneType object to a string during repository cloning.
5. Chunk Size Handling: Encountered a ValueError when attempting to create chunks with an invalid size (0), indicating a flaw in the chunking mechanism.
6. Python File Content Verification: Detected TypeError instances when passing invalid directory names to the function responsible for checking Python file content, highlighting the need for robust directory input handling.

## Lessons:
1. We identified vulnerabilities, errors, and crashes within the project's codebase through fuzz testing
2. We recommend improvements to enhance the robustness, reliability, and security of the project
3. We recognize the importance of implementing robust error handling mechanisms and improving input validation to prevent unexpected issues during execution

# 3: Integrated forensics by modifying 5 methods:
## What we did:
1. Added a file called myLogger.py to the repository.
2. Used the method giveMeLoggingObject to integrate forensics in the following 5 methods:
    * runFameML in main.py
    * getCSVData in main.py
    * dumpContentIntoFile in mining.py
    * reportDensity in report.py
    * reportProp in report.py
3. Ran the above methods in order to write logging messages to the SIMPLE-LOGGER.log files

## Results
The 3 log files generated from the 5 altered methods can be found in the empirical, FAME-ML, and mining directories. The log is called SIMPLE-LOGGER in each.

## What we learned:
- Learned how to make use of logging in order to conduct software forensics in python code.
- Gained experience using the standard python logging library.
- Achieved a general understanding of logging levels and how they can be used to control the verbosity of logging output.
- Discovered the importance of including contextual information such as timestamps and method names in log messages.
- Appreciated the role of logging in providing a historical record of events and actions within the software.

# 4: Integrated CI with GitHub Actions:
## What we did:
- We created a continuous integration .yaml file that is triggered by pushes to the main branch
- Defined a single job called "build" that which runs on the latest version of ubuntu
- The steps include a checkout of the repository and an installation of project dependencies

## Results:
- The build successfully runs and the following run details are output in actions:

- Checkout Repository
1. Run actions/checkout@v2
1. Syncing repository: nathan-bradshaw/GROUP0-SPRING2024-SQA
1. Getting Git version info
1. Temporarily overriding HOME='/home/runner/work/_temp/91278238-ff76-434a-9396-c0352ba508fe' before making global git config changes
1. Adding repository directory to the temporary git global config as a safe directory
1. /usr/bin/git config --global --add safe.directory /home/runner/work/GROUP0-SPRING2024-SQA/GROUP0-SPRING2024-SQA
1. Deleting the contents of '/home/runner/work/GROUP0-SPRING2024-SQA/GROUP0-SPRING2024-SQA'
1. Initializing the repository
1. Disabling automatic garbage collection
1. Setting up auth
1. Fetching the repository
1. Determining the checkout info
1. Checking out the ref
1. /usr/bin/git log -1 --format='%H'
1. 'cceb79cf90b8e5a103dd5cadb3e20294f5fbb063'

- Set up Python
1. Run actions/setup-python@v2
1. Successfully setup CPython (3.12.2)

- Install Dependencies
1. Run python -m pip install --upgrade pip
1. Requirement already satisfied: pip in /opt/hostedtoolcache/Python/3.12.2/x64/lib/python3.12/site-packages (24.0)

- Post Set up Python
1. Post job cleanup.

- Post Checkout Repository
1. Post job cleanup.
1. /usr/bin/git version
1. git version 2.43.2
1. Temporarily overriding HOME='/home/runner/work/_temp/f7f78543-b06c-43c2-a9e2-1473001b9d38' before making global git config changes
1. Adding repository directory to the temporary git global config as a safe directory
1. /usr/bin/git config --global --add safe.directory /home/runner/work/GROUP0-SPRING2024-SQA/GROUP0-SPRING2024-SQA
1. /usr/bin/git config --local --name-only --get-regexp core\.sshCommand
1. /usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
1. /usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
1. http.https://github.com/.extraheader
1. /usr/bin/git config --local --unset-all http.https://github.com/.extraheader
1. /usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"

-Complete Job
1. Clean up orphan processes

## What We Learned
- We gained an understanding of how to integrate CI workflows with YAML files 
- Learned how to perform common tasks such as fetching code from the repository and setting up your local environment
- Learned how to utilize the actions tab of GitHub to monitor different configurations
- Overall, we learned how to automate certain processes for our project using CI with GitHub Actions that lead to more efficiency and reliability
