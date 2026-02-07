import json
import os, subprocess




"""Отримує список імен встановлених додатків через PowerShell"""
# Ця команда повертає список імен програм, які бачить Windows
cmd = 'powershell "Get-StartApps | Select-Object Name | ConvertTo-Json"'

result = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
data = json.loads(result)

print(data)
