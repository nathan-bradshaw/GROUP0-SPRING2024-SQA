# Applied Techniques:

# 1: Git Hooks for reporting all security weaknesses upon any commit:
What we did:
- Created a git hook named pre-commit which runs everytime the user attempts to commit to github
- Edited that hook to run bandit security checks recursivelly on all files
- We then output that security report to security_report.csv in our repository and inform the user that security vulnerabilities were found
- We also created a script to install the hooks on a new github repo user's machine due to the fact that hooks are not tracked in repositories
- That pre-commit hook can be found in the git_hooks folder, and the script is called setup-hooks-sh

Results:
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

What we learned:
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
# WHAT WE DID
# RESULTS
# WHAT WE LEARNED

# 3: Integrated forensics by modifying 5 methods:
# WHAT WE DID
# RESULTS
# WHAT WE LEARNED

# 4: Integrated CI with GitHub Actions:
# WHAT WE DID
What we did:
- We created a continuous integration .yaml file that is triggered by pushes to the main branch
- Defined a single job called "build" that which runs on the latest version of ubuntu
- The steps include a checkout of the repository, an installation of project dependencies, and an execution of any tests

# RESULTS
# WHAT WE LEARNED
