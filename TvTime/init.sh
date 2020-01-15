This_path="$HOME/activeGitHub"
Current_path="$This_path/TvTime"

cd $Current_path

python script.py

git add "./series"
git commit -m 'Buenos minutos invertidos :tv:'
git push origin master
