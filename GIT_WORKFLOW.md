# Git Workflow - Avtomatik Push Qo'llanmasi

## Asosiy Prinsiplar

Har safar kod o'zgarishlari bajarilgandan keyin, quyidagi qadamlar bajarilishi kerak:

1. **O'zgarishlarni ko'rib chiqish**: `git status`
2. **Barcha o'zgarishlarni qo'shish**: `git add .`
3. **Commit yaratish**: `git commit -m "Qisqa va aniq commit xabari"`
4. **Push qilish**: `git push origin main`

## Avtomatik Push Skripti

### Windows (PowerShell)

`auto-push.ps1` skriptini yaratish:

```powershell
# auto-push.ps1
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
```

Ishlatish:
```powershell
.\auto-push.ps1
```

### Linux/Mac (Bash)

`auto-push.sh` skriptini yaratish:

```bash
#!/bin/bash
# auto-push.sh

echo "Git o'zgarishlarini tekshiryapman..."

# O'zgarishlarni ko'rsatish
git status

# Barcha o'zgarishlarni qo'shish
echo ""
echo "Barcha o'zgarishlarni qo'shyapman..."
git add .

# Commit xabarini so'rash
echo ""
read -p "Commit xabarini kiriting: " commit_message

if [ -z "$commit_message" ]; then
    commit_message="Update: $(date '+%Y-%m-%d %H:%M:%S')"
fi

# Commit yaratish
echo ""
echo "Commit yaratilmoqda..."
git commit -m "$commit_message"

# Push qilish
echo ""
echo "Push qilinmoqda..."
git push origin main

echo ""
echo "✅ Bajarildi!"
```

Ishlatish:
```bash
chmod +x auto-push.sh
./auto-push.sh
```

## Commit Xabarlari Formatlari

Yaxshi commit xabarlari quyidagi formatda bo'lishi kerak:

### Format
```
Type: Qisqa tavsif

Batafsil tavsif (ixtiyoriy)
```

### Type'lar

- `feat`: Yangi funksiya qo'shildi
- `fix`: Xato tuzatildi
- `docs`: Hujjatlashtirish yangilandi
- `style`: Kod formatlanishi o'zgardi
- `refactor`: Kod refaktoring qilindi
- `test`: Test qo'shildi/yangilandi
- `chore`: Build process yoki helper tool'lar yangilandi

### Misollar

```
feat: Telegram botga katalog va buyurtma funksiyalari qo'shildi

- Kategoriyalar ro'yxatini ko'rsatish
- Mahsulotlarni ko'rsatish
- Narx hisoblash
- Buyurtma berish
- Qidiruv funksiyasi
```

```
fix: Order modelida datetime import xatosi tuzatildi
```

```
docs: Git workflow qo'llanmasi qo'shildi
```

## Avtomatik Push Uchun Git Hook

### pre-push Hook (ixtiyoriy)

`.git/hooks/pre-push` faylini yaratish (Linux/Mac):

```bash
#!/bin/bash
# .git/hooks/pre-push

echo "Push qilishdan oldin testlar bajarilmoqda..."

# Bu yerga test komandalarini qo'shing
# python -m pytest
# npm test
# va hokazo...

exit 0
```

## Muhim Eslatmalar

1. **Hech qachon `-f` (force) push qilmang** - boshqa foydalanuvchilarning o'zgarishlarini yo'q qiladi
2. **Commit qilishdan oldin kodni ko'rib chiqing**: `git diff`
3. **Katta o'zgarishlarni kichik commit'larga bo'ling**
4. **Push qilishdan oldin pull qiling** agar boshqa o'zgarishlar bo'lsa: `git pull origin main`

## Tezkor Komandalar

```bash
# Barcha o'zgarishlarni ko'rish
git status

# Barcha o'zgarishlarni qo'shish va commit
git add . && git commit -m "feat: Yangi funksiya"

# Push qilish
git push origin main

# Barchasini bir vaqtda
git add . && git commit -m "feat: Yangi funksiya" && git push origin main
```

## Muammolarni Hal Qilish

### Push qilganda conflict xatosi

```bash
# Avval pull qiling
git pull origin main

# Conflict'larni hal qiling, keyin:
git add .
git commit -m "fix: Conflict hal qilindi"
git push origin main
```

### Xato commit'ni bekor qilish

```bash
# Oxirgi commit'ni bekor qilish (o'zgarishlar saqlanadi)
git reset --soft HEAD~1

# Oxirgi commit'ni bekor qilish (o'zgarishlar yo'qoladi)
git reset --hard HEAD~1
```

## Keyingi Qadamlar

Har safar kod o'zgarishlari bajarilgandan keyin:

1. `git status` - O'zgarishlarni ko'rish
2. `git add .` - Barcha o'zgarishlarni qo'shish
3. `git commit -m "Type: Tavsif"` - Commit yaratish
4. `git push origin main` - Push qilish

Yoki `auto-push.ps1` (Windows) yoki `auto-push.sh` (Linux/Mac) skriptini ishlatish.
