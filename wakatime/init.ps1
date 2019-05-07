$DocDir = [Environment]::GetFolderPath("MyDocuments")
$CurrentFolder = $DocDir + '\activeGitHub\wakatime'
$Year = Get-Date -UFormat %Y
$Month = Get-Date -UFormat %m

Set-Location -Path $CurrentFolder

if (!(Test-Path -Path $Year)) {
  New-Item -Path $Year -ItemType Directory
}

if (!(Test-Path -Path "${Year}\\${Month}")) {
  New-Item -Path "$Year\$Month" -ItemType Directory
}

python script.py --path "$Year/$Month"
