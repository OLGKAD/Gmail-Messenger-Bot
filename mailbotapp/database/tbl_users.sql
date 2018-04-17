create table tbl_users (
        user_id BIGINT UNIQUE AUTO_INCREMENT,
        user_FB_id BIGINT NULL,
	user_token JSON NOT NULL,
    user_photo TEXT NULL,
    user_name VARCHAR(45),
        PRIMARY KEY (user_id));
CHARACTER SET utf8 COLLATE utf8_general_ci;
