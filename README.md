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

# Running the DAST CLI

The repository contains a sample configuration file `dast_test_site.yaml`
and a driver script, `dast_test_site.sh` (PowerShell version to come) that
simplifies running the DAST CLI. You will need to update the URLs in the
configuration file to match your environment. Assuming that you are running
both the Flask application and the DAST CLI on the same server, you should
use the IP address of your server (e.g., the IP address in the file,
172.35.1.122 is that of the AWS EC2 instance in which I have been testing
this).

To use the driver script, you need to set the `API_KEY` environment to your
Checkmarx One API key.

The driver script has one mandatory argument: the Checkmarx One environment
id, which is specified using the `--environment-id` command line argument.
For example:
```
./dast_test_site.sh --environment-id f0812034-502f-4431-b758-a3ee5c395ac1
```

Other arguments that the DAST CLI accepts can also be passed to the driver
script. For example:
```
./dast_test_site.sh --environment-id f0812034-502f-4431-b758-a3ee5c395ac1 --log-level debug
```
