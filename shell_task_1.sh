if  [ -f tmp_for_shell_tasks_private ]; then
rm -rf tmp_for_shell_tasks_private
echo 'Dir "tmp_for_shell_tasks_private" has been deleted!'
fi

mkdir tmp_for_shell_tasks_private
echo 'Dir "tmp_for_shell_tasks_private" has been created!'

cd tmp_for_shell_tasks_private
pwd

touch {01..50}.jpg
echo '50 .jpg files have been created!'
dir

echo 'Replacing .jpg to .png'
dir | sed 's:jpg:png:g'

cd ../
rm -rf tmp_for_shell_tasks_private
echo 'Dir "tmp_for_shell_tasks_private" has been deleted!'
