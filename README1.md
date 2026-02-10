    https://overfruitfully-nondisinterested-dreama.ngrok-free.dev/
.

    cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"
.

    mysqldump -u root -p database_name table1 table2 table3 > selected_tables.sql
.

Example

    mysqldump -u root -p hospital_db patients doctors appointments > hospital_tables.sql
.

    CREATE DATABASE hospital_db;
    
    EXIT;

.

    mysql -u root -p hospital_db < hospital_tables.sql
.

