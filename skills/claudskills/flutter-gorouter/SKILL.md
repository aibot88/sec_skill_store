---
name: "routing-with-gorouter"
description: "Implements declarative Flutter routing using GoRouter v17 with URL-based navigation, deep linking, and authentication guards. Activates when configuring GoRoute path patterns, setting up StatefulShellRoute for persistent bottom navigation state, implementing ShellRoute for shared nested layouts, adding redirect guards with loop prevention (idempotent redirects), configuring deep links for iOS (FlutterDeepLinkingEnabled) or Android (intent-filters), debugging redirect loops or navigation stack issues, handling 404 error routes with errorBuilder, using named routes with path/query/extra parameters, or migrating from imperative Navigator.push to declarative routing. Ideal for Flutter web apps requiring URL bar synchronization, mobile apps with universal links or app links, or multi-level navigation hierarchies."
metadata:
  last_modified: "2026-04-27 17:41:00 (GMT+8)"
---

# GoRouter Declarative Navigation Guide (v17.x)

## Goal
Implement declarative routing using GoRouter, the official Flutter navigation solution. GoRouter provides URL-based navigation, deep linking support, and declarative route configuration ideal for web and mobile apps.

## Process

### Phase 1: Install Dependencies

```yaml
dependencies:
  go_router: ^17.2.0

dev_dependencies:
  go_router_builder: ^4.3.0  # Optional: for type-safe routes
```

### Phase 2: Define Routes

```dart
import 'package:go_router/go_router.dart';

final router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      name: 'home',
      builder: (context, state) => const HomeScreen(),
      routes: [
        // Nested route: /profile
        GoRoute(
          path: 'profile',
          name: 'profile',
          builder: (context, state) => const ProfileScreen(),
        ),
        // Parameterized route: /user/:id
        GoRoute(
          path: 'user/:id',
          name: 'user',
          builder: (context, state) {
            final userId = state.pathParameters['id']!;
            return UserScreen(userId: userId);
          },
        ),
      ],
    ),
    GoRoute(
      path: '/login',
      name: 'login',
      builder: (context, state) => const LoginScreen(),
    ),
  ],
);
```

### Phase 3: Use Router in App

```dart
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: router,
    );
  }
}
```

### Phase 4: Navigation

**Imperative Navigation**:
```dart
// Push by path
context.go('/profile');

// Push by name
context.goNamed('user', pathParameters: {'id': '123'});

// Push by name with query params
context.goNamed('search', queryParameters: {'q': 'flutter'});

// Pop
context.pop();

// Replace
context.pushReplacement('/login');
```

**Declarative Navigation** (recommended):
```dart
// Instead of buttons with onPressed
TextButton(
  onPressed: () => context.go('/profile'),
  child: Text('Go to Profile'),
)
```

### Phase 5: Persistent Bottom Navigation with StatefulShellRoute

```dart
final router = GoRouter(
  initialLocation: '/home',
  routes: [
    StatefulShellRoute.indexedStack(
      builder: (context, state, navigationShell) {
        return ScaffoldWithNavBar(navigationShell: navigationShell);
      },
      branches: [
        StatefulShellBranch(
          routes: [
            GoRoute(
              path: '/home',
              builder: (context, state) => const HomeScreen(),
            ),
          ],
        ),
        StatefulShellBranch(
          routes: [
            GoRoute(
              path: '/search',
              builder: (context, state) => const SearchScreen(),
            ),
          ],
        ),
        StatefulShellBranch(
          routes: [
            GoRoute(
              path: '/profile',
              builder: (context, state) => const ProfileScreen(),
            ),
          ],
        ),
      ],
    ),
  ],
);

class ScaffoldWithNavBar extends StatelessWidget {
  final StatefulNavigationShell navigationShell;
  
  const ScaffoldWithNavBar({required this.navigationShell});
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: navigationShell,
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: navigationShell.currentIndex,
        onTap: (index) => navigationShell.goBranch(index),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Search'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}
```

### Phase 6: Authentication Guards & Redirects

**CRITICAL: Prevent Redirect Loops**

Redirect callbacks MUST be idempotent — returning `null` when no redirect is needed. Infinite loops occur when redirect logic doesn't check the current location before redirecting.

**❌ BAD - Causes Infinite Loop:**
```dart
redirect: (context, state) {
  final isLoggedIn = AuthService.instance.isLoggedIn;
  
  // DANGER: Always redirects when not logged in, even if already at /login
  if (!isLoggedIn) {
    return '/login'; // Loop: /login → /login → /login...
  }
  
  return null;
}
```

**✅ GOOD - Idempotent Redirect:**
```dart
final router = GoRouter(
  redirect: (context, state) {
    final isLoggedIn = AuthService.instance.isLoggedIn;
    final currentPath = state.uri.toString(); // Use uri.toString() not matchedLocation
    
    // Only redirect IF needed (check current path first)
    if (!isLoggedIn && currentPath != '/login') {
      return '/login';
    }
    
    // Redirect to home if already logged in and trying to access login
    if (isLoggedIn && currentPath == '/login') {
      return '/';
    }
    
    // ALWAYS return null when no redirect needed
    return null;
  },
  refreshListenable: AuthService.instance, // Re-evaluate on auth change
  routes: [...],
);

class AuthService extends ChangeNotifier {
  static final instance = AuthService();
  
  bool _isLoggedIn = false;
  bool get isLoggedIn => _isLoggedIn;
  
  void login() {
    _isLoggedIn = true;
    notifyListeners(); // Triggers redirect re-evaluation
  }
  
  void logout() {
    _isLoggedIn = false;
    notifyListeners();
  }
}
```

**Redirect Best Practices:**
- Always check `state.uri.toString()` before redirecting
- Return `null` when no redirect is needed (not the current path)
- Use `state.uri.toString()` instead of `state.matchedLocation` for full URL including query params
- Test redirect logic by navigating to protected routes while logged out

### Phase 7: Deep Linking Configuration

Deep links allow external URLs to open specific screens in your app. GoRouter handles deep link routing automatically once platform configuration is complete.

#### iOS Deep Link Setup

**1. Enable Deep Linking (ios/Runner/Info.plist)**:
```xml
<!-- REQUIRED for GoRouter deep linking to work -->
<key>FlutterDeepLinkingEnabled</key>
<true/>

<!-- Custom URL scheme (myapp://...) -->
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>myapp</string>
        </array>
    </dict>
</array>
```

**2. Universal Links (Optional - for https://yourdomain.com links)**:
```xml
<key>com.apple.developer.associated-domains</key>
<array>
    <string>applinks:yourdomain.com</string>
</array>
```
Also requires `.well-known/apple-app-site-association` file on your server.

#### Android Deep Link Setup

**1. Intent Filters (android/app/src/main/AndroidManifest.xml)**:
```xml
<activity android:name=".MainActivity">
    <!-- Existing config... -->
    
    <!-- Custom URL scheme -->
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="myapp" android:host="example.com" />
    </intent-filter>
    
    <!-- HTTPS deep links (App Links) -->
    <intent-filter android:autoVerify="true">
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="https" android:host="yourdomain.com" />
    </intent-filter>
</activity>
```

**2. App Links Verification (Optional)**:
Requires `.well-known/assetlinks.json` on your server.

#### Deep Links to Nested Routes

**Problem:** Deep link `myapp://app/parent/child` opens at `/parent` instead of `/parent/child`.

**Solution:** Ensure route path structure matches URL structure exactly:

```dart
GoRoute(
  path: '/parent',
  builder: (context, state) => ParentPage(),
  routes: [
    // Nested path matches /parent/child
    GoRoute(
      path: 'child', // No leading slash - relative to parent
      builder: (context, state) => ChildPage(),
    ),
    // Parameterized nested route: /parent/child/:id
    GoRoute(
      path: 'child/:id',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return ChildDetailPage(id: id);
      },
    ),
  ],
),
```

**Test Deep Links:**
```bash
# iOS Simulator
xcrun simctl openurl booted "myapp://app/parent/child"

# Android
adb shell am start -W -a android.intent.action.VIEW \
  -d "myapp://app/parent/child" com.example.app
```

#### Deep Links with StatefulShellRoute

When using `StatefulShellRoute` for bottom navigation, deep links work but may reset the navigation stack within that branch:

```dart
StatefulShellRoute.indexedStack(
  builder: (context, state, navigationShell) {
    return ScaffoldWithNavBar(navigationShell: navigationShell);
  },
  branches: [
    StatefulShellBranch(
      routes: [
        GoRoute(
          path: '/home',
          builder: (context, state) => const HomeScreen(),
          routes: [
            // Deep link: myapp://app/home/details/123
            GoRoute(
              path: 'details/:id',
              builder: (context, state) {
                final id = state.pathParameters['id']!;
                return DetailsScreen(id: id);
              },
            ),
          ],
        ),
      ],
    ),
  ],
),
```

**Note:** The state within the home branch is preserved during normal navigation, but deep linking directly to `/home/details/123` creates a fresh navigation stack.

### Phase 8: Debugging Common Issues

#### Redirect Loop Debugging

**Symptoms:**
- App freezes on navigation
- Console shows repeated redirect messages
- Stack overflow errors

**Solution:**
Add logging to redirect callback to trace the loop:

```dart
redirect: (context, state) {
  final isLoggedIn = AuthService.instance.isLoggedIn;
  final currentPath = state.uri.toString();
  
  print('🔀 Redirect check: $currentPath (logged in: $isLoggedIn)');
  
  if (!isLoggedIn && currentPath != '/login') {
    print('➡️ Redirecting to /login');
    return '/login';
  }
  
  if (isLoggedIn && currentPath == '/login') {
    print('➡️ Redirecting to /');
    return '/';
  }
  
  print('✅ No redirect needed');
  return null;
}
```

Look for repeated identical log lines — that's your loop.

#### Deep Link Not Working

**Checklist:**
- [ ] iOS: `FlutterDeepLinkingEnabled` set to `true` in Info.plist
- [ ] Android: Intent filter includes all three required elements (action, category, data)
- [ ] Route path exactly matches deep link path structure
- [ ] Nested routes use relative paths (no leading slash)
- [ ] Test with simulator/emulator commands, not just tapping links
- [ ] Check `adb logcat` (Android) or Xcode console (iOS) for errors

#### 404 Error Routes

Handle unknown routes gracefully:

```dart
final router = GoRouter(
  routes: [...],
  errorBuilder: (context, state) => ErrorScreen(
    error: state.error,
    path: state.uri.toString(),
  ),
);

class ErrorScreen extends StatelessWidget {
  final Object? error;
  final String path;
  
  const ErrorScreen({required this.error, required this.path});
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Page Not Found')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.error_outline, size: 48),
            const SizedBox(height: 16),
            Text('The page "$path" could not be found.'),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => context.go('/'),
              child: const Text('Go Home'),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## Constraints

* **Declarative Only**: Avoid imperative Navigator.push. Use context.go/goNamed.
* **Path Parameters**: Always validate path parameters before use.
* **Web Compatibility**: All routes must maintain URL bar synchronization.
* **Redirect Loops**: ALWAYS check current path before redirecting; return `null` when no redirect needed.
* **Deep Link Testing**: Test on real devices/simulators, not just browsers.
* **State Preservation**: Use StatefulShellRoute for tabs to preserve state.
* **Nested Routes**: Use relative paths (no leading `/`) for child routes.
