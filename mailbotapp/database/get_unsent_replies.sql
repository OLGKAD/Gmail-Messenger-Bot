CREATE DEFINER = root@localhost PROCEDURE get_unsent_replies ()
	SELECT * FROM tbl_replies WHERE reply_sent = 0;
    	
--	UPDATE tbl_replies
--	SET reply_sent = 1
--	WHERE reply_sent = 0;	
