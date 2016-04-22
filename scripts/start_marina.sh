#!/bin/bash
cd ~/ind9/zen

if [ "$#" -ne 5 ]; then
    echo $#
    echo "Usage: $0 label_number data_label cluster_name rpc_type prod/stag"
    exit 1
fi
echo "ansible-playbook systems/sherlock/playbooks/sherlock_aws_push.yml -e \
"@systems/sherlock/playbooks/extra_vars/aws/marina/$5.json" -e data_label=$2 -e \
s3_build_path=Sherlock-Native/buildTestAndPublish/buildTestAndPublish/${1}.1/target -e \
build_label=$1 -e cluster=$3 -e rpc_type=$4 --vault-password-file \
/opt/indix-secrets/ansible-vault-password -vvvv" 
ansible-playbook systems/sherlock/playbooks/sherlock_aws_push.yml -e \
"@systems/sherlock/playbooks/extra_vars/aws/marina/$5.json" -e data_label=$2 -e \
s3_build_path=Sherlock-Native/buildTestAndPublish/buildTestAndPublish/${1}.1/target -e \
build_label=$1 -e cluster=$3 -e rpc_type=$4 --vault-password-file \
/opt/indix-secrets/ansible-vault-password -vvvv
cd -
