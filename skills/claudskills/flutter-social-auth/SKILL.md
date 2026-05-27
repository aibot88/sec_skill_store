---
name: "implementing-flutter-social-auth"
description: "Social authentication and OAuth/SSO for Flutter supporting Google Sign-In, Apple Sign-In, Facebook Login, and LINE Login. Use when implementing social login, OAuth flows, sign-in with Google/Apple/Facebook/LINE, SSO integration, third-party authentication, platform credential configuration (SHA-1 fingerprint for Android, Service ID for Apple, App ID for Facebook, Channel ID for LINE), native auth flows, minimal viable examples, error handling patterns, or troubleshooting authentication failures, token handling, and sign-in errors (ApiException, PlatformException)."
metadata:
  last_modified: "2026-04-01 14:35:00 (GMT+8)"
---

# Flutter Social Authentication Guide

## Goal
Implement secure, high-quality social authentication in Flutter applications across iOS, Android, and Web. This skill focuses on the most common identity providers (Google, Facebook, Apple) using best-practice plugins and native configuration strategies to ensure a seamless "Privacy-First" user experience.

## Process

### Phase 1: Provider Selection & Requirements
Identify the required social providers and gather necessary developer portal credentials.
- **Google**: Google Cloud Console / Firebase Console (SHA-1 fingerprint required for Android).
- **Facebook**: Meta for Developers (App ID, Client Token).
- **Apple**: Apple Developer Program (Service ID, Team ID, Key ID).
- **LINE**: LINE Developers Console (Channel ID).

### Phase 2: Platform-Specific Configuration
Each provider requires specific configurations in `AndroidManifest.xml`, `Info.plist`, or `web/index.html`.
- [Google Sign-In Setup](./references/google-sign-in.md)
- [Facebook Login Setup](./references/facebook-login.md)
- [Apple Sign-In Setup](./references/apple-sign-in.md)
- [LINE Login Setup](./references/line-login.md)

### Phase 3: Implementation & State Management
Integrate the authentication flow with the app's state management (e.g., Riverpod 3.0 Notifiers).
1. **Initialize**: Call the respective plugin `init` or configuration methods.
2. **Authenticate**: Trigger the login flow and capture the `AccessToken` or `IdToken`.
3. **Handle Persistence**: Store credentials securely using `flutter_secure_storage`.
4. **Error Handling**: Implement retry logic and display user-friendly error messages (e.g., ApiException 10 for Google).

---

## 📚 Documentation Library
Refer to these specialized resources for each identity provider:

- [🎯 Google Sign-In Best Practices](./references/google-sign-in.md)
- [👤 Facebook Login Best Practices](./references/facebook-login.md)
- [🍎 Apple Sign-In Best Practices](./references/apple-sign-in.md)
- [💬 LINE Login Best Practices](./references/line-login.md)

## Constraints
* **Native Overlays**: Always call `WidgetsFlutterBinding.ensureInitialized()` before initializing auth plugins in `main()`.
* **Security Awareness**: NEVER store raw AccessTokens in `SharedPreferences`. Use `Secure Storage` (encrypted).
* **Privacy Compliance**: Ensure Apple Sign-In is implemented if any other 3rd party social login is offered on iOS.
* **Error Resilience**: Always handle the `cancel` state gracefully when a user closes the auth popup.
