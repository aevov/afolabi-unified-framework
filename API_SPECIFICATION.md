# AUF Platform API Specification
## Version 1.0 | Developer Documentation

---

## Overview

The AUF API provides programmatic access to coherence data, session management, and the global mesh network. This RESTful API uses JSON for request/response bodies and OAuth 2.0 for authentication.

**Base URL:** `https://api.auf.technology/v1`  
**Sandbox URL:** `https://sandbox-api.auf.technology/v1`

---

## Authentication

### OAuth 2.0 Flow

AUF uses OAuth 2.0 with PKCE for secure authentication.

#### Step 1: Authorization Request
```
GET https://auth.auf.technology/authorize
  ?client_id={CLIENT_ID}
  &redirect_uri={REDIRECT_URI}
  &response_type=code
  &scope=read:user read:sessions write:sessions mesh:join
  &code_challenge={CODE_CHALLENGE}
  &code_challenge_method=S256
```

#### Step 2: Token Exchange
```http
POST https://auth.auf.technology/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code={AUTH_CODE}
&redirect_uri={REDIRECT_URI}
&client_id={CLIENT_ID}
&code_verifier={CODE_VERIFIER}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "refresh_token": "dGhpcyBpcyBhIHJlZnJl...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "read:user read:sessions write:sessions mesh:join"
}
```

### API Key Authentication (Server-to-Server)

For backend integrations, use API keys:

```http
GET /v1/users/me
Authorization: Bearer {API_KEY}
X-AUF-Client-ID: {CLIENT_ID}
```

### Scopes

| Scope | Description |
|-------|-------------|
| `read:user` | Read user profile and settings |
| `write:user` | Update user profile |
| `read:sessions` | Access session history and analytics |
| `write:sessions` | Create and manage sessions |
| `read:coherence` | Access real-time coherence data |
| `mesh:join` | Join mesh network sessions |
| `mesh:create` | Create mesh sessions (Pro tier) |
| `admin:org` | Manage organization (Enterprise) |

---

## Rate Limits

| Tier | Requests/min | Burst | WebSocket connections |
|------|--------------|-------|----------------------|
| Free | 60 | 10 | 1 |
| Plus | 300 | 50 | 2 |
| Pro | 1,000 | 100 | 5 |
| Enterprise | 10,000 | 500 | Unlimited |

Rate limit headers are included in all responses:
```http
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 298
X-RateLimit-Reset: 1706745600
```

---

## User Endpoints

### Get Current User

```http
GET /v1/users/me
Authorization: Bearer {ACCESS_TOKEN}
```

**Response:**
```json
{
  "id": "usr_abc123def456",
  "email": "user@example.com",
  "display_name": "Alex Chen",
  "avatar_url": "https://cdn.auf.technology/avatars/usr_abc123.jpg",
  "tier": "pro",
  "created_at": "2025-06-15T10:30:00Z",
  "stats": {
    "total_sessions": 127,
    "total_coherence_minutes": 892,
    "current_streak": 14,
    "longest_streak": 31,
    "average_coherence": 0.72,
    "mesh_sessions_joined": 23
  },
  "devices": [
    {
      "id": "dev_solas_a7f3",
      "type": "solas",
      "firmware_version": "2.1.4",
      "last_sync": "2026-01-31T18:00:00Z"
    }
  ],
  "baseline": {
    "resting_hrv": 45,
    "resting_hr": 68,
    "coherence_threshold": 0.65
  }
}
```

### Update User Profile

```http
PATCH /v1/users/me
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "display_name": "Alex Chen",
  "preferences": {
    "notifications_enabled": true,
    "reminder_time": "07:30",
    "timezone": "America/Los_Angeles"
  }
}
```

### Get User Coherence History

```http
GET /v1/users/me/coherence
  ?start_date=2026-01-01
  &end_date=2026-01-31
  &granularity=day
Authorization: Bearer {ACCESS_TOKEN}
```

**Response:**
```json
{
  "data": [
    {
      "date": "2026-01-31",
      "sessions": 2,
      "total_minutes": 25,
      "average_coherence": 0.74,
      "peak_coherence": 0.91,
      "time_in_high_coherence": 18
    }
  ],
  "summary": {
    "period_average": 0.71,
    "trend": "improving",
    "trend_percentage": 8.3
  }
}
```

---

## Session Endpoints

### Create Session

```http
POST /v1/sessions
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "type": "solo",
  "protocol": "heart_breath_sync",
  "target_duration": 600,
  "intention": "Focus and clarity for upcoming presentation"
}
```

**Response:**
```json
{
  "id": "sess_xyz789",
  "type": "solo",
  "protocol": "heart_breath_sync",
  "status": "active",
  "started_at": "2026-01-31T19:00:00Z",
  "target_duration": 600,
  "websocket_url": "wss://stream.auf.technology/v1/sessions/sess_xyz789"
}
```

### Session Protocols

| Protocol ID | Name | Duration | Level |
|-------------|------|----------|-------|
| `heart_breath_sync` | Heart-Breath Synchronization | 5-30 min | 1 |
| `gratitude_focus` | Gratitude Focus | 10-20 min | 1 |
| `coherence_building` | Coherence Building | 15-45 min | 2 |
| `intention_amplify` | Intention Amplification | 20-60 min | 2 |
| `manifestation_basic` | Basic Manifestation | 30-90 min | 3 |
| `manifestation_advanced` | Advanced Manifestation | 60-180 min | 4 |

### Get Session Details

```http
GET /v1/sessions/{session_id}
Authorization: Bearer {ACCESS_TOKEN}
```

**Response:**
```json
{
  "id": "sess_xyz789",
  "type": "solo",
  "protocol": "heart_breath_sync",
  "status": "completed",
  "started_at": "2026-01-31T19:00:00Z",
  "ended_at": "2026-01-31T19:10:23Z",
  "duration": 623,
  "metrics": {
    "average_coherence": 0.68,
    "peak_coherence": 0.87,
    "time_in_high_coherence": 412,
    "coherence_ratio": 0.66,
    "average_hrv": 52,
    "average_hr": 64,
    "breathing_sync_score": 0.81
  },
  "timeline": [
    {"time": 0, "coherence": 0.32},
    {"time": 60, "coherence": 0.51},
    {"time": 120, "coherence": 0.64},
    {"time": 180, "coherence": 0.72}
  ]
}
```

### End Session

```http
POST /v1/sessions/{session_id}/end
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "notes": "Felt strong heart connection around minute 7",
  "subjective_rating": 4
}
```

---

## Real-Time Coherence Stream

### WebSocket Connection

```javascript
const ws = new WebSocket(
  'wss://stream.auf.technology/v1/coherence',
  ['auf-protocol-v1']
);

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'authenticate',
    token: ACCESS_TOKEN
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Coherence:', data.coherence);
};
```

### Message Types

**Coherence Update (Server → Client):**
```json
{
  "type": "coherence_update",
  "timestamp": "2026-01-31T19:05:23.456Z",
  "data": {
    "coherence": 0.72,
    "hrv": 48,
    "hr": 66,
    "breathing_phase": "inhale",
    "breathing_progress": 0.65
  }
}
```

**Session Event (Server → Client):**
```json
{
  "type": "session_event",
  "event": "coherence_threshold_reached",
  "data": {
    "threshold": 0.70,
    "duration_above": 30
  }
}
```

---

## Mesh Network Endpoints

### List Active Mesh Sessions

```http
GET /v1/mesh/sessions
  ?type=public
  &status=active
Authorization: Bearer {ACCESS_TOKEN}
```

**Response:**
```json
{
  "sessions": [
    {
      "id": "mesh_global_morning",
      "name": "Morning Coherence Circle",
      "type": "scheduled",
      "visibility": "public",
      "participant_count": 127,
      "average_coherence": 0.76,
      "started_at": "2026-01-31T14:00:00Z",
      "scheduled_end": "2026-01-31T14:30:00Z",
      "host": {
        "id": "usr_host123",
        "display_name": "Sarah Kim",
        "verified": true
      },
      "join_requirements": {
        "min_tier": "pro",
        "min_coherence_history": 0.60
      }
    }
  ],
  "meta": {
    "total": 23,
    "page": 1,
    "per_page": 10
  }
}
```

### Join Mesh Session

```http
POST /v1/mesh/sessions/{mesh_id}/join
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "intention": "Global peace and harmony",
  "anonymous": false
}
```

**Response:**
```json
{
  "joined": true,
  "participant_id": "part_abc123",
  "position": 128,
  "websocket_url": "wss://mesh.auf.technology/v1/sessions/mesh_global_morning",
  "group_coherence": 0.76,
  "your_contribution_weight": 0.0078
}
```

### Create Mesh Session (Pro+)

```http
POST /v1/mesh/sessions
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "name": "Family Evening Calm",
  "visibility": "private",
  "max_participants": 8,
  "scheduled_start": "2026-01-31T21:00:00Z",
  "duration": 1200,
  "protocol": "gratitude_focus",
  "invitation_emails": [
    "family1@example.com",
    "family2@example.com"
  ]
}
```

### Mesh WebSocket Protocol

```javascript
const meshWs = new WebSocket(meshWebsocketUrl);

meshWs.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  
  switch(msg.type) {
    case 'group_coherence':
      // Group average coherence update
      // { coherence: 0.78, participant_count: 127 }
      break;
      
    case 'participant_joined':
      // New participant
      // { user_id, display_name, position }
      break;
      
    case 'sync_pulse':
      // Synchronization wave
      // { phase: 'inhale', progress: 0.5, group_sync: 0.82 }
      break;
      
    case 'manifestation_event':
      // Collective threshold reached
      // { level: 3, strength: 0.91, duration: 120 }
      break;
  }
};
```

---

## Device Endpoints

### Register Device

```http
POST /v1/devices
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "type": "solas",
  "serial_number": "SOL-2026-A7F3-9K2L",
  "firmware_version": "2.1.4"
}
```

### Sync Device Data

```http
POST /v1/devices/{device_id}/sync
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "readings": [
    {
      "timestamp": "2026-01-31T18:00:00Z",
      "hrv": 45,
      "hr": 72,
      "coherence": 0.62
    }
  ],
  "battery_level": 87,
  "last_worn": "2026-01-31T18:30:00Z"
}
```

---

## Analytics Endpoints (Enterprise)

### Organization Dashboard

```http
GET /v1/organizations/{org_id}/analytics
  ?period=30d
Authorization: Bearer {API_KEY}
```

**Response:**
```json
{
  "period": "30d",
  "users": {
    "total": 487,
    "active": 312,
    "active_rate": 0.64
  },
  "sessions": {
    "total": 4521,
    "average_duration": 892,
    "average_coherence": 0.69
  },
  "trends": {
    "coherence_improvement": 0.12,
    "engagement_trend": "stable",
    "top_protocol": "heart_breath_sync"
  },
  "wellness_impact": {
    "estimated_stress_reduction": 0.23,
    "productivity_correlation": 0.67
  }
}
```

---

## Webhooks

### Configuring Webhooks

```http
POST /v1/webhooks
Authorization: Bearer {API_KEY}
Content-Type: application/json

{
  "url": "https://your-server.com/auf-webhook",
  "events": [
    "session.completed",
    "user.streak_milestone",
    "mesh.threshold_reached"
  ],
  "secret": "your-webhook-secret"
}
```

### Event Types

| Event | Description |
|-------|-------------|
| `session.started` | User begins a session |
| `session.completed` | Session ends with metrics |
| `user.streak_milestone` | User hits 7, 30, 100 day streak |
| `user.tier_upgraded` | User upgrades subscription |
| `mesh.threshold_reached` | Collective manifestation threshold hit |
| `device.low_battery` | Device battery below 15% |

### Webhook Payload Example

```json
{
  "id": "evt_123456",
  "type": "session.completed",
  "created": "2026-01-31T19:10:23Z",
  "data": {
    "user_id": "usr_abc123",
    "session_id": "sess_xyz789",
    "duration": 623,
    "average_coherence": 0.68,
    "peak_coherence": 0.87
  }
}
```

### Webhook Signature Verification

```javascript
const crypto = require('crypto');

function verifyWebhook(payload, signature, secret) {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(`sha256=${expected}`)
  );
}
```

---

## SDK Examples

### JavaScript/TypeScript

```typescript
import { AufClient } from '@auf/sdk';

const auf = new AufClient({
  accessToken: 'your-access-token'
});

// Start a session
const session = await auf.sessions.create({
  protocol: 'heart_breath_sync',
  targetDuration: 600
});

// Stream coherence
session.onCoherence((data) => {
  console.log(`Coherence: ${data.coherence}`);
});

// Join mesh
const mesh = await auf.mesh.join('mesh_global_morning');
mesh.onGroupCoherence((data) => {
  console.log(`Group: ${data.coherence}, Participants: ${data.count}`);
});
```

### Python

```python
from auf import AufClient

client = AufClient(access_token='your-access-token')

# Get user stats
user = client.users.me()
print(f"Streak: {user.stats.current_streak} days")

# List mesh sessions
sessions = client.mesh.list(status='active')
for session in sessions:
    print(f"{session.name}: {session.participant_count} people")
```

### Swift (iOS)

```swift
import AufSDK

let auf = AufClient(accessToken: "your-access-token")

// Start session with real-time updates
auf.sessions.create(protocol: .heartBreathSync) { session in
    session.onCoherenceUpdate { coherence in
        self.coherenceLabel.text = "\(Int(coherence * 100))%"
    }
}
```

---

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "insufficient_coherence_level",
    "message": "This protocol requires Level 3 access. Your current average coherence is 0.58, which qualifies for Level 2.",
    "details": {
      "required_level": 3,
      "current_level": 2,
      "coherence_needed": 0.80
    },
    "documentation_url": "https://docs.auf.technology/errors/insufficient_coherence_level"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `unauthorized` | 401 | Invalid or expired token |
| `forbidden` | 403 | Insufficient permissions |
| `not_found` | 404 | Resource doesn't exist |
| `rate_limited` | 429 | Too many requests |
| `insufficient_tier` | 403 | Upgrade required for feature |
| `insufficient_coherence_level` | 403 | Higher coherence needed |
| `mesh_full` | 409 | Session at capacity |
| `device_not_connected` | 400 | Solas not paired |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01 | Initial API release |

---

*For support, contact api-support@auf.technology*
