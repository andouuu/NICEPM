# password Management System 3000

Before you can use the these apps, make sure you have the requirements installed:  
Windows: `py -m pip install -r requirements.txt`  
Linux: `python3 -m pip install -r requirements.txt`

Also, you have to run "create_db.py" once before running any of the apps.
This will create the database and populate it with some example data.

So, as a checklist, the first time you should:
1. Unzip the .ZIP-archive to an empty directory
2. Go to the directory on the commandline (`cd <dir-name>`)
3. Install a Python Virtual Environment:  
   Windows: `py -m venv .venv`  
   Linux: `python3 -m venv .venv`
4. Activate the VEnv:  
   Windows: `.\.venv\Scripts\activate`  
   Linux: `./.venv/Scripts/activate`
5. Install requirements in the VEnv:  
   Windows: `py -m pip install -r requirements.txt`  
   Linux: `python3 -m pip install -r requirements.txt`
6. Run the create_db script:  
   Windows: `py .\create_db.py`  
   Linux: `python3 ./create_db.py`
7. Start the API server:  
   Windows: `py .\student_api.py`  
   Linux: `python3 ./student_api.py`
   
The steps above only need to be executed once.
After that, you can start the students api server by doing the following:

1. Go to the directory on the commandline (`cd <dir-name>`)
2. Activate the VEnv:  
   Windows: `.\.venv\Scripts\activate`  
   Linux: `./.venv/Scripts/activate`
3. And finally, start the API server:  
   Windows: `py .\students.py`  
   Linux: `python3 ./students.py`

After that, you can start the frontend website with:  
Windows: `py .\student_frontend.py`  
Linux: `python3 ./student_frontend.py`

Or you can try out the commandline (CLI) tool with:  
Windows: `py .\student_cli.py`  
Linux: `python ./student_cli.py`

There's lots of room for improvement in the application, like:
- adding exception handling,
- making sure the templates and routes adhere to best practices,
- adding functionality for courses and grades,
- spice up the layout and design,
- adding useful comments and doc-strings,
- etc, etc.

Have fun!
