# StudentScoreManager
SQL Project

## Installation 
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.
From current directory in terminal, run the following command:
```bash
pip install -r requirements.txt
```

Install [MariaDB](https://mariadb.com/get-started-with-mariadb/)

## Database Configuration
1. Create .env file in the root directory of the project. This file will contain the environment variables needed for the database connection. You can create it by copying the default.env file and renaming it to .env.
   ```bash
   cp default.env .env
   ```
   or on Windows:
   ```bash
   copy default.env .env
   ```
   or manually create a new file named `.env` in the root directory of the project.
   
2. Configure the .env file following the default.env file. You can use the default.env file as a template by copying it and renaming it to .env.
3. Make sure to set the correct values for the following variables in the .env file:
   - DB_HOST: The host address of your MariaDB server (e.g., localhost).
   - DB_PORT: The port number on which your MariaDB server is running (default is 3306).
   - DB_USER: The username to connect to the database.
   - DB_PASSWORD: The password for the specified user.
   - DB_NAME: The name of the database you want to use.


## Usage
Run backend server:
```bash
fastapi dev src/main.py
```

Open another terminal window and run  frontend server by following command:

### In Command Prompt:
```bash
"frontend\index.html"
```

### In Powershell:
```bash
start frontend\index.html
```

### In Linux:
Use any browser to open the file `frontend/index.html`
```bash
xdg-open frontend/index.html
```
Note: Make sure to replace `xdg-open` with the appropriate command for your Linux distribution if necessary.

### In MacOS:
```bash
open frontend/index.html
``` 

## Contributors
Vo Thanh Nhan - 230322\
Nguyen Khoi Nguyen - 230320