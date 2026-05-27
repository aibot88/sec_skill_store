---
name: iOS Voice Input Implementation
description: This skill should be used when the user asks to "implement voice input", "add speech recognition", "use SFSpeechRecognizer", "configure microphone permissions", "音声入力を実装したい", "Speech Frameworkの使い方", "マイク権限の設定", "音声認識機能を追加", "ディクテーション機能", or needs guidance on Apple Speech Framework, AVAudioSession configuration, speech recognition authorization, real-time transcription, on-device recognition, or iOS voice input best practices for SwiftUI applications targeting iOS 17+.
version: 0.1.0
---

# iOS Voice Input Implementation

iOS 17+向けSwiftUIアプリケーションにおける音声入力機能の実装ガイド。Apple Speech Framework (SFSpeechRecognizer) を使用したディクテーション機能の実装をサポートする。

## Quick Start Checklist

音声入力機能を実装する際の必須手順：

1. **Info.plist設定**
   - `NSMicrophoneUsageDescription` - マイクアクセス理由
   - `NSSpeechRecognitionUsageDescription` - 音声認識使用理由

2. **フレームワークインポート**
   ```swift
   import Speech
   import AVFoundation
   ```

3. **権限リクエスト**
   - `SFSpeechRecognizer.requestAuthorization()` で音声認識権限を取得
   - `AVAudioSession` でマイク権限を取得

4. **音声認識実装**
   - `SFSpeechRecognizer` インスタンス作成
   - `SFSpeechAudioBufferRecognitionRequest` でストリーミング認識
   - `AVAudioEngine` でオーディオキャプチャ

## Core Components

### SFSpeechRecognizer

音声認識エンジンの主要クラス。ロケール指定で日本語対応可能。

```swift
let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "ja-JP"))
```

**主要プロパティ:**
- `isAvailable` - 認識エンジンが利用可能か
- `supportsOnDeviceRecognition` - オンデバイス認識対応か
- `locale` - 認識対象言語

### SFSpeechAudioBufferRecognitionRequest

リアルタイム音声認識用リクエスト。AVAudioEngineからのバッファを受け取る。

```swift
let request = SFSpeechAudioBufferRecognitionRequest()
request.shouldReportPartialResults = true  // 途中結果を取得
request.requiresOnDeviceRecognition = true // オフライン認識を強制
```

### AVAudioEngine

オーディオキャプチャとルーティングを担当。

```swift
let audioEngine = AVAudioEngine()
let inputNode = audioEngine.inputNode
let recordingFormat = inputNode.outputFormat(forBus: 0)
```

## Permission Flow

### Authorization Request (iOS 17+ async/await)

```swift
func requestPermissions() async -> Bool {
    // 音声認識権限
    let speechStatus = await withCheckedContinuation { continuation in
        SFSpeechRecognizer.requestAuthorization { status in
            continuation.resume(returning: status)
        }
    }

    guard speechStatus == .authorized else { return false }

    // マイク権限
    let micStatus = await AVAudioApplication.requestRecordPermission()
    return micStatus
}
```

### Authorization States

| State | 説明 | 対応 |
|-------|------|------|
| `.authorized` | 許可済み | 認識開始可能 |
| `.denied` | 拒否された | 設定アプリへ誘導 |
| `.restricted` | 制限されている | 機能無効化 |
| `.notDetermined` | 未決定 | 権限リクエスト実行 |

## Implementation Pattern

### SwiftUI ViewModel Pattern

音声認識ロジックをViewModelに分離し、SwiftUI Viewから利用する。

```swift
@MainActor
@Observable
final class SpeechRecognizerViewModel {
    var transcribedText = ""
    var isRecording = false
    var errorMessage: String?

    private var audioEngine: AVAudioEngine?
    private var recognitionTask: SFSpeechRecognitionTask?
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "ja-JP"))

    func startRecording() async throws {
        // 実装は examples/speech-recognizer-viewmodel.swift を参照
    }

    func stopRecording() {
        // 録音停止処理
    }
}
```

### SwiftUI View Integration

```swift
struct DictationView: View {
    @State private var viewModel = SpeechRecognizerViewModel()

    var body: some View {
        VStack {
            TextField("音声入力...", text: $viewModel.transcribedText, axis: .vertical)
                .textFieldStyle(.roundedBorder)

            Button(action: { Task { await toggleRecording() } }) {
                Image(systemName: viewModel.isRecording ? "mic.fill" : "mic")
            }
        }
    }
}
```

## Audio Session Configuration

AVAudioSessionの適切な設定が音声認識の品質に影響する。

```swift
func configureAudioSession() throws {
    let audioSession = AVAudioSession.sharedInstance()
    try audioSession.setCategory(.playAndRecord, mode: .measurement, options: [.duckOthers, .defaultToSpeaker])
    try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
}
```

**Category Options:**
- `.duckOthers` - 他アプリの音量を下げる
- `.defaultToSpeaker` - スピーカー出力をデフォルトに
- `.allowBluetooth` - Bluetoothヘッドセット対応

## On-Device Recognition

iOS 17+ではオンデバイス認識が安定。ネットワーク不要でプライバシー保護。

```swift
// オンデバイス認識が利用可能か確認
if speechRecognizer.supportsOnDeviceRecognition {
    request.requiresOnDeviceRecognition = true
}
```

**対応言語（日本語含む）:**
- ja-JP (日本語)
- en-US, en-GB (英語)
- その他主要言語

オフライン時のフォールバック戦略については `references/on-device-recognition.md` を参照。

## Error Handling

音声認識で発生しうる主要エラー：

| エラーコード | 原因 | 対処 |
|------------|------|------|
| 203 | 音声が検出されない | UI でユーザーに発話を促す |
| 216 | ネットワークエラー | オンデバイス認識にフォールバック |
| 1110 | オーディオフォーマット不正 | AudioSession再設定 |

詳細なトラブルシューティングは `references/troubleshooting.md` を参照。

## Japanese Locale Specifics

日本語音声認識の特記事項：

- **句読点**: 自動挿入されないため、UIで補完を検討
- **漢字変換**: 文脈依存で精度が変わる
- **フィラー**: 「えーと」「あの」は認識されることがある

```swift
// 日本語ロケール指定
let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "ja-JP"))
```

## Quick Reference

| Component | Purpose | Key API |
|-----------|---------|---------|
| `SFSpeechRecognizer` | 認識エンジン | `recognitionTask(with:resultHandler:)` |
| `SFSpeechAudioBufferRecognitionRequest` | ストリーミング認識 | `append(_:)` |
| `SFSpeechRecognitionTask` | タスク管理 | `cancel()`, `finish()` |
| `AVAudioEngine` | オーディオキャプチャ | `inputNode`, `start()` |
| `AVAudioSession` | オーディオ設定 | `setCategory(_:mode:options:)` |

## Additional Resources

### Reference Files

詳細な情報は以下を参照：

- **`references/speech-framework-api.md`** - Speech Framework API詳細リファレンス
- **`references/permission-patterns.md`** - 権限リクエストパターンとInfo.plist設定
- **`references/on-device-recognition.md`** - オンデバイス認識の詳細設定とフォールバック
- **`references/troubleshooting.md`** - エラーコード一覧とデバッグ手法

### Example Files

実装サンプルは `examples/` ディレクトリを参照：

- **`examples/speech-recognizer-viewmodel.swift`** - 完全な音声認識ViewModel実装
- **`examples/voice-text-field.swift`** - 音声入力対応TextFieldコンポーネント
- **`examples/dictation-view.swift`** - ディクテーション画面の完全サンプル
- **`examples/info-plist-config.xml`** - Info.plist設定テンプレート
