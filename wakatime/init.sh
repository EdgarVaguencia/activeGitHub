This_path="$HOME/activeGitHub"
Current_path="$This_path/wakatime"
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

# Llamada
python script.py --path "$Year/$Month"

# Git
git add "$Year/$Month"
git commit -m 'Dandole atomos :metal:'
git push origin master