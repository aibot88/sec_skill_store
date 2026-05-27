---
name: wp-course-builder
description: "Skill chuyên dụng để tạo trang web khóa học WordPress hoàn chỉnh với custom theme: Google Auth, hệ thống bài học + video Drive bảo mật, VIP membership, khóa/mở bài, khuyến mãi, admin chuyên nghiệp. Đã thực chiến với dự án Goveoai Edu."
---

# 🎓 WordPress Course Website Builder

Skill toàn diện để xây dựng trang web khóa học WordPress chuyên nghiệp — đã kiểm chứng qua dự án thực tế **Goveoai Edu**.

## Khi nào sử dụng Skill này

- Tạo mới trang web khóa học / đào tạo trực tuyến
- Cần hệ thống LMS tự build (không phụ thuộc plugin LMS)
- Video bảo mật qua Google Drive (không download được)
- Google OAuth login (không cần username/password)
- Hệ thống VIP / membership thủ công hoặc tự động
- Khóa/mở bài học (bài đầu miễn phí, bài sau VIP)

---

## Cấu trúc theme chuẩn (Blueprint)

```
{theme-name}/
├── style.css                          # Theme metadata
├── functions.php                      # Core: setup, enqueue, roles, includes
├── header.php                         # Header + nav + user dropdown + login
├── footer.php                         # Footer + social + toast
├── front-page.php                     # Homepage (hero, promos, new, announcements, courses)
├── single-{cpt_name}.php             # Chi tiết khóa học (lessons accordion + sidebar)
├── single.php                         # Fallback single
├── page.php                           # Generic page
├── index.php                          # Archive fallback
├── search.php                         # Search results
├── 404.php                            # 404 page
│
├── inc/                               # PHP modules
│   ├── google-auth.php                # Google OAuth 2.0
│   ├── vip-membership.php             # VIP admin + approve/revoke
│   ├── drive-video.php                # Secure Drive embed
│   ├── course-manager.php             # Course CPT + Lesson CPT + meta
│   ├── customizer.php                 # Theme Customizer
│   ├── template-tags.php              # Helper functions (cards, breadcrumbs)
│   └── seo.php                        # Schema + OG Meta
│
├── page-templates/
│   ├── template-dashboard.php         # Student dashboard
│   └── template-courses.php           # Course listing + filter
│
└── assets/
    ├── css/
    │   ├── main.css                   # Design system (variables, base, components)
    │   ├── course.css                 # Course + lesson styles
    │   ├── dashboard.css              # Dashboard layout
    │   └── responsive.css             # Breakpoints
    └── js/
        ├── main.js                    # Core (animations, ajax, filters, toast)
        ├── navigation.js              # Mobile nav
        └── drive-player.js            # Video fullscreen + anti-download
```

---

## Bước 1: Khởi tạo Theme

### 1.1 style.css

```css
/*
 Theme Name: {Tên theme}
 Description: {Mô tả}
 Version: 1.0.0
 Author: {Tên}
 Text Domain: {text-domain}
 Requires PHP: 8.0
 Requires at least: 6.0
*/
```

### 1.2 functions.php — Cấu trúc core

```php
<?php
defined('ABSPATH') || exit;
define('THEME_VERSION', '1.0.0');
define('THEME_DIR', get_template_directory());
define('THEME_URI', get_template_directory_uri());

// Setup: title-tag, thumbnails, menus, custom-logo, html5
function theme_setup() {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_image_size('course-thumbnail', 400, 300, true);
    register_nav_menus(['primary' => 'Menu chính']);
}
add_action('after_setup_theme', 'theme_setup');

// Enqueue: Google Fonts, Material Icons, CSS, JS
function theme_scripts() {
    wp_enqueue_style('google-fonts', 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap', [], null);
    wp_enqueue_style('material-icons', 'https://fonts.googleapis.com/icon?family=Material+Icons+Round', [], null);
    wp_enqueue_style('main', THEME_URI . '/assets/css/main.css', [], THEME_VERSION);
    
    // Conditional loading
    if (is_singular('course_cpt') || is_front_page()) {
        wp_enqueue_style('course', THEME_URI . '/assets/css/course.css', ['main'], THEME_VERSION);
    }
    
    wp_enqueue_script('main', THEME_URI . '/assets/js/main.js', ['jquery'], THEME_VERSION, true);
    wp_localize_script('main', 'themeAjax', [
        'ajaxurl' => admin_url('admin-ajax.php'),
        'nonce'   => wp_create_nonce('theme_nonce'),
    ]);
}
add_action('wp_enqueue_scripts', 'theme_scripts');

// Includes
require THEME_DIR . '/inc/template-tags.php';
require THEME_DIR . '/inc/google-auth.php';
require THEME_DIR . '/inc/vip-membership.php';
require THEME_DIR . '/inc/drive-video.php';
require THEME_DIR . '/inc/course-manager.php';
require THEME_DIR . '/inc/customizer.php';
require THEME_DIR . '/inc/seo.php';

// Custom Roles
function theme_add_roles() {
    add_role('student', 'Học viên', ['read' => true]);
    add_role('vip_student', 'Học viên VIP', ['read' => true]);
    add_role('instructor', 'Giảng viên', ['read' => true, 'edit_posts' => true, 'publish_posts' => true, 'upload_files' => true]);
}
add_action('after_switch_theme', 'theme_add_roles');
```

---

## Bước 2: Hệ thống Course + Lesson (course-manager.php)

### 2.1 Hai Custom Post Types

**Nguyên tắc**: 1 Course → nhiều Lessons. Liên kết qua meta `_lesson_course_id`.

```php
// COURSE CPT
register_post_type('goveoai_course', [
    'labels'      => [...],
    'public'      => true,
    'has_archive' => true,
    'rewrite'     => ['slug' => 'khoa-hoc'],
    'supports'    => ['title', 'editor', 'thumbnail', 'excerpt'],
    'menu_icon'   => 'dashicons-welcome-learn-more',
]);

// LESSON CPT  
register_post_type('goveoai_lesson', [
    'labels'      => [...],
    'public'      => true,
    'rewrite'     => ['slug' => 'bai-hoc'],
    'supports'    => ['title', 'editor', 'thumbnail'],
    'menu_icon'   => 'dashicons-media-video',
]);
```

### 2.2 Course Meta Fields

| Meta Key | Mô tả | Type |
|---|---|---|
| `_price_type` | free / paid / vip | select |
| `_price` | Giá gốc (VNĐ) | number |
| `_sale_price` | Giá khuyến mãi | number |
| `_duration` | Thời lượng tổng | text |
| `_difficulty` | beginner / intermediate / advanced | select |
| `_instructor` | Tên giảng viên | text |
| `_free_lessons` | Số bài mở free (mặc định 3) | number |
| `_enrolled_count` | Số học viên | number |
| `_featured` | Nổi bật | checkbox |
| `_is_hot` | Hot badge | checkbox |
| `_is_new` | New badge | checkbox |
| `_promo_badge` | Text badge khuyến mãi (VD: "SALE 90%") | text |
| `_promo_expires` | Hạn khuyến mãi | date |
| `_announcement` | Thông báo nổi bật | textarea |

### 2.3 Lesson Meta Fields

| Meta Key | Mô tả | Type |
|---|---|---|
| `_lesson_course_id` | ID khóa học mẹ | select |
| `_lesson_order` | Thứ tự bài | number |
| `_lesson_video_url` | Link Google Drive | url |
| `_lesson_notes` | Ghi chú bài học | textarea |
| `_lesson_material` | Tài liệu đọc thêm (mỗi dòng 1 link/text) | textarea |
| `_lesson_duration` | Thời lượng video | text |
| `_lesson_access` | auto / free / vip | select |

### 2.4 Logic khóa/mở bài học

```
IF lesson_access === 'free'      → Luôn mở
IF lesson_access === 'vip'       → Luôn cần VIP
IF lesson_access === 'auto'      → Dựa theo số thứ tự:
   position <= _free_lessons     → Mở
   position > _free_lessons      → Cần VIP hoặc enrolled
```

**Ví dụ**: Khóa 15 bài, `_free_lessons = 3`:
- Bài 1-3: ✅ Mở cho tất cả
- Bài 4-15: 🔒 Cần VIP mới xem được video

### 2.5 Admin UI chuyên nghiệp

Trong edit Course, hiển thị:
- **Metabox thông tin** (giá, khuyến mãi, badges)
- **Metabox danh sách bài học** (hiển thị inline, có số thứ tự, badges Free/VIP, link edit)
- **Nút "Thêm bài học mới"** (link sang `post-new.php?post_type=lesson&course_id=X`)
- **Custom Admin Columns**: Giá, Số bài, Học viên, Badges

---

## Bước 3: Google OAuth 2.0 (google-auth.php)

### 3.1 Flow

```
User click "Đăng nhập bằng Google"
  → /google-login/ (custom rewrite rule)
  → Redirect to Google OAuth consent screen
  → Google callback → /google-callback/
  → Lấy user info (name, email, avatar)
  → Kiểm tra user tồn tại (by email)
     YES → wp_signon() → redirect dashboard
     NO  → wp_create_user() + set role 'student' + save avatar → redirect dashboard
```

### 3.2 Cấu hình cần thiết

| Cài đặt | Nơi lưu | Lấy từ |
|---|---|---|
| Google Client ID | Customizer | Google Cloud Console |
| Google Client Secret | Customizer | Google Cloud Console |
| Authorized redirect URI | Google Console | `https://domain.com/google-callback/` |

### 3.3 User Meta lưu từ Google

```php
update_user_meta($user_id, 'google_id', $google_user['sub']);
update_user_meta($user_id, 'google_avatar', $google_user['picture']);
update_user_meta($user_id, 'registered_via', 'google');
```

---

## Bước 4: VIP Membership (vip-membership.php)

### 4.1 Flow duyệt VIP

```
User click "Nâng cấp VIP" → AJAX request → set vip_status='pending'
  → Admin thấy trong admin menu: "VIP Chờ duyệt (X)"
  → Admin approve → set vip_status='active', vip_expires='2027-01-01'
  → Cron daily: kiểm tra expires → auto revoke nếu hết hạn
```

### 4.2 Admin Page

Custom admin page `VIP Members` với 3 tab:
- **Chờ duyệt**: List pending, nút Approve (chọn hạn: 30/90/365 ngày, vĩnh viễn)
- **Đang hoạt động**: List active VIPs với ngày hết hạn
- **Đã từ chối/hết hạn**: History

### 4.3 Check VIP function

```php
function is_vip($user_id = null) {
    if (!$user_id) $user_id = get_current_user_id();
    // Admin luôn VIP
    if (user_can($user_id, 'administrator')) return true;
    // Check status + expiry
    $status = get_user_meta($user_id, 'vip_status', true);
    $expires = get_user_meta($user_id, 'vip_expires', true);
    return $status === 'active' && (!$expires || strtotime($expires) > time());
}
```

---

## Bước 5: Video Google Drive (drive-video.php)

### 5.1 Cách embed bảo mật

```html
<iframe 
    src="https://drive.google.com/file/d/{FILE_ID}/preview"
    allowfullscreen
    sandbox="allow-scripts allow-same-origin"
    loading="lazy"
    referrerpolicy="no-referrer"
></iframe>
```

**Các lớp bảo vệ**:
1. **Preview mode**: Google Drive chỉ stream, không cho download link
2. **Sandbox iframe**: Chặn redirect ra ngoài
3. **Anti-right-click overlay**: Div vô hình chặn context menu
4. **No referrer**: Không lộ URL gốc
5. **CSS overlay**: Che nút download gốc của Drive

### 5.2 Extract Drive File ID

```php
function extract_drive_id($url) {
    if (preg_match('/\/d\/([a-zA-Z0-9_-]+)/', $url, $m)) return $m[1];
    if (preg_match('/[?&]id=([a-zA-Z0-9_-]+)/', $url, $m)) return $m[1];
    return null;
}
```

### 5.3 Tích hợp với Lesson

Mỗi lesson có meta `_lesson_video_url`. Trong template single course:
- Lesson mở → Hiển thị iframe
- Lesson khóa → Hiển thị "VIP wall" (gradient background + nút upgrade)

---

## Bước 6: Homepage (front-page.php)

### 6.1 Các section theo thứ tự

```
1. HERO         — CTA chính, stats (học viên, khóa học, giảng viên)
2. PROMOTIONS   — Khóa đang khuyến mãi (query _promo_badge != '')
3. NEW COURSES  — Khóa mới ra mắt (query _is_new = 1)
4. ANNOUNCEMENTS — Thông báo từ khóa (query _announcement != '')
5. ALL COURSES  — Grid toàn bộ với filter (free/vip/paid)
6. HOW IT WORKS — 3 bước bắt đầu
7. CTA          — Đăng ký / khám phá
```

### 6.2 Course Filter (Client-side JS)

```javascript
filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const filter = btn.dataset.filter;
        courseCards.forEach(card => {
            if (filter === 'all' || card.dataset.type === filter) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    });
});
```

---

## Bước 7: Trang chi tiết khóa học (single-{cpt}.php)

### 7.1 Layout

```
┌──────────────────────────────────────────────────────┐
│ HEADER: Thumbnail | Title, badges, meta, price, CTA │
├──────────────────────────────────────────────────────┤
│ BODY:                                                │
│ ┌────────────────────────┐  ┌──────────────────────┐ │
│ │ Giới thiệu khóa học    │  │ SIDEBAR:             │ │
│ │ (the_content)          │  │ Tổng quan            │ │
│ ├────────────────────────┤  │ - Số bài học          │ │
│ │ Danh sách bài học       │  │ - Bài miễn phí       │ │
│ │ ┌ Bài 1 [Free] ▼      │  │ - Thời lượng          │ │
│ │ │ 🎬 Video iframe      │  │ - Cấp độ              │ │
│ │ │ 📝 Ghi chú           │  │ - Học viên            │ │
│ │ │ 📖 Tài liệu          │  │ - Giảng viên          │ │
│ │ └──────────────────────┤  │                       │ │
│ │ ┌ Bài 2 [Free] ▶      │  │ [Login/VIP prompt]    │ │
│ │ ┌ Bài 3 [Free] ▶      │  └──────────────────────┘ │
│ │ ┌ Bài 4 [🔒VIP] ▶     │                           │
│ │ ┌ Bài 5 [🔒VIP] ▶     │                           │
│ └────────────────────────┘                           │
└──────────────────────────────────────────────────────┘
```

### 7.2 Lesson Accordion Logic

```javascript
function toggleLesson(lessonId, accessible) {
    const content = document.getElementById('lesson-content-' + lessonId);
    // Close all others
    document.querySelectorAll('.lesson-content').forEach(c => c.style.display = 'none');
    // Toggle this one
    content.style.display = content.style.display === 'none' ? 'block' : 'none';
}
```

---

## Bước 8: Dashboard Học viên (template-dashboard.php)

### 8.1 Tabs

| Tab | Nội dung |
|---|---|
| Tổng quan | Stats cards (enrolled, completed, VIP), danh sách khóa gần đây |
| Khóa học của tôi | Grid course cards đã enrolled |
| Tiến trình | Progress tracking (Phase 2) |
| Hồ sơ | Avatar, tên, email, ngày đăng ký, trạng thái VIP |

### 8.2 User Stats

```php
function get_user_stats($user_id) {
    $enrolled = get_user_meta($user_id, '_enrolled_courses', true) ?: [];
    return [
        'enrolled_count' => count($enrolled),
        'is_vip'         => is_vip($user_id),
        'vip_expires'    => get_user_meta($user_id, 'vip_expires', true),
        'enrolled_ids'   => $enrolled,
    ];
}
```

---

## Bước 9: CSS Design System

### 9.1 Design Tokens (CSS Variables)

```css
:root {
    /* Colors */
    --color-primary: #6366f1;
    --color-primary-dark: #4f46e5;
    --color-success: #10b981;
    --color-accent: #f59e0b;
    --color-error: #ef4444;
    --color-bg: #ffffff;
    --color-bg-alt: #f8fafc;
    --color-text: #1e293b;
    --color-text-muted: #64748b;
    --color-border: #e2e8f0;
    
    /* Typography */
    --font-heading: 'Plus Jakarta Sans', sans-serif;
    --font-body: 'Inter', sans-serif;
    
    /* Effects */
    --radius-lg: 0.75rem;
    --radius-xl: 1rem;
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    --transition-normal: 300ms ease;
    
    --header-height: 72px;
    --container-max: 1280px;
}
```

### 9.2 Key Components

| Component | Đặc điểm |
|---|---|
| **Header** | Fixed, glassmorphism (backdrop-filter blur), scroll shadow |
| **Course Card** | Hover lift (-4px), image zoom, gradient badges |
| **Lesson Item** | Accordion, numbered circles (blue=free, gray=locked) |
| **Buttons** | Gradient primary, outline, Google login SVG |
| **Toast** | Slide-in right, auto-dismiss, 4 types |
| **VIP Badge** | Gradient gold→red |

---

## Bước 10: SEO (seo.php)

### 10.1 Course Schema

```json
{
    "@type": "Course",
    "name": "...",
    "description": "...",
    "provider": { "@type": "Organization", "name": "..." },
    "offers": { "price": "...", "priceCurrency": "VND" }
}
```

### 10.2 Open Graph

```php
add_action('wp_head', function() {
    echo '<meta property="og:title" content="' . get_the_title() . '">';
    echo '<meta property="og:description" content="' . get_the_excerpt() . '">';
    echo '<meta property="og:image" content="' . get_the_post_thumbnail_url() . '">';
    echo '<meta property="og:type" content="website">';
});
```

---

## Checklist triển khai

Khi tạo dự án mới, follow thứ tự:

- [ ] **1.** Tạo `style.css` + `functions.php` (setup, enqueue, roles, includes)
- [ ] **2.** Tạo `inc/course-manager.php` (Course CPT + Lesson CPT + meta boxes)
- [ ] **3.** Tạo `inc/template-tags.php` (course_card, breadcrumbs, helpers)
- [ ] **4.** Tạo `inc/google-auth.php` (OAuth flow + rewrite rules)
- [ ] **5.** Tạo `inc/vip-membership.php` (admin page + approve/revoke + cron)
- [ ] **6.** Tạo `inc/drive-video.php` (embed + shortcode + anti-download)
- [ ] **7.** Tạo `assets/css/main.css` (design tokens + all components)
- [ ] **8.** Tạo `assets/css/course.css` + `dashboard.css` + `responsive.css`
- [ ] **9.** Tạo `header.php` + `footer.php`
- [ ] **10.** Tạo `front-page.php` (hero, promos, new, announcements, courses, CTA)
- [ ] **11.** Tạo `single-{cpt}.php` (chi tiết khóa + lessons accordion)
- [ ] **12.** Tạo `page-templates/template-dashboard.php` + `template-courses.php`
- [ ] **13.** Tạo `assets/js/main.js` + `navigation.js` + `drive-player.js`
- [ ] **14.** Tạo `search.php` + `404.php` + `page.php`
- [ ] **15.** Tạo `inc/customizer.php` + `inc/seo.php`
- [ ] **16.** Test: Google login, VIP flow, video embed, course enrollment

---

## Lưu ý quan trọng

### Permalink
Sau khi activate theme, vào `Settings > Permalinks > Post name` và Save để flush rewrite rules.

### Google OAuth
- Phải có SSL (HTTPS) để Google OAuth hoạt động
- Authorized redirect URI phải chính xác: `https://domain.com/google-callback/`
- State token chống CSRF

### Video Drive
- File Drive phải share "Anyone with the link can view"
- Preview mode không cho download nhưng user **có thể** screen record — đây là giới hạn vật lý
- Thêm CSS overlay che nút download gốc của Google Drive player

### VIP System
- Phase 1: Admin duyệt thủ công
- Phase 2: Tích hợp WooCommerce — mua gói VIP → auto approve
- Cron `goveoai_check_vip_expiry` chạy daily để auto revoke expired VIPs

### Admin UX
- Custom columns trong admin list (Giá, Bài học, Học viên, Badges)
- Badge khuyến mãi hiển thị trên card (promo_badge)
- Lesson manager inline trong edit Course

---

## Dự án tham khảo

### Goveoai Edu
- **Vị trí**: `c:\Users\Admin\Desktop\Dự án Riêng\Skill riêng\goveoai-edu\`
- **Style**: Tham khảo NDGroup Media (ndgroupmedia.com)
- **Tính năng**: Google Auth, VIP thủ công, Drive video, Free/Paid/VIP courses, Lesson lock/unlock
- **Ngày tạo**: 2026-04-05
