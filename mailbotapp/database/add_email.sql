CREATE DEFINER = root@localhost PROCEDURE add_email (
    IN recipient_id BIGINT,
    IN sender_id VARCHAR(45),
	IN subject TEXT,
	IN sender_name VARCHAR(45),
	IN text TEXT,
	IN date_time DATETIME,
	IN sent INT,
    IN photo TEXT, 
    IN sent_or_received INT,
    IN attachment TEXT
)
        insert into tbl_emails
        (
		email_recipient_id,
		email_sender_id,
		email_subject,
		email_sender_name,
    	email_text,
		email_date_time,
		email_sent,
		email_photo,
        email_sent_or_received, 
        email_attachment
        )
        values
	    (
		recipient_id,
		sender_id,
		subject,
		sender_name,
		text,
		date_time,
		sent,
		photo,
        sent_or_received, 
        attachment
        );
    
