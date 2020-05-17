#!/usr/bin/env bash

tmp_for_shell_task_1=/tmp/tmp_for_shell_task_1

if  [ -d $tmp_for_shell_task_1 ]; then
rm -rf $tmp_for_shell_task_1
echo Dir $tmp_for_shell_task_1 has been deleted!
fi

mkdir $tmp_for_shell_task_1
echo Dir $tmp_for_shell_task_1 has been created!

cd $tmp_for_shell_task_1
pwd
echo

touch {01..50}.jpg
echo '50 .jpg files have been created!'
dir
echo

echo 'Replacing .jpg to .png'
dir | sed 's:jpg:png:g'
echo

cd -
rm -rf $tmp_for_shell_task_1
echo Dir $tmp_for_shell_task_1 has been deleted!
