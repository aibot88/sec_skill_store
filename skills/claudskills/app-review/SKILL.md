---
name: app-review
description: يقدم مراجعة شاملة واحترافية للتطبيق من جميع النواحي (Frontend, Backend, Security, etc.). يقوم بتحليل الكود، فحص الثغرات الأمنية، تقييم الأداء، وتقديم تقارير مفصلة مع خطط عمل أسبوعية.
---

# 🔬 Full Application Review — Professional Edition

Detailed instructions for performing a comprehensive application audit.

## When to use this skill

- يتم استخدام هذه الـ Skill عندما يطلب المستخدم مراجعة الكود (Code Review)، أو تدقيقاً أمنياً (Security Audit)، أو تحليلاً للأداء (Performance Analysis).
- تساعد في اكتشاف الثغرات الأمنية، العيوب المعمارية، والديون التقنية (Technical Debt).
- تضمن توافق الكود مع معايير الشركات الكبرى (Enterprise Standards) وأفضل الممارسات.

## Decision Tree: Choosing the Review Type

Before starting, the agent should determine the project type:
1. **Frontend-only (Supabase/Firebase)**: Focus on Steps 0, 1, 2, 4, 5, 6, 7, 8.
2. **Fullstack (Node/Python/Go backend)**: Focus on Steps 0, 1, 2, 3, 4, 5, 6, 7, 8.
3. **Monorepo**: Repeat all relevant steps for each package within the repository.

## How to use it

Follow the step-by-step guidance below to perform a surgical analysis of the project. If scripts are available in the `scripts/` directory, run them with `--help` first.

---

## ⚠️ قواعد صارمة — احفظها قبل أي شيء

هذه القواعد غير قابلة للتجاوز. أي مراجعة تنتهكها هي مراجعة ناقصة.

```
1. افتح كل المجلدات — لا تكتفِ بالملف الرئيسي أبداً
   مثال: لو وجدت migrations.sql، افتح أيضاً supabase/migrations/*.sql
   مثال: لو وجدت package.json في الـ root، افتح scripts/ و src/ كاملاً

2. اعدّ الأرقام الحقيقية — لا تقل "بعض" أو "عدة" أو "كثير"
   شغّل الأوامر وخذ الأرقام منها، لا من خيالك

3. تحقق قبل أن تُبلّغ — لا تبلّغ عن ثغرة إلا بعد التأكد أنها لم تُصلَح
   ابحث عن: DROP POLICY / fix / patch / security / hotfix في كل الملفات
   إذا وُجد إصلاح → اذكر أن المشكلة كانت موجودة وتم حلها ✅

4. افحص كل طبقة بنفس العمق — لا تُعطِ Frontend 10 نقاط وتُعطي DevOps سطراً واحداً

5. اربط كل مشكلة بـ: الملف + رقم السطر + الحل الكامل + مستوى الخطورة
   شكل خاطئ:  "يوجد مشكلة في الأمان"
   شكل صحيح: "[CRITICAL] src/utils/exportUtils.ts:45 — لا يوجد CSV Injection protection
               الأثر: تنفيذ أوامر على جهاز الضحية عند فتح Excel
               الحل: أضف escapeCell() لكل cell تبدأ بـ = + - @

   مستويات الخطورة الإلزامية:
   CRITICAL → ثغرة أمنية تُمكّن من اختراق النظام أو سرقة البيانات
   HIGH     → مشكلة تؤثر على سلامة البيانات أو توقف الخدمة
   MEDIUM   → مشكلة تؤثر على الجودة أو تفتح باباً للمشاكل مستقبلاً
   LOW      → اقتراح تحسين أو تنظيف كود

6. اقرأ ملفات الـ coverage الحقيقية — لا تخمّن نسبة الـ tests
   cat coverage/index.html | grep -o '[0-9]*\.[0-9]*%' | head -8

7. شغّل الفحوصات اليدوية الإلزامية أدناه — كلها بدون استثناء
   هذه الأوامر تكشف المشاكل التي لا تظهر بالـ grep العادي
```

---

## 🔎 فحوصات يدوية إلزامية — شغّلها جميعاً قبل كتابة التقرير

> هذه الفحوصات أُضيفت بعد اكتشاف أن الـ Agent يُغفلها باستمرار.
> **لا تكتب كلمة واحدة في التقرير قبل تشغيل كل أمر من هذه الأوامر.**

### 🔴 الفحص 1 — .env الحقيقي في الـ Repo (أخطر نقطة)
```bash
# هل يوجد .env حقيقي مرفوع؟
find . -name ".env" \
  -not -name ".env.example" \
  -not -name ".env.sample" \
  -not -name ".env.template" \
  | grep -v node_modules

# إذا وُجد → أبلغ فوراً في أول التقرير بـ 🚨
# واطبع محتواه لتحديد ما هو مكشوف
cat .env 2>/dev/null | grep -v "^#" | grep -v "^$"
```

**الحكم:**
- وُجد `.env` بـ credentials حقيقية → 🚨 **أولوية قصوى** — اذكره في السطر الأول من التقرير
- وُجد `.env` بقيم placeholder فقط → ✅ آمن
- لا يوجد `.env` → ✅ ممتاز

---

### 🔴 الفحص 2 — slot_locks Policy الأخيرة (DoS محتمل)
```bash
# اقرأ آخر policy على slot_locks — ليس أول ملف بل آخر migration
grep -n "slot_locks" \
  $(find . -path "*/migrations/*.sql" -o -name "migrations.sql" \
    | grep -v node_modules | sort) 2>/dev/null

# تحقق من الـ policy الفعلية في آخر migration
LAST_MIGRATION=$(find . -path "*/migrations/*.sql" \
  | grep -v node_modules | sort | tail -1)
echo "=== Last Migration: $LAST_MIGRATION ==="
grep -A4 "slot_locks" "$LAST_MIGRATION" 2>/dev/null
```

**الحكم:**
- `USING (true) WITH CHECK (true)` للـ `anon` بدون TTL check → 🔴 **مشكلة حرجة**
- `WITH CHECK (expires_at > NOW() AND expires_at < NOW() + INTERVAL '15 minutes')` → ✅ آمن
- لا توجد policy → 🔴 **خطر** — RLS غير مُفعّل

---

### 🔴 الفحص 3 — audit_logs بدون RLS
```bash
# هل يوجد RLS على audit_logs؟
grep -rn "audit_logs" \
  $(find . -name "*.sql" | grep -v node_modules | sort) 2>/dev/null \
  | grep -i "POLICY\|RLS\|ROW LEVEL\|ENABLE"

# هل يوجد ENABLE ROW LEVEL SECURITY على audit_logs؟
grep -rn "audit_logs" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null \
  | grep "ENABLE ROW LEVEL SECURITY"
```

**الحكم:**
- لا يوجد `ENABLE ROW LEVEL SECURITY` على `audit_logs` → 🔴 **مشكلة** — أي admin يكتب سجلات مزيفة
- يوجد RLS لكن لا توجد INSERT policy → ✅ صحيح (الكتابة فقط عبر SECURITY DEFINER)
- يوجد RLS + SELECT policy للـ admin → ✅ ممتاز

---

### 🔴 الفحص 4 — SECURITY DEFINER بدون REVOKE
```bash
# كل دوال SECURITY DEFINER
grep -n "SECURITY DEFINER" \
  $(find . -name "*.sql" | grep -v node_modules | sort) 2>/dev/null

# هل يوجد REVOKE بعد كل واحدة؟
echo "=== REVOKE statements ==="
grep -n "REVOKE" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null

# المقارنة: عدد SECURITY DEFINER vs عدد REVOKE
SD_COUNT=$(grep -rh "SECURITY DEFINER" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null | wc -l)
RV_COUNT=$(grep -rh "REVOKE" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null | wc -l)
echo "SECURITY DEFINER functions: $SD_COUNT"
echo "REVOKE statements: $RV_COUNT"
echo "الفرق (يجب أن يكون 0 أو الـ REVOKE أكثر): $(($SD_COUNT - $RV_COUNT))"
```

**الحكم:**
- عدد REVOKE أقل من عدد SECURITY DEFINER → 🟡 بعض الدوال مكشوفة للـ PUBLIC
- كل دالة SECURITY DEFINER لها REVOKE → ✅ ممتاز

---

### 🟡 الفحص 5 — CSV Injection في ملفات Export
```bash
# ابحث عن كل ملفات Export
EXPORT_FILES=$(find src -name "*export*" -o -name "*Export*" \
  | grep -v node_modules | grep -v test)
echo "Export files: $EXPORT_FILES"

# هل يوجد escaping للقيم الخطرة؟
grep -n "escapeCell\|escape\|sanitize\|replace.*[=+\-@]" \
  $EXPORT_FILES 2>/dev/null

# هل تُكتب البيانات مباشرة بدون escape؟
grep -n "fullName\|name\|phone\|notes" \
  $EXPORT_FILES 2>/dev/null | grep -v "escape\|sanitize" | head -10
```

**الحكم:**
- بيانات تُكتب مباشرة بدون `escapeCell` → 🔴 **CSV Injection**
- يوجد `escapeCell` أو prefix بـ `'` → ✅ محمي

---

### 🟡 الفحص 6 — Security Headers الكاملة
```bash
python3 -c "
import json
try:
    d = json.load(open('vercel.json'))
    headers = d.get('headers',[{}])[0].get('headers',[])
    keys = [h['key'] for h in headers]

    required = {
        'Content-Security-Policy':        'أهم header',
        'X-Frame-Options':                'منع Clickjacking',
        'X-Content-Type-Options':         'منع MIME sniffing',
        'Strict-Transport-Security':      'إجبار HTTPS',
        'Referrer-Policy':                'حماية الـ referrer',
        'Permissions-Policy':             'تقييد browser APIs',
        'Cross-Origin-Opener-Policy':     'حماية من Spectre',
        'Cross-Origin-Resource-Policy':   'منع cross-origin reads',
    }

    dangerous_csp = []
    csp = next((h['value'] for h in headers if h['key']=='Content-Security-Policy'), '')
    if \"'unsafe-eval'\" in csp: dangerous_csp.append('unsafe-eval')
    if \"'unsafe-inline'\" in csp: dangerous_csp.append('unsafe-inline')

    print('=== Security Headers ===')
    for r, desc in required.items():
        status = '✅' if r in keys else '❌ مفقود'
        print(f'{status} {r} — {desc}')

    print()
    print('=== CSP Issues ===')
    if dangerous_csp:
        for d in dangerous_csp:
            print(f'🔴 {d} موجود في CSP — يُضعف الحماية')
    else:
        print('✅ لا توجد مشاكل في CSP')
except Exception as e:
    print(f'خطأ: {e}')
"
```

---

### 🟡 الفحص 7 — CI Pipeline الكامل
```bash
# اقرأ كل workflows
echo "=== CI Steps ==="
python3 -c "
import os, glob
try:
    import yaml
    for f in glob.glob('.github/workflows/*.yml'):
        d = yaml.safe_load(open(f))
        print(f'File: {f}')
        for job_name, job in d.get('jobs',{}).items():
            print(f'  Job: {job_name}')
            for step in job.get('steps',[]):
                name = step.get('name','unnamed')
                run  = step.get('run','')[:60]
                print(f'    - {name}: {run}')
except ImportError:
    os.system(\"cat .github/workflows/*.yml 2>/dev/null\")
"

# ما المفقود؟
echo ""
echo "=== Missing CI Steps ==="
CI_CONTENT=$(cat .github/workflows/*.yml 2>/dev/null)
for step in "npm run lint" "npm audit" "npm run build" "tsc --noEmit"; do
  if echo "$CI_CONTENT" | grep -q "$step"; then
    echo "✅ $step"
  else
    echo "❌ مفقود: $step"
  fi
done
```

---

### 🟢 الفحص 8 — ملفات زائدة يجب حذفها
```bash
echo "=== Stale/Temp Files ==="

# ملفات backup
find . -name "*.bak" -o -name "*.tmp" -o -name "*.orig" \
  | grep -v node_modules

# ملفات Python خارج src/ (مشبوهة في مشاريع TypeScript)
find . -name "*.py" -not -path "*/src/*" -not -path "*/tests/*" \
  -not -path "*/scripts/*" | grep -v node_modules

# ملفات .bak داخل src/
find src/ -name "*.bak" -o -name "*.backup" 2>/dev/null

# ملفات build output داخل src/
find src/ -name "*.js" -not -name "*.test.js" -not -name "*.config.js" \
  2>/dev/null | head -5

echo "=== Root-level clutter ==="
ls *.py *.sh *.log 2>/dev/null | grep -v node_modules
```

---

### 🟢 الفحص 9 — أكبر الملفات (تحتاج تقسيم)
```bash
echo "=== Files > 300 lines (need splitting) ==="
find src -name "*.tsx" -o -name "*.ts" | grep -v node_modules | grep -v test \
  | grep -v ".d.ts" | xargs wc -l 2>/dev/null \
  | sort -rn | awk 'NR>1 && $1>300 {
      if ($1>800) icon="🔴"
      else if ($1>500) icon="🟡"
      else icon="🟢"
      print icon, $1, "lines —", $2
    }' | head -15
```

---

### 🟢 الفحص 10 — TypeScript Quality Score
```bash
echo "=== TypeScript Health ==="

# any usage count
ANY=$(grep -rn "\bany\b" --include="*.ts" --include="*.tsx" \
  src/ | grep -v ".d.ts" | grep -v "//.*any" | grep -v test | wc -l)
echo "any usage: $ANY $([ $ANY -lt 5 ] && echo '✅' || [ $ANY -lt 20 ] && echo '🟡' || echo '🔴')"

# ts-ignore usage
TSIG=$(grep -rn "@ts-ignore\|@ts-nocheck" --include="*.ts" --include="*.tsx" \
  src/ | grep -v node_modules | wc -l)
echo "@ts-ignore: $TSIG $([ $TSIG -eq 0 ] && echo '✅' || echo '🟡')"

# console.log في production (بدون logger)
CLOG=$(grep -rn "console\.log" --include="*.ts" --include="*.tsx" \
  src/ | grep -v node_modules | grep -v test | grep -v "logger" | wc -l)
echo "console.log: $CLOG $([ $CLOG -eq 0 ] && echo '✅' || echo '🟡')"

# TODO/FIXME count
TODO=$(grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.ts" --include="*.tsx" \
  src/ | grep -v node_modules | wc -l)
echo "TODO/FIXME: $TODO"
```

---

## 🗺️ خريطة المراجعة الكاملة

```
الخطوة 0 → استكشاف + تحديد التقنيات (5 دقائق)
    ↓
الخطوة 1 → قاعدة البيانات والـ Schema (أهم خطوة)
    ↓
الخطوة 2   → الأمان الشامل (ثاني أهم خطوة)
    ↓
الخطوة 2.5 → البنية المعمارية + Dead Code + Circular Dependencies (جديد)
    ↓
الخطوة 3   → Backend / API / RPC
    ↓
الخطوة 4   → Frontend / UI / UX
    ↓
الخطوة 5 → Testing & Coverage (أرقام حقيقية)
    ↓
الخطوة 6 → جودة الكود والبنية المعمارية
    ↓
الخطوة 7 → DevOps / CI / CD / Infrastructure
    ↓
الخطوة 8 → الأداء والـ Bundle
    ↓
الخطوة 9 → التقرير النهائي الكامل
```

---

## الخطوة 0 — الاستكشاف الكامل 🗂️

### 0.1 تحليل هيكل المشروع الكامل
```bash
# الهيكل الكامل بدون node_modules و dist و .git
find . -type f | grep -v node_modules | grep -v dist | grep -v ".git" \
  | grep -v coverage | sort | head -200

# إحصاء الملفات حسب النوع
find . -type f | grep -v node_modules | grep -v dist | grep -v ".git" \
  | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20

# حجم المشروع الإجمالي
find . -type f | grep -v node_modules | grep -v dist | grep -v ".git" \
  | xargs wc -l 2>/dev/null | tail -1

# الملفات الأكبر (قد تحتاج تقسيم)
find . -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \
  | grep -v node_modules | grep -v dist | xargs wc -l 2>/dev/null \
  | sort -rn | head -20
```

### 0.2 تحديد التقنيات بدقة
```bash
# Frontend Framework
cat package.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
deps = {**d.get('dependencies',{}), **d.get('devDependencies',{})}
frameworks = ['react','vue','angular','svelte','next','nuxt','remix','astro','solid']
tools = ['vite','webpack','esbuild','rollup','parcel','turbopack']
db = ['supabase','prisma','drizzle','mongoose','typeorm','sequelize']
state = ['redux','zustand','jotai','recoil','pinia','mobx','xstate']
test = ['vitest','jest','cypress','playwright','testing-library']
for k in frameworks+tools+db+state+test:
    if k in deps: print(f'  {k}: {deps[k]}')
"

# Backend / Runtime
ls -la src/ 2>/dev/null || ls -la app/ 2>/dev/null || ls -la server/ 2>/dev/null
cat go.mod 2>/dev/null | head -5
cat requirements.txt 2>/dev/null | head -20
cat Cargo.toml 2>/dev/null | head -10

# قاعدة البيانات
find . -name "*.sql" -o -name "*.prisma" -o -name "schema.rb" \
  -o -name "models.py" | grep -v node_modules | head -20
find . -path "*/migrations/*" -type f | grep -v node_modules | head -30

# Deployment
ls .github/workflows/ 2>/dev/null
ls -la Dockerfile docker-compose.yml vercel.json netlify.toml \
  fly.toml railway.toml render.yaml 2>/dev/null
```

### 0.3 الملفات الحساسة
```bash
# تحقق من وجود .env في الـ repo
ls -la .env .env.local .env.production .env.staging 2>/dev/null
cat .gitignore | grep -i "\.env"

# ملفات backup أو مؤقتة يجب حذفها
find . -name "*.bak" -o -name "*.tmp" -o -name "*.orig" \
  | grep -v node_modules | head -10
find . -name "*.py" -not -path "*/src/*" -not -path "*/tests/*" \
  | grep -v node_modules | head -5
```

**قرّر نوع المشروع ثم تابع الخطوات المناسبة:**
- `Frontend-only (Supabase/Firebase)` → خطوات: 0,1,2,4,5,6,7,8
- `Fullstack (Node/Python/Go backend)` → خطوات: 0,1,2,3,4,5,6,7,8
- `Monorepo` → كرّر كل خطوة على كل package

---

## الخطوة 1 — قاعدة البيانات والـ Schema 🗄️

> **هذه أهم خطوة في المراجعة** — معظم الثغرات والمشاكل الحرجة تبدأ من هنا.

### 1.1 قراءة كل ملفات الـ Schema والـ Migrations
```bash
# اقرأ كل ملفات SQL — ليس ملفاً واحداً فقط
find . -name "*.sql" | grep -v node_modules | sort | while read f; do
  echo "=== $f ===" && wc -l "$f"
done

# اقرأ كل migration بالترتيب الزمني
find . -path "*/migrations/*" -name "*.sql" | sort | head -20

# Schema كامل (Prisma/Drizzle/TypeORM)
find . -name "*.prisma" -o -name "schema.ts" -o -name "schema.rb" \
  | grep -v node_modules | xargs cat 2>/dev/null
```

### 1.2 تحليل الـ RLS Policies (Supabase)
```bash
# استخرج كل policies
grep -n "CREATE POLICY\|DROP POLICY\|USING\|WITH CHECK" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null

# ابحث عن USING (true) للـ anon — خطر محتمل
grep -n "USING (true)\|WITH CHECK (true)" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null

# تحقق من جداول بدون RLS
grep -n "ENABLE ROW LEVEL SECURITY" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null

# تحقق من GRANT للـ anon
grep -n "GRANT.*TO anon\|GRANT.*PUBLIC" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null
```

**قائمة فحص RLS:**
- [ ] كل جدول يحتوي بيانات حساسة عليه `ENABLE ROW LEVEL SECURITY`
- [ ] لا يوجد `USING (true)` على جداول patients / users / invoices / medical_records
- [ ] `anon` لا يستطيع قراءة بيانات مستخدمين آخرين
- [ ] `slot_locks` و`settings` و`closures` فقط هي المقبول أن تكون مفتوحة للـ anon
- [ ] `audit_logs` لها RLS تمنع الكتابة المباشرة

### 1.3 تحليل الـ SECURITY DEFINER Functions
```bash
grep -n "SECURITY DEFINER" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null

# هل يوجد REVOKE من PUBLIC بعد كل SECURITY DEFINER function؟
grep -A2 "SECURITY DEFINER" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null | grep -i "REVOKE\|GRANT"

# هل يوجد SET search_path لمنع search_path injection؟
grep -n "SET search_path" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null
```

**قائمة فحص RPC Security:**
- [ ] كل `SECURITY DEFINER` function يليها `REVOKE ALL FROM PUBLIC`
- [ ] كل `SECURITY DEFINER` function يحتوي `SET search_path = public`
- [ ] الدوال التي تقبل input تتحقق من صحته قبل التنفيذ
- [ ] `factory_reset` / `delete_all` / أي دالة مدمّرة محمية بـ role check صارم

### 1.4 الـ Indexes والأداء
```bash
# كل الـ indexes الموجودة
grep -n "CREATE INDEX\|CREATE UNIQUE INDEX" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null

# الحقول المستخدمة في WHERE كثيراً (يجب أن تكون indexed)
grep -n "WHERE\|ORDER BY\|GROUP BY" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null | head -30
```

**قائمة فحص الـ Indexes:**
- [ ] Foreign Keys لها indexes
- [ ] حقول البحث (phone, email, name) لها indexes
- [ ] حقول الفلترة (status, date, created_at) لها indexes
- [ ] لا يوجد `NOW()` في partial index (غير مسموح)

### 1.5 سلامة الـ Schema
```bash
# تكرار البيانات (denormalization)
grep -n "patient_name\|patient_phone\|user_email\|user_name" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null

# Constraints
grep -n "CHECK\|UNIQUE\|NOT NULL\|DEFAULT\|FOREIGN KEY\|REFERENCES" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null | head -30

# Timestamps
grep -n "created_at\|updated_at\|deleted_at" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null | head -10
```

---

## الخطوة 2 — الأمان الشامل 🔐

> **ثاني أهم خطوة** — أي ثغرة هنا تؤثر مباشرة على المرضى/المستخدمين.

### 2.1 فحص الـ Secrets المكشوفة
```bash
# هل .env الحقيقي موجود في الـ repo؟
find . -name ".env" -not -name ".env.example" -not -name ".env.sample" \
  | grep -v node_modules | head -5

# تحقق من credentials في ملفات الكود مباشرة
grep -rn "password\s*[=:]\s*['\"][^'\"]\{4,\}" \
  --include="*.ts" --include="*.js" --include="*.py" \
  | grep -v node_modules | grep -v "test\|spec\|mock\|example" | head -10

grep -rn "api_key\s*[=:]\s*['\"][^'\"]\{8,\}" \
  --include="*.ts" --include="*.js" --include="*.py" \
  | grep -v node_modules | head -10

grep -rn "secret\s*[=:]\s*['\"][^'\"]\{8,\}" \
  --include="*.ts" --include="*.js" --include="*.py" \
  | grep -v node_modules | grep -v "test\|spec\|mock" | head -10

# VITE_ variables في الكود مباشرة (يجب أن تكون فقط عبر import.meta.env)
grep -rn "VITE_SUPABASE\|VITE_API\|VITE_SECRET" \
  --include="*.ts" --include="*.tsx" --include="*.js" \
  | grep -v node_modules | grep -v "import.meta.env" | head -10
```

### 2.2 فحص الـ Content Security Policy
```bash
# vercel.json / netlify.toml / nginx.conf
cat vercel.json 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
headers = d.get('headers',[{}])[0].get('headers',[])
for h in headers:
    print(h.get('key',''), '=', h.get('value','')[:80])
" 2>/dev/null

# مشاكل خطيرة في CSP
grep -i "unsafe-inline\|unsafe-eval\|unsafe-hashes\|\* " vercel.json 2>/dev/null

# Security headers مفقودة
python3 -c "
import json
try:
    d = json.load(open('vercel.json'))
    headers = d.get('headers',[{}])[0].get('headers',[])
    keys = [h['key'] for h in headers]
    required = [
        'Content-Security-Policy',
        'X-Frame-Options',
        'X-Content-Type-Options',
        'Strict-Transport-Security',
        'Referrer-Policy',
        'Permissions-Policy',
        'Cross-Origin-Opener-Policy',
    ]
    for r in required:
        status = '✅' if r in keys else '❌ MISSING'
        print(f'{status} {r}')
except: pass
"
```

### 2.3 فحص XSS و Injection
```bash
# هل يُستخدم DOMPurify أو تعقيم مشابه؟
grep -rn "DOMPurify\|sanitize\|innerHtml\|dangerouslySetInnerHTML" \
  --include="*.ts" --include="*.tsx" --include="*.js" \
  | grep -v node_modules | head -20

# dangerouslySetInnerHTML بدون sanitize — خطر XSS
grep -rn "dangerouslySetInnerHTML" \
  --include="*.tsx" --include="*.jsx" \
  | grep -v node_modules \
  | grep -v "sanitize\|DOMPurify\|purify" | head -10

# SQL Injection patterns
grep -rn "f\"SELECT\|f'SELECT\|\`SELECT.*\${" \
  --include="*.py" --include="*.ts" --include="*.js" \
  | grep -v node_modules | head -10
```

### 2.4 فحص CSV/Excel Injection
```bash
# ملفات Export — هل تُعقّم البيانات؟
find . -name "export*.ts" -o -name "*Export*.ts" -o -name "*export*.ts" \
  | grep -v node_modules | xargs grep -l "xlsx\|csv\|XLSX" 2>/dev/null

# هل توجد حماية من formulas خطيرة؟
grep -rn "escape\|sanitize\|=.*replace\|^=\|^+\|^-\|^@" \
  $(find . -name "*export*" -o -name "*Export*" | grep -v node_modules) 2>/dev/null
```

### 2.5 فحص Authentication & Authorization
```bash
# Guard components
find . -name "*Guard*" -o -name "*guard*" -o -name "*Auth*" \
  | grep -v node_modules | grep -v ".d.ts" | head -10

# هل كل routes محمية؟
cat src/App.tsx 2>/dev/null || cat src/router.tsx 2>/dev/null \
  || cat src/routes.tsx 2>/dev/null | head -80

# JWT / Token handling
grep -rn "localStorage.*token\|sessionStorage.*token\|cookie.*token" \
  --include="*.ts" --include="*.tsx" \
  | grep -v node_modules | head -10
```

### 2.6 فحص Rate Limiting
```bash
# Client-side rate limiting (قابل للتجاوز)
grep -rn "useRateLimit\|rateLimit\|rate_limit" \
  --include="*.ts" --include="*.tsx" \
  | grep -v node_modules | head -10

# Server-side / DB rate limiting (أقوى)
grep -rn "rate_limit\|rateLimit\|throttle" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null
```

**قائمة فحص الأمان الشامل:**

| الجانب | ما تفحصه | الحكم |
|--------|----------|-------|
| `.env` في الـ repo | يجب أن يكون في `.gitignore` فقط | ✅/❌ |
| CSP `unsafe-eval` | يجب إزالته في production | ✅/❌ |
| CSP `unsafe-inline` | يجب استبداله بـ nonce أو hash | ✅/❌ |
| XSS Protection | DOMPurify على كل user input | ✅/❌ |
| CSV Injection | escape في كل Excel/CSV export | ✅/❌ |
| SQL Injection | parameterized queries فقط | ✅/❌ |
| Auth على كل routes | AuthGuard على كل admin pages | ✅/❌ |
| Rate Limiting على DB | check في RPC وليس client فقط | ✅/❌ |
| REVOKE من SECURITY DEFINER | بعد كل function | ✅/❌ |
| Secrets في الكود | لا يوجد أي credential مكشوف | ✅/❌ |

---

---

## الخطوة 2.5 — البنية المعمارية + Dead Code 🏛️

> مُضاف من ENTERPRISE SKILL v2 — يكشف مشاكل معمارية لا تظهر في الفحص الأمني.

### 2.5.1 تحليل Layer Violations (تسرّب الطبقات)
```bash
# هل الـ domain تستورد من infrastructure؟ (مخالفة صارمة)
echo "=== Domain importing Infrastructure (VIOLATION) ==="
grep -rn "import.*infrastructure" src/domain/ 2>/dev/null | head -10

# هل الـ domain تستورد من presentation؟ (مخالفة صارمة)
grep -rn "import.*presentation" src/domain/ 2>/dev/null | head -10

# هل الـ application تستورد من presentation؟ (مخالفة)
grep -rn "import.*presentation" src/application/ 2>/dev/null | head -10

# هل الـ UI تستدعي قاعدة البيانات مباشرة؟
grep -rn "supabase\.\|prisma\.\|mongoose\." src/presentation/ 2>/dev/null \
  | grep -v "test\|spec" | head -10

# هل Domain Logic موجودة داخل Components؟
grep -rn "businessRule\|validateBooking\|calculatePrice\|applyDiscount" \
  src/presentation/ 2>/dev/null | head -10
```

**الحكم:**
- أي import من `domain → infrastructure` أو `domain → presentation` → **[HIGH] Layer Violation**
- `supabase.` مباشرة في presentation بدون repository → **[HIGH] Architecture Violation**
- لا توجد انتهاكات → ✅ Clean Architecture محترم

---

### 2.5.2 Circular Dependencies
```bash
# ابحث عن circular imports بين الملفات
# الطريقة: تتبع سلاسل الـ import
echo "=== Checking for circular dependency patterns ==="

# ملفات تستورد من بعضها (circular indicator)
for file in $(find src -name "*.ts" -o -name "*.tsx" | grep -v node_modules | grep -v test); do
  imports=$(grep "^import" "$file" 2>/dev/null | grep -o "from '[^']*'" | tr -d "from '" )
  for imp in $imports; do
    # هل الملف المُستورَد يستورد بدوره من الملف الأصلي؟
    if grep -q "$(basename $file .ts)\|$(basename $file .tsx)" "src/$imp.ts" 2>/dev/null \
    || grep -q "$(basename $file .ts)\|$(basename $file .tsx)" "src/$imp.tsx" 2>/dev/null; then
      echo "[HIGH] Possible circular: $file ↔ $imp"
    fi
  done
done 2>/dev/null | head -20

# بديل أسرع — ابحث عن الأنماط الشائعة
echo "=== Common circular patterns ==="
grep -rn "from.*container\|from.*index" src/application/ 2>/dev/null | head -10
grep -rn "from.*container\|from.*index" src/domain/ 2>/dev/null | head -10
```

---

### 2.5.3 Dead Code Detection (الكود الميت)
```bash
echo "=== Dead Code Analysis ==="

# 1. ملفات موجودة لكن لا أحد يستوردها
echo "--- Potentially unused files ---"
find src -name "*.ts" -o -name "*.tsx" | grep -v node_modules | grep -v test \
  | grep -v "index\.\|main\.\|App\." | while read file; do
  basename_no_ext=$(basename "$file" | sed 's/\.[^.]*$//')
  # ابحث عن اسم الملف في كل imports
  usage=$(grep -rn "from.*$basename_no_ext\|import.*$basename_no_ext" \
    src/ --include="*.ts" --include="*.tsx" 2>/dev/null \
    | grep -v "$file" | grep -v test | wc -l)
  if [ "$usage" -eq 0 ]; then
    echo "[LOW] Possibly unused: $file"
  fi
done 2>/dev/null | head -20

# 2. ملفات .bak و backup صريحة
echo "--- Backup/temp files (should be deleted) ---"
find . -name "*.bak" -o -name "*.backup" -o -name "*.orig" \
  | grep -v node_modules | while read f; do echo "[LOW] Stale file: $f"; done

# 3. exports معرّفة لكن لا تُستخدم (TypeScript)
echo "--- Exported but potentially unused functions ---"
grep -rn "^export function\|^export const\|^export class" \
  src/ --include="*.ts" 2>/dev/null | grep -v test | while read line; do
  func=$(echo "$line" | grep -o "function [A-Za-z]*\|const [A-Za-z]*\|class [A-Za-z]*" \
    | awk '{print $2}' | head -1)
  if [ -n "$func" ]; then
    usage=$(grep -rn "$func" src/ --include="*.ts" --include="*.tsx" 2>/dev/null \
      | grep -v "^.*export" | grep -v test | wc -l)
    if [ "$usage" -le 1 ]; then
      file=$(echo "$line" | cut -d: -f1)
      echo "[LOW] Possibly unused export: $func in $file"
    fi
  fi
done 2>/dev/null | head -15

# 4. TODO/FIXME المتراكمة
echo "--- Technical Debt (TODO/FIXME) ---"
grep -rn "TODO\|FIXME\|HACK\|XXX\|TEMP\|BUG" \
  src/ --include="*.ts" --include="*.tsx" \
  | grep -v node_modules | grep -v test \
  | awk -F: '{print "[LOW]", $1":"$2, $3}' | head -20
echo "Total TODO/FIXME: $(grep -rn 'TODO\|FIXME\|HACK\|XXX' src/ --include='*.ts' --include='*.tsx' | grep -v node_modules | grep -v test | wc -l)"
```

**الحكم:**
- ملفات موجودة بدون أي import → **[LOW] Dead Code** — احذفها
- ملفات `.bak` أو `.backup` → **[LOW]** — لا مكانها في الـ repo
- exports بدون استخدام → **[LOW]** — احذف أو علّق

---


## الخطوة 3 — Backend / API / RPC ⚙️

### 3.1 تحليل نوع الـ Backend
```bash
# هل هو Frontend-only مع Supabase؟
ls src/infrastructure/repositories/ 2>/dev/null
grep -rn "supabase.rpc\|supabase.from" --include="*.ts" -l | head -10

# هل يوجد Node.js/Express backend؟
find . -name "server.ts" -o -name "server.js" -o -name "app.ts" \
  | grep -v node_modules | head -5

# هل يوجد Python/FastAPI/Django؟
find . -name "main.py" -o -name "app.py" -o -name "wsgi.py" | head -5
```

### 3.2 مراجعة RPC Functions (Supabase)
```bash
# كل الـ RPC calls من الـ Frontend
grep -rn "supabase\.rpc(" \
  --include="*.ts" --include="*.tsx" \
  | grep -v node_modules | head -30

# مقارنة بـ RPCs المعرّفة في SQL
grep -n "CREATE.*FUNCTION\|CREATE OR REPLACE FUNCTION" \
  $(find . -name "*.sql" | grep -v node_modules) 2>/dev/null
```

### 3.3 مراجعة Repositories
```bash
# كل repositories
ls src/infrastructure/repositories/ 2>/dev/null

# هل يوجد raw queries خطيرة؟
grep -rn "\.raw\|\.execute\|\.query(" \
  --include="*.ts" src/infrastructure/ 2>/dev/null | head -15

# N+1 queries patterns
grep -rn "for.*await\|forEach.*async\|map.*await" \
  --include="*.ts" src/ | grep -v node_modules | head -10

# هل يوجد pagination في كل list queries؟
grep -rn "\.range\|\.limit\|pageSize\|pagination" \
  --include="*.ts" src/ | grep -v node_modules | head -10
```

### 3.4 مراجعة Error Handling
```bash
# هل كل الـ errors مُعالجة؟
grep -rn "catch.*{}" --include="*.ts" | grep -v node_modules | head -10
grep -rn "\.catch()" --include="*.ts" | grep -v node_modules | head -10

# Result<T,E> pattern أو throw/catch عشوائي؟
grep -rn "Result<\|AppError\|ErrorCode" --include="*.ts" -l \
  | grep -v node_modules | head -10
```

---

## الخطوة 4 — Frontend / UI 🎨

### 4.1 هيكل المكونات والأحجام
```bash
# الملفات الأكبر من 300 سطر (تحتاج تقسيم)
find src -name "*.tsx" -o -name "*.jsx" | xargs wc -l 2>/dev/null \
  | sort -rn | awk '$1 > 300' | head -15

# عدد المكونات الإجمالي
find src -name "*.tsx" | grep -v node_modules | wc -l

# هل يوجد index.ts لكل مجلد؟
find src -type d | grep -v node_modules | while read d; do
  ls "$d/index.ts" "$d/index.tsx" 2>/dev/null && echo "✅ $d" || echo "❌ $d"
done | head -20
```

### 4.2 فحص الـ Hooks
```bash
# كل custom hooks
find src -name "use*.ts" -o -name "use*.tsx" | grep -v node_modules | grep -v test | head -20

# useEffect بدون cleanup (memory leaks)
grep -rn "useEffect" --include="*.tsx" --include="*.ts" -A10 \
  | grep -B5 "addEventListener\|setInterval\|setTimeout\|subscribe" \
  | grep -v "return\s*()\s*=>" | head -20

# useEffect بدون dependencies
grep -rn "useEffect(\(\) =>" --include="*.tsx" | grep -v node_modules | head -10
```

### 4.3 فحص الأداء
```bash
# lazy loading للـ pages
grep -rn "lazy\|Suspense\|import(" src/App.tsx src/router* 2>/dev/null | head -20

# React.memo / useMemo / useCallback
grep -rn "React\.memo\|useMemo\|useCallback" \
  --include="*.tsx" src/ | grep -v node_modules | wc -l

# صور بدون lazy loading أو width/height
grep -rn "<img " --include="*.tsx" | grep -v "loading=\|lazy\|width=" \
  | grep -v node_modules | head -10
```

### 4.4 إمكانية الوصول (A11y)
```bash
# صور بدون alt
grep -rn "<img " --include="*.tsx" | grep -v "alt=" | grep -v node_modules | head -10

# buttons بدون نص أو aria-label
grep -rn "<button" --include="*.tsx" | grep -v "aria-label\|children" \
  | grep -v node_modules | head -10

# form inputs بدون label
grep -rn "<input " --include="*.tsx" | grep -v "aria-label\|id=" \
  | grep -v node_modules | head -10

# RTL support للمشاريع العربية
grep -rn "dir=\"rtl\"\|direction.*rtl\|lang=\"ar\"" \
  --include="*.tsx" --include="*.html" | head -5
```

### 4.5 State Management
```bash
# هل يوجد prop drilling مفرط؟
grep -rn "props\." --include="*.tsx" | grep -v node_modules \
  | awk -F: '{print $1}' | sort | uniq -c | sort -rn | head -10

# React Query configuration
cat src/lib/queryClient.ts 2>/dev/null || cat src/lib/query*.ts 2>/dev/null

# staleTime / gcTime إعدادات
grep -rn "staleTime\|gcTime\|cacheTime\|refetchOnWindowFocus" \
  --include="*.ts" src/ | grep -v node_modules | head -10
```

---

## الخطوة 5 — Testing & Coverage 📊

> **قاعدة صارمة**: اقرأ ملفات الـ coverage الحقيقية — لا تخمّن.

### 5.1 قياس الـ Coverage الحقيقية
```bash
# اقرأ الـ coverage report
cat coverage/index.html 2>/dev/null | python3 -c "
import sys, re
content = sys.stdin.read()
# استخرج النسب من الـ HTML
percentages = re.findall(r'(\d+\.?\d*)\s*%', content)
labels = re.findall(r'(Statements|Branches|Functions|Lines)', content)
for l, p in zip(labels, percentages[:4]):
    icon = '✅' if float(p) >= 70 else '🟡' if float(p) >= 50 else '❌'
    print(f'{icon} {l}: {p}%')
" 2>/dev/null || echo "لا يوجد coverage report — شغّل npm run test:coverage أولاً"

# عدد ملفات الـ tests (الرقم الحقيقي)
echo "Test files:"
find . -name "*.test.ts" -o -name "*.test.tsx" -o -name "*.spec.ts" \
  -o -name "*.spec.tsx" -o -name "test_*.py" \
  | grep -v node_modules | wc -l

# توزيع الـ tests
echo "Tests by layer:"
find src -name "*.test.*" | grep -v node_modules | sed 's|src/||' \
  | cut -d/ -f1 | sort | uniq -c | sort -rn
```

### 5.2 جودة الـ Tests
```bash
# هل توجد edge cases؟
grep -rn "throw\|error\|fail\|reject\|invalid\|empty\|null\|undefined" \
  $(find src -name "*.test.*" | grep -v node_modules) 2>/dev/null | wc -l

# هل توجد E2E tests؟
ls cypress/ playwright/ e2e/ tests/e2e/ 2>/dev/null || echo "❌ لا يوجد E2E tests"

# هل توجد tests للـ presentation layer؟
find src/presentation -name "*.test.*" 2>/dev/null | wc -l

# test:coverage threshold في vite/jest config
grep -rn "threshold\|coverageThreshold\|statements\|lines\|functions\|branches" \
  vite.config.ts jest.config.* 2>/dev/null | head -10
```

---

## الخطوة 6 — جودة الكود والبنية المعمارية 🏗️

### 6.1 البنية المعمارية
```bash
# Clean Architecture تحقق
ls src/domain/ src/application/ src/infrastructure/ src/presentation/ 2>/dev/null

# dependency direction (infrastructure يجب ألا يُستورد في domain)
grep -rn "import.*infrastructure" src/domain/ 2>/dev/null | head -5
grep -rn "import.*presentation" src/domain/ 2>/dev/null | head -5
grep -rn "import.*presentation" src/application/ 2>/dev/null | head -5
```

### 6.2 TypeScript Quality
```bash
# any usage
grep -rn "\bany\b" --include="*.ts" --include="*.tsx" \
  | grep -v node_modules | grep -v ".d.ts" | grep -v "//.*any" \
  | grep -v test | wc -l

# as casting (unsafe)
grep -rn " as " --include="*.ts" --include="*.tsx" \
  | grep -v node_modules | grep -v ".d.ts" | grep -v "//.*as " | wc -l

# ts-ignore / ts-expect-error
grep -rn "@ts-ignore\|@ts-nocheck\|@ts-expect-error" \
  --include="*.ts" --include="*.tsx" | grep -v node_modules | head -10

# strict mode check
cat tsconfig.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
opts = d.get('compilerOptions',{})
strict_opts = ['strict','noImplicitAny','noUnusedLocals','noUnusedParameters',
               'strictNullChecks','noUncheckedIndexedAccess','exactOptionalPropertyTypes']
for o in strict_opts:
    val = opts.get(o, '❌ NOT SET')
    icon = '✅' if val == True else '❌'
    print(f'{icon} {o}: {val}')
"
```

### 6.3 Code Smells
```bash
# TODO / FIXME في الكود (عدّها)
grep -rn "TODO\|FIXME\|HACK\|XXX\|BUG\|TEMP" \
  --include="*.ts" --include="*.tsx" --include="*.py" \
  | grep -v node_modules | wc -l

# console.log في production code
grep -rn "console\.log\|console\.warn\|console\.error" \
  --include="*.ts" --include="*.tsx" \
  | grep -v node_modules | grep -v "logger\|test\|spec" | head -10

# حلقات await متسلسلة (يجب Promise.all)
grep -rn "for.*of.*await\|for.*in.*await" \
  --include="*.ts" --include="*.tsx" | grep -v node_modules | head -10

# ملفات .bak أو .tmp أو backup
find . -name "*.bak" -o -name "*.tmp" -o -name "*.orig" -o -name "*.backup" \
  | grep -v node_modules | head -10
```

### 6.4 Linting Configuration
```bash
# اقرأ إعدادات الـ linting
cat .eslintrc.json .eslintrc.js .eslintrc.yaml 2>/dev/null
cat .prettierrc .prettierrc.json 2>/dev/null

# نتائج الـ lint (من ملفات الـ output الموجودة)
cat lint-errors.txt 2>/dev/null | wc -l
cat tsc_errors.txt tsc-errors.txt tsc_output.txt 2>/dev/null | head -20
```

---

## الخطوة 7 — DevOps / CI / CD 🚀

### 7.1 فحص الـ CI Pipeline
```bash
# اقرأ كل workflows
cat .github/workflows/*.yml 2>/dev/null
ls .gitlab-ci.yml .circleci/ .travis.yml 2>/dev/null

# ما الخطوات الموجودة في الـ CI؟
python3 -c "
import yaml, glob
for f in glob.glob('.github/workflows/*.yml'):
    d = yaml.safe_load(open(f))
    for job in d.get('jobs',{}).values():
        steps = job.get('steps',[])
        print(f'File: {f}')
        for s in steps:
            print(f'  - {s.get(\"name\",\"unnamed\")}')
" 2>/dev/null
```

**قائمة فحص CI/CD:**
- [ ] `npm run lint` في الـ CI
- [ ] `npm run test` في الـ CI
- [ ] `npm audit` أو أداة CVE scan
- [ ] `npx tsc --noEmit` في الـ CI
- [ ] Build check (`npm run build`)
- [ ] لا يوجد `--skip-checks` أو `--force` في أي خطوة

### 7.2 فحص الـ Deployment
```bash
# Vercel
cat vercel.json 2>/dev/null

# Docker
cat Dockerfile 2>/dev/null | head -30
# هل non-root user؟
grep -i "USER\|user " Dockerfile 2>/dev/null

# Environment Variables في الـ Deployment
grep -rn "process\.env\.\|import\.meta\.env\." \
  --include="*.ts" --include="*.tsx" \
  | grep -v node_modules | grep -v test \
  | awk -F'import.meta.env.|process.env.' '{print $2}' \
  | cut -d'"' -f1 | cut -d')' -f1 | cut -d' ' -f1 \
  | sort -u | head -20
```

### 7.3 فحص الـ Dependencies
```bash
# Outdated packages
cat package.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
all_deps = {**d.get('dependencies',{}), **d.get('devDependencies',{})}
print(f'Total packages: {len(all_deps)}')
# packages قديمة أو مشبوهة
old_patterns = ['moment', 'request', 'underscore', 'jquery', 'bower']
for p in old_patterns:
    if p in all_deps: print(f'⚠️  قديم: {p} ({all_deps[p]})')
"

# هل يوجد package-lock.json أو yarn.lock (مهم للأمان)
ls package-lock.json yarn.lock pnpm-lock.yaml 2>/dev/null || echo "❌ لا يوجد lock file"
```

---

## الخطوة 8 — الأداء والـ Bundle 📦

### 8.1 Bundle Analysis
```bash
# حجم الـ dist
du -sh dist/ 2>/dev/null || echo "لا يوجد build — شغّل npm run build أولاً"
find dist -name "*.js" | xargs du -sh 2>/dev/null | sort -rh | head -10
find dist -name "*.css" | xargs du -sh 2>/dev/null | sort -rh | head -5

# Code splitting
cat vite.config.ts 2>/dev/null | grep -A20 "manualChunks\|chunkSizeWarning"
```

### 8.2 Lighthouse Report
```bash
# إذا وُجد lighthouse report
cat lighthouse-report*.json 2>/dev/null | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    cats = d.get('categories',{})
    for name, val in cats.items():
        score = val.get('score',0) * 100
        icon = '✅' if score >= 90 else '🟡' if score >= 70 else '❌'
        print(f'{icon} {name}: {score:.0f}/100')
except: pass
" 2>/dev/null
```

### 8.3 فحص الأداء في الكود
```bash
# صور بدون WebP/AVIF
grep -rn "\.png\|\.jpg\|\.jpeg" --include="*.tsx" --include="*.ts" \
  | grep -v node_modules | grep -v test | head -10

# Large lists بدون virtualization
grep -rn "\.map(" --include="*.tsx" \
  | grep -v node_modules | wc -l

# Service Worker / PWA
cat public/manifest.json 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('PWA Name:', d.get('name','❌ missing'))
print('Theme Color:', d.get('theme_color','❌ missing'))
print('Display:', d.get('display','❌ missing'))
print('Icons:', len(d.get('icons',[])), 'icons')
" 2>/dev/null
```

---

## الخطوة 9 — التقرير النهائي 📋

بعد الانتهاء من جميع الخطوات، قدّم التقرير بهذا الشكل الكامل:

```markdown
# 🔬 تقرير المراجعة الشاملة — [اسم المشروع]

**التاريخ:** [تاريخ اليوم]
**التقنيات:** [React X / TypeScript / Supabase / إلخ]
**حجم المشروع:** [X ملف / Y سطر]
**مراجع:** Full Application Review Skill

---

## الملخص التنفيذي (3-5 جمل)
[وصف دقيق للوضع العام — نقاط القوة الرئيسية + المشاكل الأبرز]

---

## درجة التقييم الكلية: X.X/10

| الجانب              | الدرجة | الوضع | ملاحظة سريعة |
|---------------------|--------|-------|--------------|
| Frontend            | X/10   | 🟢/🟡/🔴 | ... |
| Backend / RPC       | X/10   | 🟢/🟡/🔴 | ... |
| قاعدة البيانات       | X/10   | 🟢/🟡/🔴 | ... |
| الأمان              | X/10   | 🟢/🟡/🔴 | ... |
| جودة الكود          | X/10   | 🟢/🟡/🔴 | ... |
| Testing             | X/10   | 🟢/🟡/🔴 | X% coverage — X ملف |
| DevOps / CI         | X/10   | 🟢/🟡/🔴 | ... |
| الأداء              | X/10   | 🟢/🟡/🔴 | ... |

---

## 🚨 ثغرات أمنية حرجة (يجب إصلاحها قبل أي شيء)
## [CRITICAL] ثغرات أمنية — تُمكّن من الاختراق أو سرقة البيانات
[إذا لم توجد اكتب: "✅ لا توجد ثغرات CRITICAL"]

### [CRITICAL] ثغرة 1: [الاسم]
- **الموقع:** `الملف:السطر`
- **الأثر:** [ما الذي يمكن أن يحدث بالضبط؟]
- **الاستغلال:** [كيف يمكن استغلالها؟]
- **الحل الكامل:**
  ```sql / ts / bash
  [كود الإصلاح الكامل]
  ```

---

## [HIGH] مشاكل عالية — تؤثر على سلامة البيانات أو الخدمة

### [HIGH] `الملف:السطر` — [وصف المشكلة]
**السبب:** [لماذا هذه مشكلة؟]
**الأثر:** [ما الذي يمكن أن يحدث؟]
**الحل:**
```[language]
[كود الإصلاح]
```

---

## [MEDIUM] مشاكل متوسطة — تؤثر على الجودة أو تفتح باباً للمشاكل

1. `[الملف:السطر]` — [المشكلة] → [الحل المختصر]
2. `[الملف:السطر]` — [المشكلة] → [الحل المختصر]

---

## [LOW] تحسينات وكود ميت — لا تؤثر على الوظيفة الآن

1. [الاقتراح / الكود الميت] → [الفائدة المتوقعة]

---

## ✅ نقاط القوة البارزة

1. [نقطة قوة محددة — ليس مديحاً عاماً]
2. [نقطة قوة محددة]

---

## 📊 إحصاءات المشروع

| المقياس | القيمة |
|---------|--------|
| إجمالي الملفات | X |
| إجمالي الأسطر | X |
| ملفات الـ Tests | X |
| Test Coverage | X% |
| TODO/FIXME في الكود | X |
| any usage | X |
| Dead Code files | X |
| Layer Violations | X |
| أكبر ملف | [الاسم] (X سطر) |

---

## 🗓️ خطة العمل المقترحة

### هذا الأسبوع (حرج)
- [ ] [المهمة] — الوقت المتوقع: [X دقيقة/ساعة]

### الأسبوع القادم (مهم)
- [ ] [المهمة]

### الشهر القادم (تحسين)
- [ ] [المهمة]
```

---

## 🔀 شجرة القرار السريع

```
هل وُجد .env حقيقي في الـ repo؟
├── نعم → 🚨 أبلغ فوراً في أول التقرير + تعليمات تغيير الـ key
└── لا  → ✅ أكمل

هل وُجد USING (true) على جدول حساس للـ anon؟
├── تحقق أولاً: هل يوجد DROP POLICY لها في migration أحدث؟
│   ├── نعم → ✅ تم الإصلاح، اذكره كإصلاح سابق
│   └── لا  → 🚨 ثغرة حرجة، أبلغ فوراً

هل الـ coverage < 50%؟
├── نعم → 🔴 اذكره كمشكلة حرجة
└── لا  → قيّم وفق النسبة الفعلية

هل CI يخلو من lint أو test؟
├── نعم → 🟡 أضف التوصية
└── لا  → ✅

هل وُجد ملف > 500 سطر في الـ presentation layer؟
├── نعم → 🟡 اقترح تقسيمه
└── لا  → ✅

هل وُجد unsafe-eval في CSP؟
├── نعم → 🔴 أبلغ عنه
└── لا  → ✅

هل وُجد import من domain → infrastructure أو domain → presentation?
├── نعم → [HIGH] Layer Violation — يجب الإصلاح
└── لا  → ✅ Clean Architecture محترم

هل وُجد ملفات بدون أي import يشير إليها؟
├── نعم → [LOW] Dead Code — رشّح للحذف بعد تحقق يدوي
└── لا  → ✅

هل وُجد circular dependency؟
├── نعم → [HIGH] يسبب مشاكل في الـ build و tree-shaking
└── لا  → ✅
```

---

## 📌 نماذج الحلول الجاهزة

### إصلاح slot_locks للـ DoS
```sql
DROP POLICY IF EXISTS "slot_locks_open" ON slot_locks;

CREATE POLICY "slot_locks_anon_insert" ON slot_locks
  FOR INSERT TO anon
  WITH CHECK (
    expires_at > NOW() AND
    expires_at < NOW() + INTERVAL '15 minutes'
  );

CREATE POLICY "slot_locks_anon_select" ON slot_locks
  FOR SELECT TO anon
  USING (expires_at > NOW());

CREATE POLICY "slot_locks_anon_delete" ON slot_locks
  FOR DELETE TO anon
  USING (session_id = current_setting('request.headers', true)::json->>'x-session-id');
```

### إصلاح CSV Injection في Excel Export
```typescript
function escapeCell(value: string): string {
  if (!value) return '';
  // منع formula injection في Excel
  if (['+', '-', '=', '@', '\t', '\r'].includes(value[0])) {
    return `'${value}`; // prefix بـ apostrophe
  }
  return value;
}

// الاستخدام في export:
const rows = patients.map(p => ({
  'الاسم': escapeCell(p.fullName),
  'رقم الهاتف': escapeCell(p.phone),
}));
```

### إضافة Lint و Audit للـ CI
```yaml
# أضف في .github/workflows/ci.yml
- name: Lint
  run: npm run lint

- name: Security Audit
  run: npm audit --audit-level=high
  continue-on-error: true

- name: Build Check
  run: npm run build
```

### إصلاح RLS على audit_logs
```sql
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- فقط super_admin و admin يقرؤون
CREATE POLICY "audit_logs_admin_read" ON audit_logs
  FOR SELECT TO authenticated
  USING (get_my_role() IN ('admin', 'super_admin'));

-- لا أحد يكتب مباشرة — فقط عبر SECURITY DEFINER function
-- (لا تُنشئ INSERT policy)
```

### إزالة unsafe-eval من CSP
```json
// vercel.json — قبل
"script-src 'self' 'unsafe-inline' 'unsafe-eval' https://*.supabase.co"

// بعد (React 19 لا يحتاج unsafe-eval)
"script-src 'self' 'unsafe-inline' https://*.supabase.co"
```