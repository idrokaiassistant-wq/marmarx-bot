# auto-push.ps1 - Avtomatik Git Push Skripti

Write-Host "Git o'zgarishlarini tekshiryapman..." -ForegroundColor Cyan

# O'zgarishlarni ko'rsatish
git status

# Barcha o'zgarishlarni qo'shish
Write-Host "`nBarcha o'zgarishlarni qo'shyapman..." -ForegroundColor Yellow
git add .

# Commit xabarini so'rash
Write-Host "`nCommit xabarini kiriting (faqat matn, git komandalar emas):" -ForegroundColor Cyan
$commitMessage = Read-Host "Commit xabari"

if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Update: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
}

# Git komandalarni olib tashlash agar kiritsa
$commitMessage = $commitMessage -replace 'git\s+(add|commit|push|status).*', ''
$commitMessage = $commitMessage -replace '&&.*', ''
$commitMessage = $commitMessage.Trim()

if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Update: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
}

# Commit yaratish
Write-Host "`nCommit yaratilmoqda..." -ForegroundColor Yellow
$commitResult = git commit -m "$commitMessage" 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Xato: Commit qilinmadi!" -ForegroundColor Red
    Write-Host $commitResult -ForegroundColor Red
    Write-Host "`nIltimos, qaytadan urinib ko'ring." -ForegroundColor Yellow
    exit 1
}

# Push qilish
Write-Host "`nPush qilinmoqda..." -ForegroundColor Yellow
$pushResult = git push origin main 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Xato: Push qilinmadi!" -ForegroundColor Red
    Write-Host $pushResult -ForegroundColor Red
    Write-Host "`nIltimos, qaytadan urinib ko'ring." -ForegroundColor Yellow
    exit 1
}

Write-Host "`n✅ Bajarildi!" -ForegroundColor Green
