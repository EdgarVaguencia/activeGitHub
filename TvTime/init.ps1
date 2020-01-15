$DocDir = [Environment]::GetFolderPath("MyDocuments")
$CurrentFolder = $DocDir + '\activeGitHub\TvTime'

Set-Location -Path $CurrentFolder

# Api
python script.py

# Git
git add "./series"
git commit -m 'Buenos minutos invertidos :tv:'
