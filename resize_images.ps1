Add-Type -AssemblyName System.Drawing
$portraits = Get-ChildItem -Path "c:\Users\tuesv\Documents\DMDG_UT\.agent\portraits\*.png"
foreach ($file in $portraits) {
    Write-Host "Processing: $($file.Name)"
    $img = [System.Drawing.Image]::FromFile($file.FullName)
    $newWidth = [int]($img.Width / 2)
    $newHeight = [int]($img.Height / 2)
    $bmp = New-Object System.Drawing.Bitmap($newWidth, $newHeight)
    $graph = [System.Drawing.Graphics]::FromImage($bmp)
    $graph.DrawImage($img, 0, 0, $newWidth, $newHeight)
    
    $img.Dispose()
    $graph.Dispose()
    
    $tempPath = $file.FullName + ".tmp"
    $bmp.Save($tempPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
    
    Remove-Item $file.FullName
    Rename-Item $tempPath $file.Name
    Write-Host "Successfully Resized: $($file.Name) to $($newWidth)x$($newHeight)"
}
