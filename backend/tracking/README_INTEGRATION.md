# Tracking App - GraphQL Integration

The tracking API is exposed through `/graphql/` only.

## Session initialization

```graphql
mutation {
  sessionInit(
    sessionId: "11111111-1111-1111-1111-111111111111"
    referrer: "https://example.com"
    language: "fr"
  ) {
    sessionId
    created
  }
}
```

## Page view

```graphql
mutation {
  recordPageView(
    sessionId: "11111111-1111-1111-1111-111111111111"
    url: "https://example.com"
    title: "Accueil"
  ) {
    pageviewId
  }
}
```

## Question interaction

```graphql
mutation {
  recordQuestionInteraction(
    sessionId: "11111111-1111-1111-1111-111111111111"
    questionId: "q1"
    serie: "s1"
    timeSpentSeconds: 12.5
    revisitCount: 0
    orderIndex: 1
  ) {
    interactionId
    revisitCount
  }
}
```

## Generic tracking event

```graphql
mutation {
  recordTrackingEvent(
    sessionId: "11111111-1111-1111-1111-111111111111"
    eventType: "cta_click"
    pageUrl: "https://example.com"
    metadata: "{\"cta_id\":\"hero-cta\"}"
  ) {
    eventId
  }
}
```

## Notes

- The server still stores `ip_address`, `user_agent`, and UTM data on `VisitorSession`.
- Rate limiting is applied inside each mutation.
- No REST endpoint remains for tracking.
