CREATE DEFINER = root@localhost PROCEDURE get_unsent_emails()
--	SET @temp = (SELECT * FROM tbl_emails WHERE email_sent = 0);	
--	UPDATE tbl_emails
--	SET email_sent = 1
--	WHERE email_sent = 0;	
--	SELECT @temp;
	SELECT * FROM tbl_emails WHERE email_sent = 0;
