$projects = Get-ChildItem -Path "YOUTUBE\Projects" -Directory
foreach ($project in $projects) {
    $name = $project.Name
    Write-Host "Adding README to $name..."
    
    Set-Location $project.FullName
    $readmeContent = @"
# $name (유튜브 영상 프로젝트)

## 프로젝트 소개
이 저장소는 당목담글(DMDG) 유튜브 채널을 위한 영상 제작물 에셋, 썸네일, 대본 및 렌더링 스크립트를 독립적으로 관리하는 서브모듈입니다.

## 파일 구성
- `assets/`: 영상 제작에 필요한 원본 에셋 (이미지, 오디오 등)
- `exports/`: 최종 렌더링된 MP4 영상 파일 및 썸네일
- `narration/`: 나레이션 대본 및 오디오 파일
- 각종 기획 및 리뷰 마크다운 문서들

> **안내**: 본 저장소는 메인 DMDG_UT 시스템에서 자동화된 파이프라인에 의해 렌더링 및 관리를 받습니다.
"@
    
    Set-Content -Path "README.md" -Value $readmeContent -Encoding UTF8
    
    git add README.md
    git commit -m "docs: add README.md for $name"
    git push origin main
    
    Set-Location "..\..\.."
}
