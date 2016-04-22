#!/bin/bash
echo "moving the files with proper suffix"
cd ~/ind9/sherlock/native/build/cluster_runner/sherlock/

mv SherlockMasterNg.out SherlockMasterNg_$1.out
mv SherlockSlaveNg.out SherlockSlaveNg_$1.out

echo "copying the files to s3"
cd ~/explore/s4cmd/

./s4cmd.py put ~/ind9/sherlock/native/build/cluster_runner/sherlock/SherlockMasterNg_$1.out s3://platform-analytics/Sherlock-Native/tempExecutables/
./s4cmd.py put ~/ind9/sherlock/native/build/cluster_runner/sherlock/SherlockSlaveNg_$1.out s3://platform-analytics/Sherlock-Native/tempExecutables/

cd ~/ind9/zen

if [ "$#" -ne 5 ]; then
    echo $#
    echo "Usage: $0 label_number data_label cluster_name rpc_type prod/stag"
    exit 1
fi
echo "ansible-playbook systems/sherlock/playbooks/sherlock_aws_push.yml -e \
"@systems/sherlock/playbooks/extra_vars/aws/sherlock/$5.json" -e data_label=$2 -e \
s3_build_path=Sherlock-Native/buildTestAndPublish/buildTestAndPublish/${1}.1/target -e \
build_label=$1 -e cluster=$3 -e rpc_type=$4 --vault-password-file \
/opt/indix-secrets/ansible-vault-password -vvvv" 
ansible-playbook systems/sherlock/playbooks/sherlock_aws_push.yml -e \
"@systems/sherlock/playbooks/extra_vars/aws/sherlock/$5.json" -e data_label=$2 -e \
s3_build_path=Sherlock-Native/tempExecutables/ -e \
build_label=$1 -e cluster=$3 -e rpc_type=$4 --vault-password-file \
/opt/indix-secrets/ansible-vault-password -vvvv
cd ~/ind9/hackathon/sunrise/scripts
