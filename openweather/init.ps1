$DocDir = [Environment]::GetFolderPath("MyDocuments")
$CurrentFolder = $DocDir + '\activeGitHub\openweather'
$Year = Get-Date -UFormat %Y
$Month = Get-Date -UFormat %m

Set-Location -Path $CurrentFolder

if (!(Test-Path -Path $Year)) {
  New-Item -Path $Year -ItemType Directory
}

if (!(Test-Path -Path "${Year}\\${Month}")) {
  New-Item -Path "$Year\$Month" -ItemType Directory
}

# Api
python script.py --path "$Year/$Month"

# Git
git add "$Year/$Month"
git commit -m "Actualizando el clima :partly_sunny:"
