#TMP_DIR=/tmp/openpix/
DST=/home/openpix/openpix/
#ssh ethir "if [ ! -d $TMP_DIR ]; then mkdir $TMP_DIR; fi"
#rsync --recursive . ethir:$TMP_DIR
#ssh root@ethir "rsync --recursive $TMP_DIR $DST; chown -R openpix:wheel $DST"

ssh root@ethir "usermod -s /usr/local/bin/bash openpix"
rsync --recursive . openpix@ethir:$DST
ssh root@ethir "usermod -s /home/openpix/openpix/bin/shell openpix"


