
file="classes.py"

if [ -f $file ] ; then
    rm $file
fi

pushd ../DB/Utils
ls
./class_creation.sh $1 $2
cp classes.py ../../PeeWeeController
rm classes.py
popd

