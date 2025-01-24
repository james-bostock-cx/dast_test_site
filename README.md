# Introduction

This repository contains a simple Python web application for testing
the Checkmarx One DAST engine. The site is simple but has a few
features that make it interesting:

- Different pages are accessible depending on a) whether a user is
  logged in; and b) the user’s role.
- There are two login screens. At present, they are functionally
  equivalent. The second one exists purely because the Zap context
  only allows a single login URL.

# Running the Application

## Creating a Virtual Environment

To avoid needlessly pollution the system Python installation, it is
recommended to create a virtual environment.

On Linux:
```
python3 -m py venv venv
```

On Windows:
```
py -m venv venv
```

Both commands will cause a `venv` folder to be created containing the
virtual environment.

## Activating the Virtual Environment

On Linux (assuming the shell is bash):
```
source venv/bin/activate
```

On Windows (assuming the shell is PowerShell):
```
.\venv\Scripts\activate.ps1
```

## Installing the Dependencies

The **pip** command can be used to install the third-party dependencies:
```
pip install -r requirements.txt
```

## Running the Application

Bash and PowerShell scripts are provided to simplify running the application.

On Linux:
```
./run.sh
```

On Windows:
```
.\run.ps1
```
