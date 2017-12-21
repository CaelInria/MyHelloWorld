#!/bin/sh
################################################################################
myFile=".results.$$"
hostIP="localhost"
port="8080"
waiting=2
lifetime="2"

echo

# expected result: Welcome! :-))))
echo -n "POST /welcome"
echo -n "                                             ==>    "
http POST $hostIP:$port/welcome > $myFile
cat $myFile
echo
echo

# expected result: {"token":"mon-token"}
echo -n "POST /login(admin, root)"
echo -n "                                  ==>    "
http POST $hostIP:$port/login login=admin pass=root > $myFile
cat $myFile
echo

tokenId1=`grep token $myFile | sed -e 's/{"token":"//' -e 's/"}//'`

echo -n "POST /login(admin, admin)"
echo -n "                                 ==>    "
http POST $hostIP:$port/login login=admin pass=admin > $myFile
cat $myFile
echo

# expected result: {"token":"mon-token"}
echo -n "POST /login(tagada, pouet)"
echo -n "                                ==>    "
http POST $hostIP:$port/login login=tagada pass=pouet > $myFile
cat $myFile
echo

# expected result: {"token":"mon-token"}
echo -n "POST /login(foo, bar)"
echo -n "                                     ==>    "
http POST $hostIP:$port/login login=foo pass=bar > $myFile
cat $myFile
echo

tokenId2=`grep token $myFile | sed -e 's/{"token":"//' -e 's/"}//'`

echo

# expected result: {"result":"2"}
echo -n "POST /compute($tokenId1, \"1 + 1\")"
echo -n "                    ==>    "
http POST $hostIP:$port/compute token="$tokenId1" expression="1 + 1" >$myFile
cat $myFile
echo

# expected result: {"result":" "}
echo -n "POST /compute($tokenId2, \"(1 + 2.2) * 3.14\")"
echo -n "         ==>    "
http POST $hostIP:$port/compute token="$tokenId2" expression="(1 + 2.2) * 3.14" >$myFile
cat $myFile
echo

# expected result: {"result":" "}
echo -n "POST /compute($tokenId1, \"'foo' + 'foo' + 'foo'\")"
echo -n "    ==>    "
http POST $hostIP:$port/compute token="$tokenId1" expression="'foo' + 'foo' + 'foo'" >$myFile
cat $myFile
echo

# expected result: {"result":"True"}
echo -n "POST /compute($tokenId2, \"1 + 1 == 2\")"
echo -n "               ==>    "
http POST $hostIP:$port/compute token="$tokenId2" expression="1 + 1 == 2" > $myFile
cat $myFile
echo

# expected result: {"result":"False"}
echo -n "POST /compute($tokenId1, \"'foo' == 2\")"
echo -n "               ==>    "
http POST $hostIP:$port/compute token="$tokenId1" expression="'foo' == 2" > $myFile
cat $myFile
echo

echo
sleep $waiting

echo -n "POST /setlifetime($tokenId1, 1000)"
echo -n "                   ==>    "
http POST $hostIP:$port/setlifetime token="$tokenId1" value=1000 > $myFile
cat $myFile
echo

# expected result: {"lifetime":"my-lifetime"}
echo -n "POST /setlifetime($tokenId1, $lifetime)"
echo -n "                      ==>    "
http POST $hostIP:$port/setlifetime token="$tokenId1" value=$lifetime > $myFile
cat $myFile
echo

echo

# expected result: {"fault":"has expired"}
echo -n "POST /compute($tokenId1, \"1 + 1 == 2\")"
echo -n "               ==>    "
http POST $hostIP:$port/compute token="$tokenId1" expression="1 + 1 == 2" > $myFile
cat $myFile
echo

# expected result: {"result":" "}
echo -n "POST /compute($tokenId2, \"'foo = ' + str(3.14)\")"
echo -n "     ==>    "
http POST $hostIP:$port/compute token="$tokenId2" expression="'foo = ' + str(3.14)" >$myFile
cat $myFile
echo

# expected result: {"result":" "}
echo -n "POST /compute($tokenId2, \"sqrt(144)\")"
echo -n "                ==>    "
http POST $hostIP:$port/compute token="$tokenId2" expression="sqrt(144)" >$myFile
cat $myFile
echo

# expected result: {"result":"True"}
echo
echo -n "POST /bye"
echo -n "                                                 ==>    "
http POST $hostIP:$port/bye > $myFile
cat $myFile
echo
echo

rm -f $myFile
exit 0
