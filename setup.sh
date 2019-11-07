#!/bin/bash

read -p 'Email account : ' email_acc
email_regex="^[a-z0-9!#\$%&'*+/=?^_\`{|}~-]+(\.[a-z0-9!#$%&'*+/=?^_\`{|}~-]+)*@([a-z0-9]([a-z0-9-]*[a-z0-9])?\.)+[a-z0-9]([a-z0-9-]*[a-z0-9])?\$"
if [[ ! ${email_acc} =~ ${email_regex} ]] ; then
    echo "email format is not valid"
    exit 1
fi

read -sp 'Email password :'  email_pass
echo  ""

read -p '591 url : ' url
url_regex="^(https://)?rent.591.com.tw.*"
if [[ ! ${url} =~ ${url_regex} ]] ; then
    echo "591 url is not valid"
    exit 1
fi
if [[ ! ${url} =~ "^https" ]]; then
    url="https://"${url}
fi

read  -p 'Chrome webdirver directory (default /usr/local/bin/) : '  driver_dir
driver_dir=${driver_dir:-/usr/local/bin/}
${driver_dir}=${driver_dir}'/chromedriver'

# output config file
rm ./config.json && touch ./config.json
echo "{" >> ./config.json
echo "    \"591_url\" : \"${url}\","  >> ./config.json
echo "    \"email_acc\" : \"${email_acc}\"," >> ./config.json
echo "    \"email_pass\" : \"${email_pass}\"," >> ./config.json
echo "    \"smtp_server\" : \"smtp.gmail.com:587\",  " >> ./config.json
echo "    \"default_driver_dir\" : \"/usr/local/bin/chromedriver\"  " >> ./config.json
echo "}" >> ./config.json

cat ./config.json

docker run -it -w /usr/workspace -v $(pwd):/usr/workspace joyzoursky/python-chromedriver:3.7-selenium python notifier.py
