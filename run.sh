# Path
This_path="$HOME/activeGitHub"
WakatimePath="$This_path/wakatime/init.sh"
WakatimePathScript="$This_path/wakatime/script.py"
OpenWeatherPath="$This_path/openweather/init.sh"
OpenWeatherPathScript="$This_path/openweather/script.py"
LastFmPath="$This_path/lastFm/init.sh"
LastFmPathScript="$This_path/lastFm/script.py"
GasolinazoPath="$This_path/gasolinazo/init.sh"
GasolinazoPathScript="$This_path/gasolinazo/script.py"

# cambiando permisos
chmod +x $WakatimePath
chmod +x $WakatimePathScript
chmod +x $OpenWeatherPath
chmod +x $OpenWeatherPathScript
chmod +x $LastFmPath
chmod +x $LastFmPathScript
chmod +x $GasolinazoPath
chmod +x $GasolinazoPathScript

# Se ejecuta cada script según sea requerido
crontab crontab.txt
