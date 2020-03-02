
DIR=`pyenv prefix`/lib/python3.8/site-packages

upload_func () {
    local FUNC=$1
	AWS_PAGER="" aws --profile $BOTO3PROF --output yaml \
        lambda update-function-code  \
        --function-name $FUNC --zip-file fileb://$FUNC.zip
}

zip_func () {
    local FUNC=$1
    rm -f $FUNC.zip
    zip -r9 -q $FUNC.zip *
}

cp lambda_function.py $DIR
pushd $DIR
zip_func testLambda
upload_func testLambda
popd

