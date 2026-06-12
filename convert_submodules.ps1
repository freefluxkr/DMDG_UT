$projects = @{
    'Hangeul_Meadow' = 'https://github.com/dmdg-official/DMDG_UT_Hangeul_Meadow.git'
    'SadoSeja' = 'https://github.com/dmdg-official/DMDG_UT_SadoSeja.git'
    'Subway_Smell' = 'https://github.com/dmdg-official/DMDG_UT_Subway_Smell.git'
}

foreach ($project in $projects.GetEnumerator()) {
    $name = $project.Name
    $url = $project.Value
    Write-Host "Processing $name..."
    
    git rm -r --cached "YOUTUBE/Projects/$name"
    
    Set-Location "YOUTUBE/Projects/$name"
    git init
    git add .
    git commit -m "Initial commit for $name"
    git branch -M main
    git remote add origin $url
    git push -u origin main
    
    Set-Location "../../../"
    Rename-Item "YOUTUBE/Projects/$name" "YOUTUBE/Projects/${name}_backup" -Force
    git submodule add $url "YOUTUBE/Projects/$name"
    
    if ($LASTEXITCODE -eq 0) {
        Remove-Item -Recurse -Force "YOUTUBE/Projects/${name}_backup"
    }
}
git commit -m "chore: add last 3 submodules"
git push
