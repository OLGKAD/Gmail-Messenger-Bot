CREATE DEFINER = root@localhost PROCEDURE user_exists (
        IN FB_id BIGINT
)
        SELECT COUNT(1) FROM tbl_users WHERE user_FB_id = FB_id;                                                                                                                                            
