-- Keep a restored copy away from the backup server: it would upload its own
-- dump there and then delete the oldest real backups during cleanup. The
-- host is cleared as well as the password because a private key file
-- authenticates without it.
UPDATE db_backup
   SET sftp_host = NULL,
       sftp_password = NULL;
