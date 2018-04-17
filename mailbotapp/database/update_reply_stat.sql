CREATE DEFINER = root@localhost PROCEDURE update_reply_stat()
        UPDATE tbl_replies
        SET reply_sent = 1
        WHERE reply_sent = 0;

