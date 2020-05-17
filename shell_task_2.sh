backup=/tmp/backup
ref_path=/etc

if [ -d $backup ]; then
rm -rf $backup
echo Dir $backup has been deleted!
fi

mkdir $backup
echo Dir $backup has been created!

cp $ref_path/*.conf $backup
echo Backup files were copied to $backup from $ref_path!

diff='Little difference!'

for config in pacman.conf resolv.conf
do

echo $diff >> $backup/$config
echo
echo --------COMPARISON $config--------------
diff -y $ref_path/$config $backup/$config
echo --------END of COMPARISON---------------
echo REFERENCE $config:
find $ref_path -maxdepth 1 -name $config
echo

done

rm -rf $backup
echo Dir $backup has been deleted!