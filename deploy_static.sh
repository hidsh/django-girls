if [ $API_TOKEN ]; then
	cp -a blog/static .
	echo 'copied: blog/static --> /static'
else
	echo 'Do nothing (Not required at development)'
fi
