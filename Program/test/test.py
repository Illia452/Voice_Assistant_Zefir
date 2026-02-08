import json
import subprocess


cmd = 'powershell "Get-StartApps | Select-Object Name | ConvertTo-Json"'
result = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
data = json.loads(result)

print(data)