#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo $#
    echo "Usage: $0 label_number data_label prod/stag"
    exit 1
fi

cd /home/indix/ind9/zen

label_number=$1
data_label=$2
cluster_name="test"
rpc_type="nghttp2"
stage=$3

echo "ansible-playbook systems/sherlock/playbooks/sherlock_aws_push.yml -e \
"@systems/sherlock/playbooks/extra_vars/aws/sherlock/${stage}.json" -e data_label=${data_label} -e \
s3_build_path=Sherlock-Native/buildTestAndPublish/buildTestAndPublish/${label_number}.1/target -e \
build_label=$label_number -e cluster=$cluster_name -e rpc_type=$rpc_type --vault-password-file \
/opt/indix-secrets/ansible-vault-password -vvvv" 
ansible-playbook systems/sherlock/playbooks/sherlock_aws_push.yml -e \
"@systems/sherlock/playbooks/extra_vars/aws/sherlock/${stage}.json" -e data_label=${data_label} -e \
s3_build_path=Sherlock-Native/buildTestAndPublish/buildTestAndPublish/${label_number}.1/target -e \
build_label=$label_number -e cluster=$cluster_name -e rpc_type=$rpc_type --vault-password-file \
/opt/indix-secrets/ansible-vault-password -vvvv
cd -
