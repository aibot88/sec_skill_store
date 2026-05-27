---
name: kaltura-api
description: Build applications on Kaltura — The Agentic Digital Experience Platform. 48 guides covering authentication (sessions, AppTokens, SSO/SAML), content management (upload, search, categories, metadata, captions), playback, AI services (captions, translation, agents, conversational AI), virtual events, user management, multi-stream, cue points & interactive video (hub + 5 dedicated type guides), content distribution, syndication feeds, analytics, gamification, webhooks, messaging, content moderation (flagging, AI-powered via REACH), experience components (Player, Express Recorder, Captions Editor, Genie Widget, Media Manager, Content Lab, Agents Widget, VOD Avatar Studio, Conversational Avatar, Chat & Collaborate, Embeddable Analytics), Unisphere framework, multi-account management. 912 tests validated against live API. API v3 (form-encoded) and modern JSON APIs with curl examples.
---

# Kaltura API Integration

Kaltura — The Agentic Digital Experience Platform. Kaltura is powering rich, agentic digital experiences across organizational journeys for customers, employees, learners, and audiences. The Kaltura platform combines intelligent content creation, enterprise-grade content management and intelligence, and multimodal conversational engagement capabilities. Kaltura serves leading enterprises, financial institutions, educational institutions, media and telecom providers, and other organizations worldwide.

This skill gives you the knowledge map to build any integration on Kaltura's 100+ REST API services.

## Platform Overview

The platform is built on three core layers:

- **Intelligent Content Creation** — Recording, editing, AI-assisted content generation (transcription, translation, captioning, dubbing, summarization, chaptering, clipping, quiz generation), and avatar-based video creation
- **Enterprise-Grade Content Management and Intelligence** — Centralized management of live and on-demand content with metadata, permissions, workflows, analytics, and AI-driven workflow agents for automated content lifecycle operations
- **Multimodal Conversational Engagement** — Content hubs, virtual events and webinars, player embeds, LMS/CMS integrations, conversational AI agents (Kaltura Genies and Agentic Avatars), and TV streaming applications

Content is organized as **entries** (media objects with metadata, flavors, thumbnails, and captions). Every API call requires a **Kaltura Session (KS)** — a signed, time-limited auth token.

## Authentication

Two auth methods, depending on context:

| Method | When to Use | How |
|--------|-------------|-----|
| `session.start` | Internal backend tools where you control the environment | POST with `partnerId` + `adminSecret` → returns KS |
| `appToken.startSession` | Production integrations, partner apps, microservices | HMAC exchange with a pre-created token — no admin secret exposed |

KS types: **USER** (type=0) for end-user operations, **ADMIN** (type=2) for backend-only management.

For full auth details, KS privileges, and AppToken HMAC workflow:
- [Session Guide](../../../KALTURA_SESSION_GUIDE.md) — KS generation, types, privileges, security practices
- [AppTokens API](../../../KALTURA_APPTOKENS_API.md) — Create, distribute, and rotate scoped tokens
- [Auth Broker API](../../../KALTURA_AUTH_BROKER_API.md) — SSO/SAML configuration, app subscriptions, federated login

## API Patterns

### API v3 (most services)

```bash
curl -X POST "$KALTURA_SERVICE_URL/service/{service}/action/{action}" \
  -d "ks=$KALTURA_KS" \
  -d "format=1" \
  -d "param[key]=value"
```

- **Base URL:** `https://www.kaltura.com/api_v3`
- Form-encoded POST, always include `format=1` for JSON responses
- Nested params use bracket notation: `filter[nameContains]=test`

### Modern JSON APIs

Some newer services use JSON bodies with auth headers:

| API | Base URL | Auth Header |
|-----|----------|-------------|
| Events Platform | `https://events-api.nvp1.ovp.kaltura.com/api/v1` | `Authorization: Bearer $KALTURA_KS` |
| App Registry | `https://app-registry.nvp1.ovp.kaltura.com/api/v1` | `Authorization: Bearer $KALTURA_KS` |
| User Profile | `https://user.nvp1.ovp.kaltura.com/api/v1` | `Authorization: Bearer $KALTURA_KS` |
| Agents Manager | `https://agents-manager.nvp1.ovp.kaltura.com` | `Authorization: Bearer $KALTURA_KS` |
| AI Genie | `https://genie.nvp1.ovp.kaltura.com` | `Authorization: KS $KALTURA_KS` |
| Messaging | `https://messaging.nvp1.ovp.kaltura.com/api/v1` | `Authorization: Bearer $KALTURA_KS` |
| Auth Broker | `https://auth.nvp1.ovp.kaltura.com/api/v1` | `Authorization: KS $KALTURA_KS` |
| Reports Microservice | `https://reports.nvp1.ovp.kaltura.com` | `Authorization: Bearer $KALTURA_KS` |
| Game Services (SCM) | `https://scm.nvp1.ovp.kaltura.com/api/v1` | `Authorization: Bearer $KALTURA_KS` |

> **Regional deployments** may use different base URLs (e.g., `irp2` for EU, `frp2` for DE). The URLs above are for the default NVP1 (US) region. Check your Kaltura account configuration for the correct regional endpoints.

## Common Integration Flows

### Upload → Process → Deliver → Embed

1. **Upload** content via chunked upload or import-from-URL
2. **Poll** for entry status to reach READY (status=2)
3. **Enrich** with REACH services (captions, translation, moderation, 22+ services) or Agents
4. **Search** your content library with eSearch
5. **Embed** the player in your application

### Entry Status Lifecycle

| Status | Value | Meaning |
|--------|-------|---------|
| ERROR_IMPORTING | -2 | Import failed |
| ERROR_CONVERTING | -1 | Transcoding failed |
| IMPORT | 0 | File being fetched/imported |
| PRECONVERT | 1 | Queued for transcoding |
| READY | 2 | Fully processed, playable |
| DELETED | 3 | Entry deleted |
| PENDING | 4 | Pending processing |
| MODERATE | 5 | Awaiting moderation |
| BLOCKED | 6 | Blocked by admin |
| NO_CONTENT | 7 | Entry created, no media attached |

### Upload Lifecycle

```
uploadToken.add → uploadToken.upload (one or more chunks) → media.add → media.addContent
```

Shortcuts: `media.addFromUploadedFile` (create + attach in one call), `media.addFromUrl` (import from URL).

## Capability Map — Detailed Guides

Read the relevant guide when you need to implement a specific capability:

### Getting Started

- **[API Getting Started](../../../KALTURA_API_GETTING_STARTED.md)** — API request structure, your first API call, multirequest batching with result chaining, error handling patterns, client libraries. Start here for API fundamentals.

### Content Management

- **[Upload & Ingestion API](../../../KALTURA_UPLOAD_AND_INGESTION_API.md)** — Chunked/resumable uploads, import-from-URL, entry CRUD, flavor assets, attachmentAsset for non-media files, CSV export. Start here for any content ingestion workflow.

- **[Content Delivery API](../../../KALTURA_CONTENT_DELIVERY_API.md)** — playManifest URLs (HLS/DASH), raw serve, download links, delivery profiles, CDN configuration, access control for playback.

- **[Thumbnail API](../../../KALTURA_THUMBNAIL_API.md)** — Dynamic thumbnail URL (27 params), thumbAsset CRUD, thumbParams templates.

- **[eSearch API](../../../KALTURA_ESEARCH_API.md)** — Full-text search across entries, captions, metadata, categories, and users. Supports AND/OR/NOT operators, nested filters, highlighting, facets, and sorting.

- **[Categories & Entitlements API](../../../KALTURA_CATEGORIES_AND_ENTITLEMENTS_API.md)** — Hierarchical content taxonomy via `category` service, membership and entitlement via `categoryUser`, content assignment via `categoryEntry`. Accounts with entitlement enabled require `disableentitlement` KS privilege for cross-category operations.

- **[Access Control API](../../../KALTURA_ACCESS_CONTROL_API.md)** — `accessControlProfile` rules with conditions (geo/IP/domain/scheduling restrictions) and actions (block/preview/limit flavors). Assign profiles to entries to enforce playback and access restrictions.

- **[Custom Metadata API](../../../KALTURA_CUSTOM_METADATA_API.md)** — XSD-based metadata schemas via `metadata_metadataProfile` plugin service with Kaltura-native types (textType, dateType, objectType, listType) and `<appinfo>` annotations for KMC rendering. Per-object structured metadata CRUD via `metadata_metadata` with optimistic locking, XSLT transformation pipeline, and eSearch integration via `KalturaESearchEntryMetadataItem`.

- **[Captions & Transcripts API](../../../KALTURA_CAPTIONS_AND_TRANSCRIPTS_API.md)** — Caption asset management (SRT/WebVTT/DFXP/SCC) via `caption_captionAsset` with two-step creation (add → setContent), on-the-fly WebVTT conversion, HLS segmented delivery, JSON serving for AI/LLM integrations, caption parameter templates via `caption_captionParams`, multi-language workflows, REACH integration for ASR/translation, and eSearch caption search via `KalturaESearchCaptionItem`.

- **[Moderation API](../../../KALTURA_MODERATION_API.md)** — Content moderation with two systems: legacy queue (`baseEntry.flag/approve/reject/listFlags` with `KalturaEntryModerationStatus` 1-6) and AI-powered moderation via REACH (`entryVendorTask` with `serviceFeature=15`, LLM-based text analysis and AWS Rekognition visual moderation). Configurable policies with weighted rules, critical-rule overrides, and category auto-activation. Player plugin `playkit-js-moderation` for viewer content flagging.

- **[Cue Points & Interactive Video API](../../../KALTURA_CUE_POINTS_API.md)** — Hub guide for temporal metadata on video entries via `cuepoint_cuepoint` service. Covers architecture, base service CRUD, 8 cue point types, REST vs live push protocols, eSearch integration via `KalturaESearchCuePointItem`, player plugin ecosystem, bulk XML import. Links to 5 dedicated type guides below.

- **[Quiz API](../../../KALTURA_QUIZ_API.md)** — Interactive video quiz lifecycle via `quiz_quiz` + `userEntry` services with 8 question types (MC, T/F, reflection, multi-answer, open, fill-in-blank, hotspot, go-to), 5 scoring models, PDF export, 4 report types, player IVQ plugin.

- **[Chapters & Slides API](../../../KALTURA_CHAPTERS_AND_SLIDES_API.md)** — Thumb cue points (chapter=subType 2, slide=subType 1), timedThumbAsset workflow (create, upload, serve, cascade delete), 5 slide creation pathways, navigation and dualscreen player plugins.

- **[Annotations API](../../../KALTURA_ANNOTATIONS_API.md)** — Annotations with threaded parent-child replies, hotspot pattern (JSON partnerData), searchableOnEntry flag, navigation player plugin.

- **[Ad Cue Points API](../../../KALTURA_AD_CUE_POINTS_API.md)** — VAST/VPAID ad insertion with 4 protocol types, pre-roll/mid-roll/overlay placement, protocol immutability, bumper player plugin.

- **[Code, Event & Session Cue Points API](../../../KALTURA_CODE_CUE_POINTS_API.md)** — Code cue points (view-change commands, systemName, forceStop), event cue points (BROADCAST_START/END, auto-created by media server), session cue points (recording boundaries), dualscreen player plugin.

### Playback

- **[Player Embed Guide](../../../KALTURA_PLAYER_EMBED_GUIDE.md)** — Embed Kaltura's Player v7 via iframe or JavaScript SDK. Covers autoplay, clipping (start/end times), access-controlled playback with KS, and programmatic player control.

- **[Multi-Stream API](../../../KALTURA_MULTI_STREAM_API.md)** — Dual/multi-screen entries for Picture-in-Picture and Side-by-Side layouts. Parent-child entry relationships, Dual Screen player plugin, runtime layout switching.

### AI Services

- **[REACH API](../../../KALTURA_REACH_API.md)** — Governed enrichment services marketplace: 22+ service types (captions, translation, moderation, dubbing, AI clips, quiz, sentiment analysis, and more) delivered by Machine/AI and Human Professional vendors across 80+ languages. Includes credit management, vendor abstraction, content deletion policies, and REACH Automation Rules (Boolean event conditions, category conditions, always-on) for automatic processing.

- **[Agents Manager API](../../../KALTURA_AGENTS_MANAGER_API.md)** — Create automated content-processing agents with triggers ("when a new entry is uploaded") and actions ("generate captions, then translate to Spanish"). Hands-free processing at scale.

- **[AI Genie API](../../../KALTURA_AI_GENIE_API.md)** — Conversational AI search over your video library using RAG. Streaming responses with structured answers (flashcards, sources, follow-ups). Supports both semantic search and multi-turn conversations.

### Events & User Management

- **[User Management API](../../../KALTURA_USER_MANAGEMENT_API.md)** — Full user lifecycle via `user` service (add, get, list, update, delete), login and credential management (enableLogin/disableLogin), role-based access control (RBAC) via `userRole` service (add, get, list, update, clone, delete), and groups via `group_group` service with `groupUser` membership. User statuses: 0 (BLOCKED), 1 (ACTIVE), 2 (DELETED).

- **[Auth Broker API](../../../KALTURA_AUTH_BROKER_API.md)** — SSO/SAML configuration microservice at `https://auth.nvp1.ovp.kaltura.com/api/v1`. Auth profiles (SAML IdP config with certificate, attribute mappings, group sync), app subscriptions (link apps to auth providers), SAML metadata endpoint, and SPA proxy for KMC. Uses `Authorization: KS <KS>` header (not Bearer).

- **[Events Platform API](../../../KALTURA_EVENTS_PLATFORM_API.md)** — Create and manage virtual events (town halls, webinars, conferences). Modern REST API with session types (Interactive Room, LiveWebcast, SimuLive), team members, speakers, templates, and event duplication. Multi-region support.

- **[App Registry API](../../../KALTURA_APP_REGISTRY_API.md)** — Register and manage Kaltura application instances (KMS sites, Events Platform portals, custom apps). Each registered app gets a unique GUID used by other services to associate data with specific app contexts. When Events Platform creates a virtual event, the event ID becomes the `appCustomId` — use `appCustomIdIn` filter to resolve virtual event IDs to app GUIDs.

- **[User Profile API](../../../KALTURA_USER_PROFILE_API.md)** — Per-application user profile management with event attendance lifecycle tracking. Manage registration, attendance status progression (created → registered → confirmed → attended → participated), bulk user import, attendance reporting, and incremental data sync. Includes cross-service registration data retrieval (virtualEvent → App Registry → User Profile → user.list) and engagement analytics via Reports API (report IDs 3030, 3037). Depends on App Registry for app context.

- **[Messaging API](../../../KALTURA_MESSAGING_API.md)** — Template-based email messaging for event communications, attendee notifications, and personalized outreach. Create templates with dynamic tokens (user profile fields, magic login links, QR codes, unsubscribe links), send personalized emails to individual users or groups, track delivery status and engagement (opens, clicks, bounces), and manage CAN-SPAM compliant unsubscribe preferences. Depends on App Registry for app context (appGuid) and integrates with User Profile for recipient data.

### Analytics & Gamification

- **[Analytics Reports API](../../../KALTURA_ANALYTICS_REPORTS_API.md)** — Pull analytics data: `report.getTable/getTotal/getGraphs` for VOD/Live/Webcast metrics, CSV exports via `getUrlForReportAsCsv` and `getCsvFromStringParams`, async Reports Microservice (generate/serve), live analytics via `liveReports.getEvents` and `beacon.list` for stream health. Pipe-delimited response format with paging, date-range filters, and multi-request batching.

- **[Analytics Events Collection API](../../../KALTURA_ANALYTICS_EVENTS_COLLECTION_API.md)** — Report playback and engagement events back to Kaltura analytics. `stats.collect` for server-side player events (WIDGET_LOADED, PLAY, quartiles, SEEK, buffer, replay), `analytics.trackEvent` for application-level tracking (PageLoad, ButtonClicked). Supports `appId` KS privilege for per-application segmentation and custom event context fields.

- **[Gamification API](../../../KALTURA_GAMIFICATION_API.md)** — Leaderboards, badges, certificates, lead scoring, and a rules engine via the Game Services (SCM) microservice. Rule types: sum, count, countUnique, countBoolean, external, override. Participation policies (display/do_not_display/do_not_save with email domain or group matching). Sub-leaderboards with filterPaths. Certificate PDF generation with text overlays. External events via CSV import. Scheduled game objects for automated status transitions.

### Experience Components

- **[Experience Components API](../../../KALTURA_EXPERIENCE_COMPONENTS_API.md)** — Index of all embeddable UI components with shared best practices for KS scoping, session expiry, and error handling.
- **[Express Recorder](../../../KALTURA_EXPRESS_RECORDER_API.md)** — Browser-based WebRTC video/audio/screen recording. Creates Kaltura entries on upload. JS embed with events and methods API.
- **[Captions Editor](../../../KALTURA_CAPTIONS_EDITOR_API.md)** — Interactive caption editing with video/waveform sync. iframe embed with URL parameters. Requires existing captionAsset.
- **[Conversational Avatar](../../../KALTURA_CONVERSATIONAL_AVATAR_API.md)** — AI-powered conversational video avatar embed via sandboxed iframe. Dynamic Page Prompts for persona configuration.
- **[Chat & Collaborate](../../../KALTURA_CNC_API.md)** — Real-time chat, Q&A, polls, reactions alongside video. Activated through Events Platform, not standalone.
- **[Genie Widget](../../../KALTURA_GENIE_WIDGET_API.md)** — Conversational AI search widget. ES module embed via Unisphere loader. Custom theming, 15 languages, content scoping. Player integration via 3 PlayKit plugins.
- **[Media Manager](../../../KALTURA_MEDIA_MANAGER_API.md)** — Browsable media library widget. Select/manage modes, inline table or modal dialog visuals, category-scoped, upload flow, entry selection callbacks.
- **[Content Lab](../../../KALTURA_CONTENT_LAB_API.md)** — AI content repurposing widget. Dual-runtime (application + ai-consent). Generates summaries, chapters, clips, quizzes from video. Entry eligibility checks, consent API.
- **[Agents Widget](../../../KALTURA_AGENTS_WIDGET_API.md)** — Agent management drawer UI. Create/configure automated content-processing agents with triggers and actions. Connects to Agents Manager backend.
- **[VOD Avatar Studio](../../../KALTURA_VOD_AVATAR_API.md)** — Pre-recorded avatar video studio. Script-to-video generation with AI avatars. Output saved as Kaltura media entries.
- **[Embeddable Analytics](../../../KALTURA_ANALYTICS_EMBED_API.md)** — Analytics dashboards via iframe + postMessage. viewsConfig for widget control, 9 dashboard views, 11 entity drill-downs, date filters.
- **[Unisphere Framework](../../../KALTURA_UNISPHERE_FRAMEWORK_API.md)** — Micro-frontend framework: loader, workspace lifecycle, 9 built-in services (pub-sub, storage, theme, analytics, logger), 15 embeddable widgets (Genie, Media Manager, Content Lab, Notifications, Avatars), player integration plugins, custom runtime development. CDN embedding (no npm needed) and npm build path.

### Multi-Account Management

- **[Multi-Account Management API](../../../KALTURA_MULTI_ACCOUNT_MANAGEMENT_API.md)** — Multi-account management: create child accounts via `partner.register`, cross-account auth via `session.impersonate`, aggregated analytics via multi-account report variants (20001-20023), per-account usage reports.

### Distribution & Syndication

- **[Content Distribution API](../../../KALTURA_DISTRIBUTION_API.md)** — Push content to external platforms (YouTube, Facebook, FTP, Cross-Kaltura) via distribution connectors. Distribution profiles define automation rules (auto-submit on entry ready, moderation-gated, sunrise/sunset scheduling). Entry distributions track per-entry status through a state machine (PENDING → QUEUED → SUBMITTING → READY). Uses `contentDistribution_*` plugin services (distributionProvider, distributionProfile, entryDistribution).

- **[Syndication Feeds API](../../../KALTURA_SYNDICATION_API.md)** — Generate RSS/MRSS/XML feeds (Google Video Sitemap, Yahoo MRSS, iTunes Podcast, Roku) that external platforms pull via HTTP GET. Feeds serve XML at public URLs with entry filtering, playlist scoping, and configurable caching (24h default, 30min with `&limit=N`). Uses the `syndicationFeed` service.

### Integration & Automation

- **[Webhooks & Event Notifications API](../../../KALTURA_WEBHOOKS_API.md)** — Real-time HTTP webhooks and email notifications triggered by content events (entry ready, metadata changed, caption added, REACH task completed). Clone pre-built system templates, configure webhook URLs with HMAC signing, set event conditions, and use manual dispatch for testing. Email notifications are delivered via the Messaging Service (SendGrid) with delivery tracking and engagement analytics. Uses the `eventnotification_eventnotificationtemplate` API v3 plugin service. Boolean Event Notification Templates serve as conditions for REACH Automation Rules (documented in the REACH guide).

## Security & Best Practices

When building on Kaltura, follow these principles for production-quality integrations:

- **Use AppTokens for production auth.** Generate KS server-side via AppTokens; keep `adminSecret` on the server only. Create scoped tokens with minimal privileges and rotate periodically. See [AppTokens API](../../../KALTURA_APPTOKENS_API.md).
- **Prefer USER KS (type=0)** for end-user operations. Reserve ADMIN KS (type=2) for backend-only management. Scope privileges with `edit:`, `sview:`, `setrole:`, `iprestrict:`.
- **Verify webhook signatures.** Validate `SHA256(signing_secret + body)` on all incoming HTTP webhooks before processing.
- **Use Kaltura's built-in services** rather than reimplementing. REACH for enrichment services (captions, translation, moderation, and more), Agents Manager for automated processing, Messaging for email delivery, eSearch for search, Access Control for content protection.
- **Handle errors and retries.** Check every API response for error codes. Implement exponential backoff for transient failures (HTTP 500, rate limits). Log error codes for debugging.
- **Set short KS expiry.** Default to 1-4 hour sessions. Use AppToken session renewal rather than long-lived admin sessions.
- **Sanitize inputs.** Validate user-provided entry IDs, search terms, and metadata before passing to API calls.
- **Use CAN-SPAM compliant email patterns.** Include unsubscribe links and respect opt-out preferences when using the Messaging API.

## Environment Setup

```bash
export KALTURA_SERVICE_URL="https://www.kaltura.com/api_v3"
export KALTURA_PARTNER_ID="your_partner_id"
export KALTURA_KS="your_kaltura_session"
```

Regional deployments may use different base URLs. Check with your Kaltura account configuration.
