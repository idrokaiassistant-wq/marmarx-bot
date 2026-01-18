# Docker Tozalash - Ko'rsatma

## ✅ MarmarX Loyihasi Tozalandi

Quyidagilar o'chirildi:
- ✅ Konteynerlar: `marmarx_api`, `marmarx_bot`, `marmarx_db`
- ✅ Image'lar: `marmarx-api:latest`, `marmarx-bot:latest`
- ✅ Volume: `marmarx_postgres_data`

## 🧹 Boshqa Loyihalarni Tozalash

### ⚠️ OGOHLANTIRISH:
Sizning kompyuteringizda quyidagi loyihalar ham bor:
- `smarttabrik` loyihalari (bot, api, worker, postgres, redis)
- `cursor` loyihalari (api, bot, worker, redis, postgres)
- `supabase` (to'liq stack)
- `ollama`
- `n8n`

### 📋 Variant 1: Faqat Foydalanuvchi Loyihalarini O'chirish (K8s tizimidan tashqari)

**Konteynerlarni o'chirish:**
```bash
# Barcha to'xtatilgan konteynerlarni o'chirish (k8s dan tashqari)
docker ps -a --filter "name=k8s" --format "{{.ID}}" | ForEach-Object { docker rm $_ }

# Yoki faqat aniq loyihalarni:
docker-compose -f <loyiha_docker-compose.yml> down -v
```

**Image'larni tozalash:**
```bash
# Ishlatilmayotgan image'larni o'chirish
docker image prune -a
```

**Volume'larni tozalash:**
```bash
# Ishlatilmayotgan volume'larni o'chirish
docker volume prune
```

### 📋 Variant 2: Hammasini Tozalash (XAVFLI - K8s ham o'chadi!)

**⚠️ EHTIYOT!** Bu Docker Desktop'ni buzishi mumkin!

```bash
# Barcha konteynerlarni o'chirish (k8s ham)
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)

# Barcha image'larni o'chirish
docker rmi $(docker images -q) -f

# Barcha volume'larni o'chirish
docker volume prune -a -f

# Barcha network'larni tozalash
docker network prune -f

# Hammasini birdan tozalash
docker system prune -a --volumes -f
```

### 📋 Variant 3: Aniq Loyihalarni Tozalash

**SmartTabrik loyihalarini tozalash:**
```bash
docker stop smart_tabrik_bot smart_tabrik_worker smart_tabrik_api smart_tabrik_postgres smart_tabrik_redis
docker rm smart_tabrik_bot smart_tabrik_worker smart_tabrik_api smart_tabrik_postgres smart_tabrik_redis
docker volume rm smarttabrik_postgres_data smarttabrik_redis_data smarttabrik_image_cache smarttabrik_antigravity_postgres_data smarttabrik_antigravity_redis_data smarttabrik_antigravity_image_cache
```

**Cursor loyihalarini tozalash:**
```bash
docker stop smarttabrik_cursor-api-1 smarttabrik_cursor-bot-1 smarttabrik_cursor-worker-1 smarttabrik_cursor-redis-1 smarttabrik_cursor-postgres-1
docker rm smarttabrik_cursor-api-1 smarttabrik_cursor-bot-1 smarttabrik_cursor-worker-1 smarttabrik_cursor-redis-1 smarttabrik_cursor-postgres-1
docker volume rm smarttabrik_cursor_pg_data
```

**Supabase va boshqa loyihalarni tozalash:**
```bash
# Supabase konteynerlari
docker stop $(docker ps -a --filter "name=supabase" --format "{{.ID}}")
docker rm $(docker ps -a --filter "name=supabase" --format "{{.ID}}")

# Ollama
docker stop ollama
docker rm ollama
docker volume rm ollama

# N8N
docker stop n8n
docker rm n8n
docker volume rm n8n_data
```

## 🔄 Tozalashdan Keyin

Agar MarmarX loyihasini qayta ishga tushirmoqchi bo'lsangiz:

```bash
docker-compose up -d
```

## 💡 Maslahat

Agar faqat MarmarX ni tozalash kerak bo'lsa, bu allaqachon qilingan ✅

Agar boshqa loyihalar ham kerak emas bo'lsa, ularni alohida o'chiring (Variant 3).

Agar "hammasini" tozalash kerak bo'lsa, Variant 2 ni ishlating, lekin Docker Desktop'ni qayta ishga tushirish kerak bo'lishi mumkin.
