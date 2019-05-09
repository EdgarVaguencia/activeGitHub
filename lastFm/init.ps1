$DocDir = [Environment]::GetFolderPath("MyDocuments")
$CurrentFolder = $DocDir + '\activeGitHub\lastFm'
$Year = Get-Date -UFormat %Y

Set-Location -Path $CurrentFolder

if (!(Test-Path -Path $Year)) {
    New-Item -Path $Year -ItemType Directory
}

# Api
python script.py --path "$Year"

# Git
git add "$Year"
git commit -m "Recomendación musical :headphones:"
