#/usr/bin bash

GIT_ZH="https://github.com/openZH/covid_19.git"
GIT_COR_DATA="https://github.com/daenuprobst/covid19-cases-switzerland.git"

if [ -e covid_19 ]; then
	cd covid_19
	git pull
	cd ..
else
	git clone $GIT_ZH
fi

if [ -e covid19-cases-switzerland ]; then
	cd covid19-cases-switzerland
	git pull
	cd ..
else
	git clone $GIT_COR_DATA
fi
