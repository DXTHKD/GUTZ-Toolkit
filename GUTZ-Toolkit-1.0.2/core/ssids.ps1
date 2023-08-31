$WirelessSSIDs = (netsh wlan show profiles | Select-String ': ' ) -replace ".*:\s+"
$WifiInfo = foreach($SSID in $WirelessSSIDs) {
    $Password = (netsh wlan show profiles name=$SSID key=clear | Select-String 'Key Content') -replace ".*:\s+"
    [PSCustomObject]@{"SSID"=$SSID;"Password"=$Password}
}  
$WifiInfo | ConvertTo-Json -Depth 2
Write-Output ""
Write-Output " Press any key to go back"
Read-Host