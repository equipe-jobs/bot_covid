$exclude = @("venv", "Bot_Covid.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "Bot_Covid.zip" -Force