CREATE DEFINER = root@localhost PROCEDURE get_email(
        IN this_email_id BIGINT
)
        SELECT * FROM tbl_emails WHERE email_id = this_email_id;
