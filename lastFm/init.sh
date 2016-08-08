This_path="$HOME/activeGitHub"
Current_path="$This_path/lastFm"
Year=`date +"%Y"`
Month=`date +"%m"`

cd $Current_path

if [ ! -d "$Year" ]
then
  mkdir $Year
fi

python script.py --path "$Year"

# Git
git add "$Year/$Month"
git commit -m "Recomendación musical :headphones:"
git push origin master
