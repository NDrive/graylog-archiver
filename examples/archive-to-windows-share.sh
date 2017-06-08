#!/bin/bash

#
# 1. you'll need cifs-utils for using this script
#    to install on Ubuntu run: apt-get update && apt-get install cifs-utils
# 2. all output redirected to log file
# 3. tested with Ubuntu 14 LTS and Windows Server 2012 R2 (file share)
# 4. use it on your own risk!
#

# local variables
ES_USER=graylog
ES_GROUP=graylog
ES_REPO_PATH=/data/backups/elasticsearch
GRAYLOG_ARCHIVER_CONFIG=/opt/graylog-archiver/conf/graylog_archiver.json
GRAYLOG_ARCHIVER_LOG=/var/log/graylog-archiver.log

# remote variables
REMOTE_BACKUP_DIR=//windows_server/backup_share/graylog
REMOTE_BACKUP_DIR_USER=graylog
REMOTE_BACKUP_DIR_DOMAIN=domain.local
REMOTE_BACKUP_DIR_PASSWORD=change-this-password

# make dirs for backup
mkdir -p $ES_REPO_PATH >> $GRAYLOG_ARCHIVER_LOG 2>&1

# mount remote share
mount -t cifs -o username=${REMOTE_BACKUP_DIR_USER},domain=${REMOTE_BACKUP_DIR_DOMAIN},password=${REMOTE_BACKUP_DIR_PASSWORD},uid=${ES_USER},gid=${ES_GROUP} ${REMOTE_BACKUP_DIR} $ES_REPO_PATH >> $GRAYLOG_ARCHIVER_LOG 2>&1

# backup graylog app
graylog-archiver -c $GRAYLOG_ARCHIVER_CONFIG >> $GRAYLOG_ARCHIVER_LOG 2>&1

# umount remote share
umount $ES_REPO_PATH >> $GRAYLOG_ARCHIVER_LOG 2>&1
