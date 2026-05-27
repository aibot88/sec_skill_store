---
name: auth-implement
description: "Node.js Express 백엔드의 JWT 인증 시스템을 구현하는 스킬. 'auth 구현', '로그인 만들어줘', '회원가입 API', 'JWT 미들웨어', '인증 시스템 구현'처럼 인증/계정 관련 구현을 요청하면 이 스킬을 사용할 것. auth-builder 에이전트가 사용한다."
---

# Auth Implement Skill — JWT 인증 시스템 구현

## 역할
auth-builder 에이전트가 사용. SQLite + JWT + bcrypt 기반의 인증 시스템을 구현한다.

## 구현 순서
1. `_workspace/01_architect_*.md` 읽기 (설계 문서 확인)
2. `npm init -y` + 의존성 설치
3. DB 초기화 모듈 작성
4. User 모델 작성
5. JWT 미들웨어 작성
6. auth 라우터 작성
7. Express 앱 진입점 작성

## 구현 가이드

### 의존성 설치
```bash
npm install express better-sqlite3 jsonwebtoken bcryptjs dotenv node-fetch
npm install --save-dev nodemon
```

### `src/db/init.js` 패턴
```js
const Database = require('better-sqlite3');
const path = require('path');

const DB_PATH = process.env.DB_PATH || './data/app.db';
const db = new Database(DB_PATH);

db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');  // FK 강제 적용 필수

function initDB() {
  db.exec(`
    CREATE TABLE IF NOT EXISTS users ( ... );
    CREATE TABLE IF NOT EXISTS calendar_events ( ... );
    CREATE TABLE IF NOT EXISTS todos ( ... );
  `);
}

module.exports = { db, initDB };
```

### `src/middleware/auth.js` 패턴
```js
const jwt = require('jsonwebtoken');

function verifyToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // "Bearer <token>"
  if (!token) return res.status(401).json({ success: false, error: '인증 토큰이 없습니다' });

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded; // { userId, email }
    next();
  } catch (e) {
    return res.status(401).json({ success: false, error: '유효하지 않은 토큰입니다' });
  }
}

module.exports = { verifyToken };
```

### `src/routes/auth.js` 패턴
- `POST /api/auth/register`: email + password → bcrypt 해시 → DB insert → JWT 반환
- `POST /api/auth/login`: email + password → DB 조회 → bcrypt compare → JWT 반환
- 토큰 만료: `expiresIn: '7d'`

### `src/app.js` 패턴
```js
require('dotenv').config();
const express = require('express');
const { initDB } = require('./db/init');

const app = express();
app.use(express.json());

initDB(); // 서버 시작 시 테이블 생성

app.use('/api/auth', require('./routes/auth'));
// 피처 라우터는 feature-builder가 추가

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`서버 실행 중: http://localhost:${PORT}`));
```

### `.env.example`
```
PORT=3000
DB_PATH=./data/app.db
JWT_SECRET=your-secret-key-here
WEATHER_API_KEY=your-openweathermap-api-key
```

## 완료 기준
- `node src/app.js` 실행 시 서버가 시작되고 DB 파일이 생성됨
- `POST /api/auth/register`로 계정 생성 성공
- `POST /api/auth/login`으로 JWT 토큰 수신 성공
- 잘못된 비밀번호로 로그인 시 401 반환
