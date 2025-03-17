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
./run_test_site.sh
```

On Windows:
```
.\run_test_site.ps1
```

# Adding Users

When the application is first started, there are no users. As some pages
are only accessible if a user has logged in, some users need to be created.
This can be done via the `/register` endpoint. Each user has three properties:

- Username
- Password
- Role

The role can be one of the following (case-insensitive):

- Admin
- Altuser
- User

The role determines which pages are displayed (users with the "Admin" role
see a special dashboard) or accessible.

The sample configuration file, `dast_test_site.yaml`, gives the details of
three users. These users should be given the following roles:

- admin: Admin
- user01: Altuser
- user02: User

The users are stored in a SQLite 3 database, `instance/users.db`. This means
it can be queries using the **sqlite3** command (assuming it is installed):
```
(venv) [ec2-user@ip-172-35-1-122 dast_test_site]$ sqlite3 instance/users.db
SQLite version 3.40.0 2023-06-02 12:56:32
Enter ".help" for usage hints.
sqlite> select * from user;
1|admin|scrypt:32768:8:1$fjfy1bCXqu2ma0aa$4886314740a167272933aa390393c92acdf0c53d5524123f19e3836544a9e32b40b2e23138fb75d8f4cae0ab8cead04812ceebcddf1cf7939954ac6a9094a2d9|admin
2|user01|scrypt:32768:8:1$3i7rCWN2oSSQ1qBT$9467d54843e2febcbdf6a34ad18106fad86bfefea8fff3832937f18d4e03ec82b9d27ac81d783c06f5719cabfd8c89881fd71f684d6d685e8f530b00fd7b4077|altuser
3|user02|scrypt:32768:8:1$xsBvqrfOmJxofLhk$3ce3045ae467229602394306b6bfb3040b566d3c6405a96c70a1f95b740e57e34e2189ec7a9fa02e6dbb1f9f510586d1c4e534fe6e7e84a3bb6ecf4719b06a72|user
sqlite>
```

# Running the DAST CLI

The repository contains a sample configuration file `dast_test_site.yaml`
and a driver script, `run_dast_scan.sh` (PowerShell version to come) that
simplifies running the DAST CLI. You will need to update the URLs in the
configuration file to match your environment. Assuming that you are running
both the Flask application and the DAST CLI on the same server, you should
use the IP address of your server (e.g., the IP address in the file,
172.35.1.122 is that of the AWS EC2 instance in which I have been testing
this).

To use the driver script, you need to set the `API_KEY` environment to your
Checkmarx One API key.

The driver script has three mandatory arguments: the base URL of the Checkmarx
One tenant, which is specified using the `--base-url` command line flag;
the Checkmarx One environment id, which is specified using the
`--environment-id` command line flag; and the location of the configuration
file, which is specified using the `--config` command line flag. Note that
the driver script mounts the current directory on the `/demo` mountpoint so
the configuration file should be prefixed with `/demo/`.

For example:
```
./run_dast_scan.sh --base-url https://anz.ast.checkmarx.net --environment-id f0812034-502f-4431-b758-a3ee5c395ac1 --config /demo/dast_test_site.yaml
```

Other arguments that the DAST CLI accepts can also be passed to the driver
script. For example:
```
./run_dast_scan.sh --base-url https://anz.ast.checkmarx.net --environment-id f0812034-502f-4431-b758-a3ee5c395ac1 --config /demo/dast_test_site.yaml --log-level debug
```
