$projects = @{
    'sodam-pwa' = 'https://github.com/dmdg-official/sodam-pwa.git'
    'museum-pwa' = 'https://github.com/dmdg-official/museum-pwa.git'
    'museum-react' = 'https://github.com/dmdg-official/museum-react.git'
}

foreach ($project in $projects.GetEnumerator()) {
    $name = $project.Name
    $url = $project.Value
    Write-Host "Processing $name..."
    
    git rm -r --cached $name
    
    Set-Location $name
    if (Test-Path ".git") {
        Remove-Item -Recurse -Force ".git"
    }
    git init
    git add .
    git commit -m "Initial commit for $name with updated README"
    git branch -M main
    git remote add origin $url
    git push -u origin main
    
    Set-Location ".."
    Rename-Item $name "${name}_backup" -Force
    git submodule add $url $name
    
    if ($LASTEXITCODE -eq 0) {
        Remove-Item -Recurse -Force "${name}_backup"
    }
}
git commit -m "chore: add web app submodules"
git push
