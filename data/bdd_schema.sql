
Build
 - uuid
 - account_id
 - create_date
 - finish_date
 - status
 - file_name (uuid+createDate.json)

CREATE TABLE build(
    uuid VARCHAR(255) NOT NULL,
    account_id VARCHAR(255) DEFAULT NULL,
    create_date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    finish_date TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT NULL,
    status INT DEFAULT 0,
    file_name VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY(uuid)
);
