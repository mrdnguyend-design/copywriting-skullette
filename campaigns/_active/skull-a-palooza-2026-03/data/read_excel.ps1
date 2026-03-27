$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$xl.DisplayAlerts = $false

# File 1
$wb1 = $xl.Workbooks.Open("d:\Skullette - Copywriting\skull-a-palooza\update_gia_day2.xlsx")
$ws1 = $wb1.Worksheets.Item(1)
$csvPath1 = "d:\Skullette - Copywriting\skull-a-palooza\update_gia_day2.csv"
$wb1.SaveAs($csvPath1, 6) # xlCSV = 6
$wb1.Close($false)

# File 2
$wb2 = $xl.Workbooks.Open("d:\Skullette - Copywriting\skull-a-palooza\collection_d2_r1.xlsx")
$ws2 = $wb2.Worksheets.Item(1)
$csvPath2 = "d:\Skullette - Copywriting\skull-a-palooza\collection_d2_r1.csv"
$wb2.SaveAs($csvPath2, 6)
$wb2.Close($false)

$xl.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($xl) | Out-Null
Write-Host "Done - CSVs saved"
