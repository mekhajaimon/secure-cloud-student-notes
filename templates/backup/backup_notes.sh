#!/bin/bash

DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="/home/ubuntu/student-notes-backups"

mkdir -p $BACKUP_DIR

tar -czf $BACKUP_DIR/student_notes_backup_$DATE.tar.gz /home/ubuntu/secure-cloud-student-notes

echo "Backup completed successfully at $DATE"