---
name: ui-ux-settings-preferences-design
description: Design settings and preferences screens including account management, privacy controls, and platform-specific patterns
argument-hint: "<app or feature needing settings design>"
allowed-tools: Read, Glob, Grep
---

# Settings & Preferences Design

Design settings and preferences screens for: $ARGUMENTS

## Expert Knowledge

You are a settings design specialist with expertise in:
- Settings organization and hierarchy
- Preference controls and patterns
- Account management UX
- Privacy and data settings
- Settings search and discovery
- iOS Settings patterns
- Android Preferences patterns
- React Native settings implementations

## Settings Design Principles

### 1. Settings Architecture

**Settings Structure**:
```
┌─────────────────────────────────────────────────────┐
│               SETTINGS HIERARCHY                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ACCOUNT                                            │
│  ├── Profile                                        │
│  ├── Email & Password                              │
│  ├── Connected Accounts                            │
│  └── Subscription                                   │
│                                                     │
│  PREFERENCES                                        │
│  ├── Learning                                       │
│  │   ├── Daily Goal                                │
│  │   ├── Reminder Time                             │
│  │   └── Difficulty                                │
│  ├── Notifications                                 │
│  └── Appearance                                     │
│                                                     │
│  PRIVACY & SECURITY                                 │
│  ├── Biometrics                                    │
│  ├── Data Usage                                    │
│  └── Privacy Settings                              │
│                                                     │
│  SUPPORT                                            │
│  ├── Help Center                                   │
│  ├── Contact Us                                    │
│  └── About                                          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Settings Types**:
```typescript
type SettingType =
  | 'toggle'          // On/off switch
  | 'single_select'   // Radio/picker
  | 'multi_select'    // Checkboxes
  | 'slider'          // Range value
  | 'text_input'      // Text entry
  | 'time_picker'     // Time selection
  | 'navigation'      // Links to subscreen
  | 'action'          // Triggers action
  | 'info';           // Display only

interface Setting {
  id: string;
  type: SettingType;
  label: string;
  description?: string;
  value: any;
  defaultValue: any;
  options?: SettingOption[];
  validation?: ValidationRule;
  requiresAuth?: boolean;
  premium?: boolean;
}
```

### 2. Settings Screen Layout

**Main Settings Screen**:
```
┌─────────────────────────────────────┐
│  Settings                    [Done] │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────────┐│
│  │ 🔍 Search settings...           ││
│  └─────────────────────────────────┘│
│                                     │
│  ACCOUNT                            │
│  ┌─────────────────────────────────┐│
│  │ 👤 Profile                    > ││
│  │    John Doe                     ││
│  ├─────────────────────────────────┤│
│  │ 📧 Email & Password           > ││
│  │    john@email.com               ││
│  ├─────────────────────────────────┤│
│  │ ⭐ Premium                    > ││
│  │    Free Plan                    ││
│  └─────────────────────────────────┘│
│                                     │
│  LEARNING                           │
│  ┌─────────────────────────────────┐│
│  │ 🎯 Daily Goal                 > ││
│  │    15 minutes                   ││
│  ├─────────────────────────────────┤│
│  │ ⏰ Reminder                   > ││
│  │    9:00 AM                      ││
│  ├─────────────────────────────────┤│
│  │ 🔊 Sound Effects           [●] ││
│  └─────────────────────────────────┘│
│                                     │
│  ... more sections                  │
└─────────────────────────────────────┘
```

**Section Styling**:
```typescript
const settingSectionStyles = {
  header: {
    fontSize: 13,
    fontWeight: '600',
    color: 'text.secondary',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    paddingHorizontal: 16,
    paddingTop: 24,
    paddingBottom: 8,
  },
  container: {
    backgroundColor: 'surface.primary',
    borderRadius: 12,
    marginHorizontal: 16,
    overflow: 'hidden',
  },
  row: {
    minHeight: 44,
    paddingHorizontal: 16,
    paddingVertical: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  divider: {
    height: 1,
    backgroundColor: 'border.light',
    marginLeft: 52,  // Align with text after icon
  },
};
```

### 3. Setting Control Types

**Toggle Setting**:
```
┌─────────────────────────────────────┐
│ 🔊 Sound Effects                [●] │
│    Play sounds for correct answers  │
└─────────────────────────────────────┘

Specs:
├── Label: Primary text, left
├── Description: Secondary text, below label
├── Switch: Right aligned
├── Tap anywhere toggles (not just switch)
└── Immediate effect (no save button)
```

**Single Select (Picker)**:
```
┌─────────────────────────────────────┐
│ 🌍 App Language                   > │
│    English                          │
└─────────────────────────────────────┘
       ↓ Tap
┌─────────────────────────────────────┐
│  App Language                [Done] │
├─────────────────────────────────────┤
│  ○ English                          │
│  ● Español                      ✓  │
│  ○ Français                        │
│  ○ Deutsch                         │
│  ○ Português                       │
│  ○ 日本語                          │
└─────────────────────────────────────┘
```

**Slider Setting**:
```
┌─────────────────────────────────────┐
│ 🎯 Daily Goal                       │
│                                     │
│ 5 min  ○━━━━━━━●━━━━━○  30 min    │
│              15 min                 │
│                                     │
│ Casual    Basic   Serious  Intense │
└─────────────────────────────────────┘

Specs:
├── Show current value
├── Show min/max labels
├── Haptic feedback on change
├── Snap to defined values (optional)
└── Show contextual labels
```

**Time Picker**:
```
┌─────────────────────────────────────┐
│ ⏰ Reminder Time                  > │
│    9:00 AM                          │
└─────────────────────────────────────┘
       ↓ Tap
iOS: Native time picker wheel
Android: Material time picker dialog
```

**Multi-Select**:
```
┌─────────────────────────────────────┐
│  Practice Days                      │
├─────────────────────────────────────┤
│  [✓] Monday                         │
│  [✓] Tuesday                        │
│  [✓] Wednesday                      │
│  [ ] Thursday                       │
│  [✓] Friday                         │
│  [ ] Saturday                       │
│  [ ] Sunday                         │
│                                     │
│  Selected: 4 days                   │
└─────────────────────────────────────┘
```

### 4. Navigation Settings

**Drill-Down Navigation**:
```
Main Screen:           Sub Screen:
┌─────────────────┐   ┌─────────────────┐
│ Notifications > │ → │ < Notifications │
└─────────────────┘   ├─────────────────┤
                      │ Push            │
                      │ [●] Enabled     │
                      │                 │
                      │ TYPES           │
                      │ [✓] Reminders   │
                      │ [✓] Achievements│
                      │ [ ] Social      │
                      │ [ ] Marketing   │
                      │                 │
                      │ SCHEDULE        │
                      │ Quiet Hours   > │
                      └─────────────────┘
```

**Linked Settings**:
```typescript
interface LinkedSetting {
  parentId: string;
  childIds: string[];
  behavior: 'disable' | 'hide' | 'reset';
}

// Example: Notifications off → hide notification types
const linkedSettings: LinkedSetting[] = [
  {
    parentId: 'notifications_enabled',
    childIds: ['notif_reminders', 'notif_achievements', 'notif_social'],
    behavior: 'disable',  // Gray out when parent is off
  },
];
```

### 5. Account Settings

**Profile Section**:
```
┌─────────────────────────────────────┐
│  Profile                     [Save] │
├─────────────────────────────────────┤
│                                     │
│        ┌─────────┐                  │
│        │  [📷]   │                  │
│        │  Photo  │                  │
│        └─────────┘                  │
│        Change Photo                 │
│                                     │
│  Name                               │
│  ┌─────────────────────────────────┐│
│  │ John Doe                        ││
│  └─────────────────────────────────┘│
│                                     │
│  Username                           │
│  ┌─────────────────────────────────┐│
│  │ @johndoe                        ││
│  └─────────────────────────────────┘│
│  This will change your profile URL  │
│                                     │
│  Native Language                    │
│  ┌─────────────────────────────────┐│
│  │ English                       ▼ ││
│  └─────────────────────────────────┘│
│                                     │
└─────────────────────────────────────┘
```

**Subscription Settings**:
```
┌─────────────────────────────────────┐
│  Subscription                       │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────────┐│
│  │ ⭐ Premium                      ││
│  │                                 ││
│  │ You're on the Free plan         ││
│  │                                 ││
│  │ Unlock all features:            ││
│  │ • Unlimited AI conversations    ││
│  │ • Advanced pronunciation        ││
│  │ • Offline access                ││
│  │                                 ││
│  │ ┌─────────────────────────────┐ ││
│  │ │   Upgrade to Premium        │ ││
│  │ └─────────────────────────────┘ ││
│  └─────────────────────────────────┘│
│                                     │
│  Restore Purchases                  │
│                                     │
└─────────────────────────────────────┘
```

### 6. Privacy & Data Settings

**Privacy Settings**:
```
┌─────────────────────────────────────┐
│  Privacy                            │
├─────────────────────────────────────┤
│                                     │
│  DATA COLLECTION                    │
│  ┌─────────────────────────────────┐│
│  │ Analytics                   [●] ││
│  │ Help improve the app            ││
│  ├─────────────────────────────────┤│
│  │ Personalized Ads            [ ] ││
│  │ Show relevant ads               ││
│  └─────────────────────────────────┘│
│                                     │
│  YOUR DATA                          │
│  ┌─────────────────────────────────┐│
│  │ Download My Data              > ││
│  │ Request a copy of your data     ││
│  ├─────────────────────────────────┤│
│  │ Delete My Data                > ││
│  │ Permanently remove your data    ││
│  └─────────────────────────────────┘│
│                                     │
│  Privacy Policy                   > │
│                                     │
└─────────────────────────────────────┘
```

**Danger Zone**:
```
┌─────────────────────────────────────┐
│  DANGER ZONE                        │
│  ┌─────────────────────────────────┐│
│  │ 🗑️ Delete Account               ││
│  │ This cannot be undone           ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘

Delete Confirmation:
┌─────────────────────────────────────┐
│                                     │
│    Delete Your Account?             │
│                                     │
│    This will permanently delete:    │
│    • All your progress              │
│    • Your learning history          │
│    • Your achievements              │
│                                     │
│    Type "DELETE" to confirm:        │
│    ┌─────────────────────────────┐  │
│    │                             │  │
│    └─────────────────────────────┘  │
│                                     │
│    [Delete Account]  [Cancel]       │
│                                     │
└─────────────────────────────────────┘
```

### 7. Settings Search

**Search Implementation**:
```
┌─────────────────────────────────────┐
│ 🔍 notification                     │
├─────────────────────────────────────┤
│                                     │
│ RESULTS                             │
│                                     │
│ ⏰ Push Notifications             > │
│    Notifications > Push             │
│                                     │
│ 🔔 Notification Sound             > │
│    Notifications > Sound            │
│                                     │
│ 🌙 Quiet Hours                    > │
│    Notifications > Schedule         │
│                                     │
└─────────────────────────────────────┘

Search Behavior:
├── Search label and description
├── Search parent categories
├── Show breadcrumb path
├── Deep link to specific setting
└── Highlight matching text
```

### 8. Platform-Specific Patterns

**iOS Settings**:
```
iOS Guidelines:
├── Grouped UITableView style
├── System tint for switches
├── Chevron (>) for navigation
├── Footer text for explanations
├── Inset grouped style (iOS 13+)
└── Settings bundle for system Settings

SwiftUI:
Form {
  Section(header: Text("Learning")) {
    Toggle("Sound Effects", isOn: $soundEnabled)
    Picker("Daily Goal", selection: $dailyGoal) {
      ForEach(goals) { Text($0.label) }
    }
  }
}
.navigationTitle("Settings")
```

**Android Settings**:
```
Android Guidelines:
├── PreferenceScreen/PreferenceFragmentCompat
├── Material Design switches
├── Two-line list items (title + summary)
├── Preference categories with headers
├── Icon + title + summary + widget
└── Material You theming

Jetpack Compose:
ListItem(
  headlineContent = { Text("Sound Effects") },
  supportingContent = { Text("Play sounds for correct answers") },
  trailingContent = { Switch(checked, onCheckedChange) },
  leadingContent = { Icon(Icons.VolumeUp) }
)
```

### 9. Settings Persistence

**Storage Strategy**:
```typescript
interface SettingsStorage {
  // Local storage
  local: {
    store: 'AsyncStorage' | 'MMKV' | 'UserDefaults' | 'SharedPreferences';
    syncToCloud: boolean;
  };

  // Remote backup
  cloud: {
    enabled: boolean;
    provider: 'iCloud' | 'Google' | 'Custom';
    mergeStrategy: 'local_wins' | 'remote_wins' | 'latest_wins';
  };

  // Migration
  version: number;
  migrations: Migration[];
}

// Default values
const defaultSettings = {
  learning: {
    dailyGoal: 15,
    reminderTime: '09:00',
    soundEnabled: true,
  },
  notifications: {
    enabled: true,
    reminders: true,
    achievements: true,
    social: false,
  },
  appearance: {
    theme: 'system',
    haptics: true,
  },
};
```

### 10. Accessibility

**Settings Accessibility**:
```
Screen Reader:
├── Each setting fully described
├── Toggle state announced
├── Current value announced
├── Section headers as landmarks
└── Search results announced

Implementation:
<View
  accessible={true}
  accessibilityRole="switch"
  accessibilityLabel="Sound Effects"
  accessibilityHint="Double tap to toggle"
  accessibilityState={{ checked: soundEnabled }}
>
```

## Deliverables

For: $ARGUMENTS

Provide:
1. **Settings Architecture**: Categories, hierarchy
2. **Screen Layouts**: Main and sub-screens
3. **Control Types**: Toggle, picker, slider, etc.
4. **Account Section**: Profile, subscription, security
5. **Privacy Settings**: Data controls, deletion
6. **Search Implementation**: Search and navigation
7. **Platform Patterns**: iOS and Android specifics
8. **Persistence Strategy**: Storage and sync
9. **Accessibility**: Screen reader, labels
10. **Default Values**: Smart defaults for all settings
