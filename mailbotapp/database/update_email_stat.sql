CREATE DEFINER = root@localhost PROCEDURE update_email_stat()
	UPDATE tbl_emails
        SET email_sent = 1
        WHERE email_sent = 0; 
