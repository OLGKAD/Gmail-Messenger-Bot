CREATE DEFINER = root@localhost PROCEDURE get_old_emails (
    IN user_id BIGINT,
    IN sender_id VARCHAR(45)
)
    SELECT * FROM tbl_emails WHERE email_sender_id = sender_id AND email_recipient_id = user_id;
