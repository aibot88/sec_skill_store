---
name: privacy-manifest
description: PrivacyInfo.xcprivacy generator en validator. Run bij elke dependency change en pre-submit.
---

# Privacy Manifest Manager

Sinds 2024 verplicht voor App Store.

## Checklist
- `PrivacyInfo.xcprivacy` bestaat in project
- Geldig plist format
- Bevat alle vereiste keys:
  - `NSPrivacyTracking` (Bool)
  - `NSPrivacyTrackingDomains` (Array)
  - `NSPrivacyCollectedDataTypes` (Array of Dictionaries)
  - `NSPrivacyAccessedAPITypes` (Array)

## Vereiste APIs (Required Reason API)
Check code voor gebruik, documenteer reden:

### File timestamp APIs
- creationDate, modificationDate, fileModificationDate
- Reason codes: C617.1, 3B52.1, 0A2A.1, 3D61.1

### System boot time
- systemUptime, mach_absolute_time
- Reason codes: 35F9.1, 8FFB.1, 3D61.1

### Disk space
- volumeAvailableCapacityKey, getAttributesOfFileSystem
- Reason codes: E174.1, 85F4.1, 7D9E.1, B728.1

### Active keyboard
- UITextInputMode.activeInputModes
- Reason codes: 54BD.1, 8646.1

### User defaults
- UserDefaults
- Reason codes: CA92.1, 1C8F.1, C56D.1, AC6B.1

## Third-party SDKs
Alle SDKs die deze APIs gebruiken moeten EIGEN privacy manifest hebben. Check:
- Firebase (heeft eigen manifest sinds 10.23.0)
- Sentry (heeft eigen manifest)
- Nieuwere SDKs: check docs

## Output
1. Lijst van gemiste usage declarations
2. Correcte reason codes per detected API usage
3. SDK dependency check met bekende manifest status
4. Voorbeeld PrivacyInfo.xcprivacy als er geen is
