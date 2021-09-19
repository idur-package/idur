#/usr/bin/bash
# test
if [ ! $(whoami) = "root" ]
then
    echo "you need root"
    exit
fi
if [ ! -f "/usr/bin/apt" ]
then
    echo "idur works only on debian"
    exit
fi

apt install -y git curl python3 bash coreutils

cd /tmp/
rm -vrf idurtmp
mkdir -p idurtmp
cd idurtmp/
curl -LO https://raw.githubusercontent.com/idur-package/idur/v0.1.2/src/idur.py
chmod a+x idur.py
./idur.py add-repo official-repo https://github.com/idur-package/official-repo
./idur.py install idur-stable
cd ..
rm -vrf idurtmp/
