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
rm -vrf idurtemp
mkdir -p idurtemp
cd idurtemp/
curl -LO #link
chmod a+x idur.py
./idur.py add-repo official-repo #link
./idur.py install idur-stable
cd ..
rm -vrf idurtemp
cd $(basename $0) #not remember
