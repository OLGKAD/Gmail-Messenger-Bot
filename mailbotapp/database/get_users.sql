CREATE DEFINER = root@localhost PROCEDURE get_users()
        SELECT * FROM tbl_users;
