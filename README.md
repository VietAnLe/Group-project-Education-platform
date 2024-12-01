# Group-project-Education-platform
USTH B3 ICT Group project about making an Education platform for English learning and testing


## How to Use 
## How to get the import data from mysql workbench 

1. Download the `Dump20241201` folder.
2. Open MySQL Workbench or your preferred client.
3. For each `.sql` file in the folder, execute it in the `english_learning` database:
   - In MySQL Workbench: Open each `.sql` file and execute.
   - Using the command line:
     ```bash
     mysql -u <username> -p english_learning < <file_name>.sql
     ```

Steps to Verify:
Ensure the Database Exists:

Before running the script, make sure the english_learning database exists. If not, the CREATE DATABASE statement in the script will create it for you.
Alternatively, you can create it manually:

bash
mysql -u <username> -p
CREATE DATABASE english_learning;
Run the Command:

Navigate to the folder where the SQL file is located:
bash

cd 
Execute the script:
bash

mysql -u <username> -p english_learning < english_learning_assignment_images.sql

Confirm Results:
Log in to MySQL and check if the assignment_images table is created and populated:
bash
mysql -u <username> -p
USE english_learning;
SHOW TABLES;
SELECT * FROM assignment_images;

If everything is set up correctly, the mysql command will execute the SQL file and create/insert data as specified in the script. If there are any errors, ensure the database exists and the file paths are correct.
