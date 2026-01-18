# auto-push.ps1 - Avtomatik Git Push Skripti

Write-Host "Git o'zgarishlarini tekshiryapman..." -ForegroundColor Cyan

# O'zgarishlarni ko'rsatish
git status

# Barcha o'zgarishlarni qo'shish
Write-Host "`nBarcha o'zgarishlarni qo'shyapman..." -ForegroundColor Yellow
git add .

# Commit xabarini so'rash
$commitMessage = Read-Host "Commit xabarini kiriting"

if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Update: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
}

# Commit yaratish
Write-Host "`nCommit yaratilmoqda..." -ForegroundColor Yellow
git commit -m $commitMessage

# Push qilish
Write-Host "`nPush qilinmoqda..." -ForegroundColor Yellow
git push origin main

Write-Host "`n✅ Bajarildi!" -ForegroundColor Green
