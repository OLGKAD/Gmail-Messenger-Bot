create table tbl_emails (
        email_id BIGINT UNIQUE AUTO_INCREMENT,
        email_recipient_id BIGINT NULL,
        email_sender_id VARCHAR(45) NULL,
        email_subject TEXT NULL,
        email_sender_name VARCHAR(45) NULL,
        email_text TEXT NULL,
        email_date_time DATETIME NULL,
        email_sent INT NULL,
        email_photo TEXT NULL,
        email_sent_or_received INT NULL,
        email_attachment TEXT  NULL,
        FOREIGN KEY (email_recipient_id)
                REFERENCES tbl_users(user_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        PRIMARY KEY (email_id));
CHARACTER SET utf8 COLLATE utf8_general_ci;
