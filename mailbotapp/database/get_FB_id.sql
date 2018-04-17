CREATE DEFINER = root@localhost PROCEDURE get_FB_id(
	IN this_user_id BIGINT
)
        SELECT * FROM tbl_users WHERE user_id = this_user_id;
