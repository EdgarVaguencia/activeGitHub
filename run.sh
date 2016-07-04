# Path
This_path="$HOME/activeGitHub"
WakatimePath="$This_path/wakatime/init.sh"
WakatimePathScript="$This_path/wakatime/script.py"

# cambiando permisos
chmod +x $WakatimePath
chmod +x $WakatimePathScript

# Se ejecuta cada script según sea requerido
crontab crontab.txt