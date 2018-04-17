CREATE DEFINER = root@localhost PROCEDURE get_user_id(
    IN this_FB_id BIGINT
)
        SELECT * FROM tbl_users WHERE user_FB_id = this_FB_id;
