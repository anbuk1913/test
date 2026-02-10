    https://overfruitfully-nondisinterested-dreama.ngrok-free.dev/
.

    cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"
.

    mysqldump -u root -p database_name table1 table2 table3 > selected_tables.sql
.

Example

    mysqldump -u root -p hospital_db patients doctors appointments > hospital_tables.sql
.

    dir hospital_tables.sql
.

    notepad hospital_tables.sql



