# Tracking App — Integration Guide

## 1 — Manual insertion points (do these by hand)

### 1a — Register the app in settings

**File:** `backend/pixelprowlers/settings.py`

Find the `INSTALLED_APPS` list. Add `"tracking"` after `"urgencies"`.

```python
INSTALLED_APPS = [
    # ... existing apps ...
    "rest_framework",
    "audits",
    "urgencies",
    "tracking",   # <-- ADD THIS LINE
]
```

### 1b — Wire the URLs

**File:** `backend/pixelprowlers/urls.py`

Add the tracking namespace alongside the existing `audits` and `urgencies` includes.
Adapt the line shown here to match your existing `audits`/`urgencies` pattern:

```python
urlpatterns = [
    # ... existing patterns ...
    path("api/audits/", include("audits.urls")),
    path("api/urgencies/", include("urgencies.urls")),
    path("api/tracking/", include("tracking.urls")),   # <-- ADD THIS LINE
]
```

---

## 2 — Database migration commands

Run these inside the `backend/` directory (venv activated or via `python manage.py`):

```bash
python manage.py makemigrations tracking
python manage.py migrate
```

---

## 3 — Frontend Nuxt Integration (JavaScript / TypeScript)

### 3a — Session initialization

Call this once when the Nuxt app first loads (e.g. in a plugin or `app.vue` `onMounted`).

```javascript
// Use crypto.randomUUID() to generate a session ID
const sessionId = crypto.randomUUID()

// Persist across page reloads
sessionStorage.setItem('pp_session_id', sessionId)

// Call session/init to create (or refresh) the visitor session
async function initSession() {
  try {
    await fetch('/api/tracking/session/init', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        // these fields are optional; server reads them from headers too
        referrer: document.referrer,
        language: navigator.language,
      }),
    })
  } catch (err) {
    // silently ignore — tracking must never break the UX
    console.warn('[tracking] session/init failed', err)
  }
}
```

### 3b — Track page views

```javascript
async function trackPageView(url, title) {
  const sessionId = sessionStorage.getItem('pp_session_id')
  if (!sessionId) return
  try {
    await fetch('/api/tracking/pageview', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, url, title }),
    })
  } catch (err) {
    console.warn('[tracking] pageview failed', err)
  }
}
```

Call it from `useHead` or a `watchEffect` each time the route changes.

### 3c — Track question interactions (audit form)

For each question in the 20-question audit form, measure time spent and send on change.

```javascript
async function trackQuestionInteraction(questionId, serie, orderIndex) {
  const sessionId = sessionStorage.getItem('pp_session_id')
  if (!sessionId) return

  // timeTracking is a Map<questionId, timestamp when question was shown>
  const shownAt = timeTracking.get(questionId)
  const timeSpentSeconds = shownAt ? (Date.now() - shownAt) / 1000 : 0

  try {
    await fetch('/api/tracking/question-interaction', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        question_id: questionId,
        serie: serie || null,
        time_spent_seconds: Math.round(timeSpentSeconds * 100) / 100,
        revisit_count: 0,   // server increments if already seen
        order_index: orderIndex,
      }),
    })
  } catch (err) {
    console.warn('[tracking] question-interaction failed', err)
  }
}
```

On the question-change event in your form component:

```javascript
// when user moves to question N
onQuestionChange(questionId, orderIndex) {
  trackQuestionInteraction(questionId, serie, orderIndex)
  timeTracking.set(questionId, Date.now())   // start timer for next question
}
```

### 3d — Track generic events (CTA clicks, form submit, abandon)

```javascript
async function trackEvent(eventType, pageUrl, metadata = {}) {
  const sessionId = sessionStorage.getItem('pp_session_id')
  if (!sessionId) return
  try {
    await fetch('/api/tracking/event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, event_type: eventType, page_url: pageUrl, metadata }),
    })
  } catch (err) {
    console.warn('[tracking] event failed', err)
  }
}

// Examples:
trackEvent('cta_click', window.location.href, { cta_id: 'hero-cta' })
trackEvent('form_submit', window.location.href, { form_id: 'audit-form', total_questions: 20 })

// Track form abandon via beforeunload (fires when user closes tab/navigates away)
window.addEventListener('beforeunload', () => {
  const sessionId = sessionStorage.getItem('pp_session_id')
  if (!sessionId) return
  // Use sendBeacon for reliability — it does not block the page unload
  const payload = JSON.stringify({
    session_id: sessionId,
    event_type: 'form_abandon',
    page_url: window.location.href,
    metadata: { last_question: currentQuestionId },
  })
  navigator.sendBeacon('/api/tracking/event', new Blob([payload], { type: 'application/json' }))
})
```

---

## 4 — RGPD / Privacy Notice

**What is stored:** IP address (identifiable), User-Agent, referrer URL, UTM parameters, session timestamps, per-question timing.

**What is NOT stored:** no name, no email, no PII by design.

**Consent:** because IP + UTM constitute personal data under GDPR/FR RGPD, a **consent banner** must be displayed before any tracking cookie or localStorage session ID is set. Follow CNIL guidelines (opt-in or legitimate interest documented). Suggested cookie text:
> "Nous collectons des anonymes de navigation pour ameliorer votre experience. Voulez-vous accepter ces cookies ?"

**Data retention:** set an automatic purge cron (Django management command or raw SQL) to delete VisitorSession records older than 90 days, or as required by your CNIL compliance documentation. Index on `created_at` enables efficient purge queries.

**Recommended:**
- Store retention policy in your privacy policy page
- Provide a "delete my data" endpoint (delete all records for a given session_id) for GDPR subject access requests
- Anonymize IP addresses after N days (keep first 3 octets only for geographic analytics)

---

## 5 — File structure produced

```
backend/tracking/
  __init__.py
  apps.py          — TrackingConfig
  models.py        — VisitorSession, PageView, QuestionInteraction, TrackingEvent
  utils.py         — parse_user_agent, get_client_ip, extract_utm
  serializers.py   — DRF serializers with upsert logic
  views.py         — 4 APIView endpoints + TrackingThrottle
  urls.py          — 4 named routes under /api/tracking/
  admin.py         — ModelAdmin x 4 + readonly fields
```

After adding to `INSTALLED_APPS` and `urls.py` and running migrations, the endpoints are live:

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/tracking/session/init` | Create / refresh visitor session |
| POST | `/api/tracking/pageview` | Record page view |
| POST | `/api/tracking/question-interaction` | Record question interaction (upsert) |
| POST | `/api/tracking/event` | Generic tracking event |