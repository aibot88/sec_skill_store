---
name: framework-source-security-analyzer
description: "프레임워크와 언어의 소스코드 및 개발자 가이드를 직접 분석하여 메타적 보안 구조를 파악하는 스킬. Spring의 mass assignment, Java getHost()의 URL Confusion처럼 프레임워크/언어 설계상의 보안 함의를 소스코드 레벨에서 추출한다. GitHub 소스, 공식 문서, 보안 가이드를 직접 조회하고, 아키텍처 패턴-취약점 매핑을 생성한다. 대상: Spring, Django, Rails, Express, ASP.NET 등 프레임워크와 Java, Python, JavaScript, C# 등 언어의 표준 라이브러리. '프레임워크 보안 분석', '소스코드 보안 분석', '메타 구조 취약점', '언어 설계 취약점' 같은 표현에 트리거된다."
---

# Framework Source Security Analyzer

프레임워크와 언어의 **소스코드와 개발자 가이드를 직접 분석**하여 메타적 보안 구조와 설계상 취약점을 파악하는 스킬이다.

일반적인 보안 가이드와의 차이점: 개별 취약점이 아닌, 프레임워크/언어의 **설계 철학과 아키텍처 패턴**이 어떻게 보안 취약점으로 이어지는지를 소스코드 레벨에서 분석한다.

## 핵심 원칙

```
"왜 이 프레임워크는 이런 방식으로 설계되었는가?"
"이 편의성/추상화가 어떤 보안 리스크를 숨기는가?"
"개발자가 의도치 않게 범하는 실수는 어디서 오는가?"
```

---

## 작업 흐름 개요

```
1. 대상 식별      → 어떤 프레임워크/언어/라이브러리를 분석할 것인가
2. 위협 조사      → CVE, 보안 연구, 실제 공격 사례 수집
3. 소스 분석      → GitHub 소스코드, 공식 문서, 개발자 가이드 조회
4. 메타 패턴 추출 → 설계 패턴과 보안 취약점의 구조적 관계 매핑
5. 문서 생성      → 프레임워크별 보안 아키텍처 분석 보고서
```

---

## 1단계: 대상 식별과 범위 설정

### 분석 대상 카테고리

**A. 웹 프레임워크**
- Backend: Spring (Java), Django (Python), Rails (Ruby), Express (Node.js), ASP.NET (C#), Laravel (PHP), FastAPI (Python)
- Frontend: React, Vue, Angular, Next.js, Nuxt.js

**B. 언어 표준 라이브러리**
- Java: `java.net.URL`, `java.io`, `java.security`, serialization
- Python: `pickle`, `eval`, `exec`, `os`, `subprocess`
- JavaScript/Node.js: `eval`, `vm`, `child_process`, URL parsing
- C#: `System.Net`, `System.Xml`, deserialization

**C. ORM/데이터 접근 레이어**
- Hibernate, JPA, SQLAlchemy, ActiveRecord, Entity Framework, Sequelize, TypeORM

**D. 보안/인증 라이브러리**
- Spring Security, Passport.js, Django Auth, ASP.NET Identity, JWT libraries

**E. 직렬화/파싱 라이브러리**
- Jackson, Gson, PyYAML, XML parsers, JSON parsers

### 범위 설정

하나의 분석에서 다루는 범위:
- **단일 컴포넌트 심층 분석**: 예) Spring Data Binding, Jackson deserialization
- **프레임워크 전체 아키텍처**: 예) Spring Framework 전체의 보안 메타 구조
- **언어별 위험 패턴**: 예) Java Deserialization 생태계 전체

**범위 결정 기준**: 10-20개의 메타 패턴을 식별할 수 있는 크기가 적절

---

## 2단계: 위협 조사 (Threat Intelligence)

프레임워크/언어 특화 위협 정보를 수집한다.

### 검색 전략

#### 카테고리 A: 프레임워크별 CVE와 취약점
```
검색어 패턴:
  "{프레임워크} CVE 2023 2024 2025"
  "{프레임워크} security vulnerability"
  "{프레임워크} {컴포넌트} exploit"
  
예시:
  "Spring Boot CVE 2024"
  "Django ORM SQL injection"
  "Express.js prototype pollution"
  
목적: 프레임워크의 실제 취약점 역사 파악
```

#### 카테고리 B: 프레임워크 설계 결함 연구
```
검색어 패턴:
  "{프레임워크} security design flaw"
  "{프레임워크} insecure defaults"
  "{프레임워크} security architecture"
  
예시:
  "Spring mass assignment vulnerability"
  "Rails parameter binding security"
  "Django template injection"
  
목적: 개별 버그가 아닌 구조적 설계 문제 식별
```

#### 카테고리 C: 언어 레벨 취약점
```
검색어 패턴:
  "{언어} {기능} security vulnerability"
  "{언어} deserialization attack"
  "{언어} URL parsing confusion"
  
예시:
  "Java getHost URL confusion"
  "Python pickle deserialization"
  "JavaScript prototype pollution"
  
목적: 언어 설계 자체의 보안 함의
```

#### 카테고리 D: 컨퍼런스 발표 및 연구
```
검색어 패턴:
  "{프레임워크} security BlackHat OWASP"
  "{프레임워크} attack research paper"
  
목적: 체계적 공격 분류 및 신규 공격 벡터
```

#### 카테고리 E: 실무 보안 패턴
```
검색어 패턴:
  "{프레임워크} security best practices"
  "{프레임워크} secure coding guide"
  "{프레임워크} security checklist OWASP"
  
목적: 실무에서 자주 발생하는 잘못된 사용 패턴
```

### 위협 정보 정리

다음 항목을 추출하여 정리:

```markdown
## 위협 조사 결과

### 알려진 취약점 패턴
- [Mass Assignment, SQL Injection, Template Injection 등]

### 주요 CVE 및 사건
| CVE | 연도 | 영향 | 근본 원인 |
|-----|------|------|----------|
| CVE-XXXX-YYYY | 2024 | ... | Framework design flaw |

### 구조적 설계 문제
- [프레임워크의 철학/추상화가 숨기는 보안 리스크]

### 실무 오용 패턴
- [개발자가 자주 범하는 실수와 그 원인]

### 조사할 소스 위치
- [GitHub 리포지토리, 문서 URL, 핵심 코드 파일]
```

---

## 3단계: 소스코드 직접 분석 (Source Deep Dive)

이 단계가 **이 스킬의 핵심 차별점**이다.

### 소스 분석 대상

#### A. GitHub 소스코드
```
web_fetch를 사용하여 실제 구현 코드 조회:
  https://github.com/{org}/{repo}/blob/main/{path}
  
주요 분석 대상:
  - 핵심 보안 로직 (인증, 권한, 검증)
  - 데이터 바인딩/파싱 로직
  - 기본값(defaults) 설정
  - 보안 관련 어노테이션/데코레이터
```

#### B. 공식 개발자 가이드
```
프레임워크 공식 문서:
  - Security Guide
  - Best Practices
  - Configuration Reference
  - Migration Guide (보안 변경 사항)
```

#### C. 이슈 트래커 및 커밋 히스토리
```
보안 패치 커밋에서 학습:
  - 어떤 설계가 문제였는가
  - 어떻게 수정되었는가
  - Breaking change인가 호환성 유지인가
```

### 소스 분석 시 추출할 패턴

#### 패턴 1: Insecure Defaults (불안전한 기본값)
```java
// 예시: Spring Boot의 기본 설정
@ConfigurationProperties
public class ServerProperties {
    // 기본값이 보안에 미치는 영향
    private boolean exposeErrorDetails = true; // 개발 편의 vs 정보 노출
}
```

**추출 내용**:
- 기본값이 무엇인가
- 왜 이 기본값인가 (편의성, 호환성, 성능 등)
- 보안 리스크는 무엇인가
- 안전하게 변경하는 방법

#### 패턴 2: Implicit Trust (암묵적 신뢰)
```python
# 예시: Django ORM
class User(models.Model):
    # 필드가 자동으로 바인딩됨
    is_admin = models.BooleanField(default=False)
    
# 개발자가 의도하지 않은 필드가 업데이트될 수 있음
```

**추출 내용**:
- 프레임워크가 무엇을 "자동"으로 처리하는가
- 어떤 입력을 신뢰하는가
- 신뢰 경계(trust boundary)는 명확한가

#### 패턴 3: Abstraction Leaks (추상화 누수)
```javascript
// Express.js의 body-parser
app.use(express.json());
// 내부적으로 JSON.parse() 사용
// → prototype pollution 가능
```

**추출 내용**:
- 추상화가 숨기는 저수준 동작
- 저수준 취약점이 추상화를 통해 노출되는 경로
- 개발자가 인지하기 어려운 보안 결정

#### 패턴 4: Confused Deputy (혼동된 대리인)
```java
// Java URL.getHost()
URL url = new URL("http://example.com@attacker.com");
String host = url.getHost(); // "attacker.com" 반환
// 하지만 브라우저는 example.com으로 해석할 수 있음
```

**추출 내용**:
- 같은 데이터를 다르게 해석하는 컴포넌트
- 파싱 불일치로 인한 보안 우회
- 표준 불일치 또는 모호성

#### 패턴 5: Serialization Hazards (직렬화 위험)
```java
// Java ObjectInputStream
ObjectInputStream ois = new ObjectInputStream(input);
Object obj = ois.readObject(); // RCE 위험
```

**추출 내용**:
- 직렬화 포맷의 메타데이터 신뢰
- Type confusion 가능성
- 역직렬화 시 자동 실행되는 코드 (gadgets)

#### 패턴 6: Template Injection Surface
```python
# Django/Jinja2
template = Template("Hello {{ name }}")
# 사용자 입력이 템플릿 컨텍스트에 들어가면?
```

**추출 내용**:
- 템플릿 엔진의 표현식 평가 능력
- Sandbox 탈출 방법
- 안전한 컨텍스트 분리 방법

### 소스 읽기 실행 방법

```
1. web_search로 GitHub 리포지토리 찾기
2. web_fetch로 핵심 소스 파일 조회
   - Security 관련 클래스/모듈
   - Configuration defaults
   - 데이터 바인딩/파싱 로직
3. 공식 문서의 Security 섹션 조회
4. 2단계에서 식별한 CVE의 패치 커밋 확인
5. 코드와 문서 간 불일치 식별
```

**중요**: 소스코드 인용 시 GitHub 링크와 파일명, 라인 번호 명시
예: `SpringMVC DataBinder.java:245` 또는 링크

---

## 4단계: 메타 패턴 추출 (Meta-Pattern Analysis)

개별 취약점이 아닌, **프레임워크의 철학과 설계가 만드는 보안 구조**를 추출한다.

### 분석 프레임워크

각 메타 패턴에 대해:

```markdown
### [번호]. [메타 패턴 이름] ([프레임워크/언어])

**설계 철학**: 이 패턴이 왜 존재하는가 (편의성, 성능, 추상화 등)

**구현 메커니즘**: 
- 소스코드 레벨에서 어떻게 구현되는가
- 관련 클래스/함수/모듈 (소스 링크)

**보안 함의**: 이 설계가 만드는 보안 리스크

**공격 벡터**:
- 구체적 공격 시나리오
- 코드 예제 (취약한 코드 vs 안전한 코드)

**실제 사례**: CVE, 보안 사건

**근본 원인 분석**: 
- 왜 이렇게 설계되었는가
- 대안은 무엇이었는가
- 왜 이 대안을 선택하지 않았는가

**완화 방법**: 
- 프레임워크 설정 변경
- 코드 패턴 변경
- 추가 보안 레이어
```

### 메타 패턴 카탈로그

다음은 자주 발견되는 메타 패턴들이다:

#### 1. Convenience over Safety (편의성 > 안전성)
```
프레임워크가 개발 속도를 위해 보안을 희생한 설계
예: Auto-binding, Magic methods, Implicit conversions
```

#### 2. Backward Compatibility Tax (하위 호환성 부담)
```
레거시 지원을 위해 불안전한 기능 유지
예: Insecure defaults maintained, Deprecated but available
```

#### 3. Abstraction Opacity (불투명한 추상화)
```
추상화가 보안 결정을 숨김
예: ORM SQL generation, Template auto-escaping assumptions
```

#### 4. Implicit Trust Boundaries (암묵적 신뢰 경계)
```
어디가 신뢰/비신뢰 경계인지 명확하지 않음
예: Request parameter auto-binding, Session data assumptions
```

#### 5. Serialization as API (직렬화를 API로 사용)
```
직렬화 포맷을 통신/저장 포맷으로 사용
예: Java Serialization, Python Pickle, .NET BinaryFormatter
```

#### 6. Parser Differential (파서 불일치)
```
같은 입력을 다르게 해석하는 컴포넌트들
예: URL parsing differences, HTTP header interpretation
```

#### 7. Magic Method Invocation (매직 메소드 실행)
```
프레임워크가 자동으로 호출하는 메소드들
예: __wakeup(), __destruct(), lifecycle hooks
```

#### 8. Configuration Complexity (설정 복잡성)
```
보안 설정이 너무 복잡하여 실수 유발
예: Spring Security DSL, CORS configuration
```

#### 9. Defaults for Development (개발용 기본값)
```
개발 편의를 위한 기본값이 프로덕션에 유지됨
예: Debug mode, Error details, Sample credentials
```

#### 10. Framework Lock-in Risk (프레임워크 종속 리스크)
```
프레임워크의 보안 메커니즘에만 의존
예: Framework-only validation, Built-in auth only
```

---

## 5단계: 문서 생성

### 출력 형식

```markdown
# {프레임워크/언어} 소스코드 보안 분석: 메타 구조 직접 추출

> **분석 대상**: [프레임워크/언어 버전]
> **소스 조사**: [GitHub 리포지토리, 문서 URL]
> **분석 시점**: [날짜]
> **주요 CVE 반영**: [CVE 범위]

---

## Executive Summary

[3-5문장으로 핵심 발견사항 요약]

---

## 제1부: 프레임워크 설계 철학과 보안 트레이드오프

### 1. [메타 패턴 1]
### 2. [메타 패턴 2]
...

## 제2부: 소스코드 레벨 취약 구조

### N. [메타 패턴 N]
...

## 제3부: 언어 레벨 설계 문제 (해당 시)

### Language-Specific Hazards
...

## 제4부: 최신 CVE 및 실제 공격 사례

| CVE | 연도 | 근본 원인 | 영향받는 버전 | 메타 패턴 |
|-----|------|----------|--------------|----------|
| ... | ... | ... | ... | ... |

---

## 부록 A: 메타 패턴 ↔ 공격 ↔ 방어 매핑표

| 메타 패턴 | 대표 취약점 | 공격 기법 | 소스 위치 | 완화 방법 |
|----------|------------|----------|----------|----------|
| ... | ... | ... | ... | ... |

## 부록 B: 소스코드 보안 체크리스트

**설정 검증**
- [ ] 프로덕션에서 debug mode 비활성화
- [ ] 에러 상세 정보 노출 비활성화
...

**코드 패턴 검증**
- [ ] Mass assignment 방지 (whitelist 사용)
- [ ] 직렬화 사용 시 type 검증
...

## 부록 C: 안전한 코드 패턴 예제

### 취약한 패턴 vs 안전한 패턴

```java
// VULNERABLE
@RequestMapping("/user")
public User updateUser(@ModelAttribute User user) {
    return userRepository.save(user); // Mass assignment!
}

// SECURE
@RequestMapping("/user")
public User updateUser(@RequestBody UserUpdateDTO dto) {
    User user = userRepository.findById(dto.getId());
    user.setEmail(dto.getEmail()); // Explicit field mapping
    user.setName(dto.getName());
    return userRepository.save(user);
}
```

## 부록 D: 프레임워크 버전별 보안 변경사항

| 버전 | 보안 변경 | Breaking Change | Migration |
|------|----------|----------------|-----------|
| ... | ... | ... | ... |
```

### 문서 품질 기준

- **메타 패턴 수**: 10-20개
- **소스코드 인용**: 각 패턴에 실제 소스 코드 링크 또는 인용
- **실용성**: 취약한 코드 vs 안전한 코드 비교 예제
- **매핑 테이블**: 메타 패턴↔공격↔방어 종합 매핑
- **체크리스트**: 즉시 적용 가능한 검증 리스트
- **언어**: 사용자 언어로 작성

### 파일 저장

```
/mnt/user-data/outputs/{프레임워크}_소스코드_보안분석.md
```

present_files로 사용자에게 제공

---

## 분석 깊이 조절

| 요청 수준 | 검색 횟수 | 소스 fetch | 메타 패턴 수 | 예시 |
|-----------|----------|-----------|------------|------|
| 간단 | 3-5회 | 2-4개 파일 | 5-8개 | "Spring MVC 보안 분석" |
| 보통 | 6-10회 | 5-10개 파일 | 10-15개 | "Spring Framework 전체 보안 구조" |
| 심층 | 10-20회 | 10-20개 파일 | 15-25개 | "Java 생태계 Deserialization 전체" |

---

## 프레임워크별 특화 가이드

### Spring Framework
```
핵심 분석 대상:
- Spring MVC: DataBinder, @ModelAttribute, @RequestBody
- Spring Security: SecurityContext, Authentication
- Spring Data: JPA, Query DSL, Projections
- Spring Boot: Auto-configuration, Actuator

소스 위치:
- github.com/spring-projects/spring-framework
- docs.spring.io/spring-framework/reference/

주요 메타 패턴:
- Mass Assignment via DataBinder
- SpEL Injection in expressions
- Actuator exposure
```

### Django
```
핵심 분석 대상:
- ORM: QuerySet, Model forms
- Template Engine: DTL, auto-escaping
- Middleware: Session, CSRF
- Settings: DEBUG, ALLOWED_HOSTS

소스 위치:
- github.com/django/django
- docs.djangoproject.com/

주요 메타 패턴:
- Mass Assignment via ModelForm
- Template injection via user templates
- Debug mode information disclosure
```

### Express.js
```
핵심 분석 대상:
- Middleware: body-parser, cookie-parser
- Routing: Route parameters, Query strings
- Template Engines: EJS, Pug

소스 위치:
- github.com/expressjs/express
- expressjs.com/

주요 메타 패턴:
- Prototype pollution via body-parser
- Path traversal in static file serving
- Template injection
```

### Java Standard Library
```
핵심 분석 대상:
- java.net.URL: Parsing, getHost()
- java.io: ObjectInputStream, Serialization
- java.security: XML parsers, XXE

소스 위치:
- github.com/openjdk/jdk
- docs.oracle.com/javase/

주요 메타 패턴:
- URL parsing confusion (getHost vs getAuthority)
- Deserialization RCE
- XXE in XML parsers
```

---

## 주의사항

### 소스 우선 원칙
- 블로그보다 실제 소스코드가 정확함
- 문서와 소스가 다를 경우 소스가 실제 동작임
- 버전별 차이 주의 (major.minor.patch)

### 설계 의도 이해
- "왜 이렇게 만들었는가"를 먼저 파악
- 보안과 다른 목표(성능, 호환성) 간 트레이드오프 이해
- 비난이 아닌 분석적 접근

### 실용성 중시
- 이론적 취약점보다 실제 exploit 가능성
- 완화 방법은 현실적이어야 함
- Breaking change vs 점진적 개선 고려

### 최신성
- 최근 2년 CVE 우선
- 최신 버전의 소스코드 기준
- Deprecated 기능 명시

### 저작권
- 소스코드 짧은 인용은 허용 (분석 목적)
- 긴 복사는 피하고 핵심만 발췌
- GitHub 링크 제공

---

## 참고 자료 (내부 사용)

### 주요 GitHub 리포지토리
- Spring: github.com/spring-projects/*
- Django: github.com/django/django
- Rails: github.com/rails/rails
- Express: github.com/expressjs/express
- ASP.NET: github.com/dotnet/aspnetcore

### 보안 데이터베이스
- NVD: nvd.nist.gov
- Snyk Vulnerability DB: snyk.io/vuln
- GitHub Security Advisories: github.com/advisories

### 연구 소스
- OWASP: owasp.org
- PortSwigger Research: portswigger.net/research
- BlackHat/DEF CON archives

### 공식 보안 가이드
- Spring Security Docs
- Django Security
- OWASP Framework Security
