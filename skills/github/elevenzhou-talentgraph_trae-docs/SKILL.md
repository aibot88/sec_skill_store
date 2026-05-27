# Next.js 项目服务器部署技能

## 技能描述

自动化部署 Next.js 项目到 Linux 服务器（Ubuntu/Debian），支持国内服务器 GitHub 镜像加速。

## 适用场景

- Next.js 14+ App Router 项目
- 使用 SQLite 数据库（better-sqlite3）
- 使用 NextAuth.js 认证
- 需要部署到腾讯云/阿里云等国内服务器

## 前置条件

- 服务器 SSH 访问权限（密钥或密码）
- 服务器 IP 地址
- 项目已推送到 GitHub 仓库

## 部署流程

### 1. 连接服务器并安装环境

```bash
# SSH 连接
ssh -i ~/.ssh/your-key.pem ubuntu@YOUR_SERVER_IP

# 安装 Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs build-essential

# 安装 PM2
sudo npm install -g pm2
```

### 2. 克隆项目（国内服务器使用镜像）

```bash
# 方式一：直接克隆（海外服务器）
git clone https://github.com/YOUR_REPO.git talentgraph

# 方式二：使用镜像（国内服务器）
git clone https://ghfast.top/https://github.com/YOUR_REPO.git talentgraph

cd talentgraph
```

### 3. 安装依赖

```bash
npm install
npm install --save-dev @types/better-sqlite3
```

### 4. 配置环境变量

```bash
cat > .env << 'EOF'
# NextAuth 配置
NEXTAUTH_URL=http://YOUR_SERVER_IP:3000
NEXTAUTH_SECRET=your-random-secret-key

# AI 服务配置
DEEPSEEK_API_KEY=your-deepseek-key
OPENAI_API_KEY=your-openai-key
EOF
```

### 5. 构建项目

```bash
npm run build
```

### 6. 启动服务

```bash
pm2 start npm --name talentgraph -- start
pm2 save
```

### 7. 开放防火墙端口

```bash
# Ubuntu UFW
sudo ufw allow 3000/tcp

# 或在云服务商控制台安全组中放行 3000 端口
```

## 常见构建问题及解决方案

### 问题 1: GitHub clone 超时

**原因**: 国内网络访问 GitHub 不稳定

**解决方案**: 使用镜像加速
```bash
git clone https://ghfast.top/https://github.com/YOUR_REPO.git
```

### 问题 2: `trustHost` 属性报错

**错误信息**: `Object literal may only specify known properties, and 'trustHost' does not exist in type 'NextAuthOptions'.`

**原因**: NextAuth v4 不支持 `trustHost` 属性（这是 v5 的 API）

**解决方案**: 移除 `trustHost: true` 配置

```diff
const handler = NextAuth({
  secret: process.env.NEXTAUTH_SECRET,
- trustHost: true,
  providers: [...]
})
```

### 问题 3: `Property 'role' does not exist on type 'User'`

**原因**: NextAuth 默认的 `User` 类型没有 `role` 字段

**解决方案**: 使用类型断言绕过

```typescript
// 在 authorize 回调中
return {
  id: user.id,
  name: user.name,
  email: user.email,
  role: user.role  // 直接返回
}

// 在 jwt 回调中
async jwt({ token, user }) {
  if (user) {
    token.userId = user.id
    ;(token as any).role = (user as any).role
  }
  return token
}

// 在 session 回调中
async session({ session, token }) {
  if (session.user) {
    (session.user as any).id = (token as any).userId
    ;(session.user as any).role = (token as any).role
  }
  return session
}
```

### 问题 4: `Request is not assignable to NextRequest`

**原因**: Next.js App Router 的 route handler 要求使用 `NextRequest` 类型

**解决方案**: 所有 API route 文件使用 `NextRequest`

```diff
- import { NextResponse } from 'next/server'
+ import { NextResponse, NextRequest } from 'next/server'

- export async function GET(req: Request) {
+ export async function GET(req: NextRequest) {
```

### 问题 5: `Cannot find module 'better-sqlite3'` 类型错误

**原因**: 缺少 TypeScript 类型声明

**解决方案**:
```bash
npm install --save-dev @types/better-sqlite3
```

### 问题 6: pdfjs-dist 构建失败

**错误信息**: `Failed to parse source file... Syntax Error`

**原因**: pdfjs-dist 的 worker 文件太大，SWC 无法解析

**解决方案**: 改用 CDN 加载 worker

```diff
- pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
-   'pdfjs-dist/build/pdf.worker.min.mjs',
-   import.meta.url
- ).href
+ pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.mjs`
```

### 问题 7: `NEXTAUTH_URL` 端口错误

**原因**: `.env` 文件中的 `NEXTAUTH_URL` 端口与实际运行端口不一致

**解决方案**: 确保 `NEXTAUTH_URL` 与服务器实际端口一致

```env
# 正确
NEXTAUTH_URL=http://124.222.221.3:3000

# 错误（端口不匹配）
NEXTAUTH_URL=http://124.222.221.3:3003
```

## 部署检查清单

- [ ] Node.js 18+ 已安装 (`node -v`)
- [ ] PM2 已安装并配置开机自启 (`pm2 startup`)
- [ ] `.env` 文件已创建
- [ ] `NEXTAUTH_URL` 指向正确的服务器地址和端口
- [ ] 防火墙/安全组已放行 3000 端口
- [ ] `npm run build` 构建成功
- [ ] PM2 进程运行正常 (`pm2 status`)
- [ ] 服务可访问 (`curl http://localhost:3000`)

## 常用运维命令

```bash
# 查看服务状态
pm2 status

# 查看日志
pm2 logs talentgraph

# 重启服务
pm2 restart talentgraph

# 停止服务
pm2 stop talentgraph

# 更新部署
cd ~/talentgraph
git pull origin master
npm run build
pm2 restart talentgraph
```

## 经验总结

1. **国内服务器部署优先使用镜像**: GitHub 直连在国内服务器上非常不稳定，`ghfast.top` 镜像可以大幅提高克隆成功率。

2. **NextAuth v4 类型问题**: NextAuth v4 的 TypeScript 类型定义不够完善，扩展 `User` 和 `Session` 类型时经常需要 `as any` 绕过。

3. **App Router 类型要求严格**: 所有 route handler 必须使用 `NextRequest`，否则类型检查会失败。

4. **better-sqlite3 需要编译环境**: 服务器上需要安装 `build-essential` 和 Python 才能编译原生模块。

5. **环境变量必须正确配置**: `NEXTAUTH_URL` 必须与实际访问地址一致，否则会导致登录后跳转错误。

6. **云服务商安全组**: 除了服务器防火墙，还需要在云服务商控制台的安全组中放行端口。
