This_path="$HOME/activeGitHub"
Current_path="$This_path/openweather"
Year=`date +"%Y"`
Month=`date +"%m"`

cd $Current_path

if [ ! -d "$Year" ]
then
  mkdir $Year
fi

if [ ! -d "$Year/$Month" ]
then
  mkdir $Year/$Month
fi

python script.py --path "$Year/$Month"

# Git
git add "$year/$Month"
git commit -m "Actualizando el clima :partly_sunny:"
git push origin master
