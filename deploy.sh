#!/bin/bash
command -v aws >/dev/null 2>&1 || { echo "First, install the AWS CLI: python -m pip install --upgrade awscli." >&2; exit 1; }

app=projectbase
user=$(aws iam get-user | python -m json.tool | fgrep UserName | cut -d'"' -f 4)
email=${user}@1ticket.com
log_streamer_arn="/dti1ticket/logging/logstream_arn"
create_log_group=true


template=template.yaml
swagger=swagger.yaml
use_previous_value=true
user=$(echo $email| cut -d'@' -f 1)
stage=${1:-dev-$user}


latest_version=$(date -u "+%Y-%m-%dT%H%M%SZ")
if [[ "$stage" == *dev* ]]; then
    stack=${app}-${user}
    version=$latest_version
    env_type=dev
    code_bucket=etix-releases-dev
    export AWS_PROFILE=1ticketdev
    export AWS_DEFAULT_PROFILE=1ticketdev
else
    stack=${app}
    email=devops@1ticket.com
    version=$(git describe --tags 2> /dev/null) || $latest_version
    env_type=prod
    code_bucket=dti1ticket-releases
    export AWS_PROFILE=dti1ticketprod
    export AWS_DEFAULT_PROFILE=dti1ticketprod
fi
release=${stack}-${version}
release_swagger=swagger-${release}.yaml
aws_profile=${AWS_PROFILE:-default}
aws_region=${AWS_DEFAULT_REGION:-us-east-1}
aws_account_id=$(aws sts get-caller-identity --output text --query 'Account')
code=$app

echo "Creating ${release_swagger}..."
sed -e "s/<<region>>/$aws_region/g" \
    -e "s/<<accountId>>/$aws_account_id/g" \
    -e "s/<<service>>/$app/g" \
    -e "s/<<stage>>/$stage/g" \
    -e "s/<<stack>>/$stack/g" \
    < $swagger > $release_swagger
aws s3 cp ${release_swagger} s3://${code_bucket}/
rm $release_swagger

echo "Packaging ${release}..."
rm -rf $release
mkdir $release
if [ -d vendored ]; then
    for package in vendored/*.zip
    do
        unzip -d $release -q -o -u $package
    done
fi
cp -R $code $release
cd $release
zip -rq9 ${release}.zip *
aws s3 cp ${release}.zip s3://${code_bucket}/
cd ..
rm -rf $release
echo $aws_profile
echo "Deploying $version to ${stack}..."
aws cloudformation deploy \
    --region $aws_region \
    --profile $aws_profile \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides ServiceName=$app \
                          StageName=$stage \
                          CodeBucketName=$code_bucket \
                          CodeKey=${release}.zip \
                          EnvironmentType=${env_type} \
                          SupportEmail=support@1ticket.com \
                          SwaggerKey=${release_swagger} \
                          NotificationEmail=${email} \
                          LogStreamerArn="${log_streamer_arn}" \
                          CreateLogGroup=${create_log_group} \
    --stack-name $stack \
    --template-file $template \
    --tags app-name=$stack

echo "Describing..."
aws cloudformation describe-stacks \
    --region $aws_region \
    --profile $aws_profile \
    --stack-name ${stack} \
| python -m json.tool

echo ""
echo "Have a great day."
echo ""
