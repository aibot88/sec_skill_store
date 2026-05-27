---
name: supabase-realtime
description: >
  This skill should be used when working with Supabase Realtime, setting up database change
  listeners, implementing presence, using broadcast channels, or building real-time features.
  Trigger when: "Supabase Realtime", "realtime subscription", "listen for changes",
  "database changes", "broadcast", "presence", "WebSocket", "channel",
  "real-time updates", "subscribe to table", "Postgres changes",
  "supabase.channel", "realtime configuration", "realtime authorization",
  "broadcast from database", "realtime.broadcast_changes", "private channel",
  or implementing any live/real-time functionality with Supabase.
---

# Supabase Realtime

Guidance for implementing real-time features using Supabase's Realtime service. Pinned to April 2026.

## Overview

Supabase Realtime provides three capabilities over WebSocket connections:

| Feature | Description | Use Case |
|---------|-------------|----------|
| **Postgres Changes** | Listen to INSERT/UPDATE/DELETE on tables | Small-scale live feeds (legacy path; doesn't scale well) |
| **Broadcast** | Send ephemeral messages to channel subscribers | Chat, cursors, typing indicators — **recommended primitive** |
| **Presence** | Track shared state across clients | Online users, collaborative editing |

**Recommendation pivot (2024-2026):** Supabase docs now recommend **Broadcast (especially Broadcast-from-Database)** over Postgres Changes for non-trivial scale. Postgres Changes still works and is documented, but each table added to the publication adds Realtime overhead, and the write-amplification gets expensive past a few thousand connected clients. New builds should default to Broadcast; reach for Postgres Changes only when you specifically want Postgres' row-level event semantics with low-volume tables.

## Postgres Changes (legacy path)

### Subscribe to All Changes on a Table

```typescript
const channel = supabase
  .channel("table-changes")
  .on(
    "postgres_changes",
    { event: "*", schema: "public", table: "messages" },
    (payload) => {
      console.log("Change received:", payload);
    }
  )
  .subscribe();
```

### Subscribe to Specific Events

```typescript
// Only INSERT events
supabase
  .channel("new-messages")
  .on(
    "postgres_changes",
    { event: "INSERT", schema: "public", table: "messages" },
    (payload) => {
      console.log("New message:", payload.new);
    }
  )
  .subscribe();
```

### Filter by Column Value

```typescript
supabase
  .channel("my-messages")
  .on(
    "postgres_changes",
    {
      event: "INSERT",
      schema: "public",
      table: "messages",
      filter: "room_id=eq.room-123",
    },
    (payload) => {
      console.log("New message in room:", payload.new);
    }
  )
  .subscribe();
```

### Available Filter Operators

| Filter | Example | Description |
|--------|---------|-------------|
| `eq` | `column=eq.value` | Equals |
| `neq` | `column=neq.value` | Not equals |
| `lt`, `gt` | `column=gt.5` | Less/greater than |
| `lte`, `gte` | `column=gte.10` | Less/greater or equal |
| `in` | `column=in.(a,b,c)` | In list |

### Database Configuration for Postgres Changes

#### Enable Realtime on a Table

By default, tables are not enabled for Realtime Postgres Changes. Enable via SQL:

```sql
alter publication supabase_realtime add table public.messages;
```

#### Replica Identity

For UPDATE and DELETE events to include full row data (not just primary key), set `REPLICA IDENTITY FULL`:

```sql
alter table public.messages replica identity full;
```

Without this, `payload.old` in UPDATE/DELETE events only contains the primary key columns. **Trade-off:** `replica identity full` increases WAL volume — worth it on small tables where old values matter, expensive on hot high-volume tables.

#### Disable Realtime on a Table

```sql
alter publication supabase_realtime drop table public.messages;
```

## Broadcast (recommended)

Send and receive ephemeral messages without database persistence.

### Send a Broadcast Message

```typescript
const channel = supabase.channel("room-1");

channel.subscribe((status) => {
  if (status === "SUBSCRIBED") {
    channel.send({
      type: "broadcast",
      event: "cursor-move",
      payload: { x: 100, y: 200, userId: "user-123" },
    });
  }
});
```

### Receive Broadcast Messages

```typescript
supabase
  .channel("room-1")
  .on("broadcast", { event: "cursor-move" }, (payload) => {
    console.log("Cursor moved:", payload.payload);
  })
  .subscribe();
```

## Broadcast-from-Database (the scalable Postgres Changes replacement)

Use Postgres triggers to call `realtime.broadcast_changes()` and emit events from the database. Same insight as Postgres Changes (server pushes when data changes) but routed through Broadcast — which scales much better and **doesn't require `REPLICA IDENTITY FULL`**.

```sql
create or replace function public.broadcast_message_change()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  perform realtime.broadcast_changes(
    'room:' || NEW.room_id,        -- topic (channel name)
    TG_OP,                          -- 'INSERT' / 'UPDATE' / 'DELETE'
    TG_OP,                          -- event name
    TG_TABLE_NAME,
    TG_TABLE_SCHEMA,
    NEW,                            -- new record
    OLD                             -- old record (for UPDATE/DELETE)
  );
  return coalesce(NEW, OLD);
end;
$$;

create trigger on_message_change
  after insert or update or delete on public.messages
  for each row execute function public.broadcast_message_change();
```

Clients subscribe to the same channel name:
```typescript
supabase
  .channel(`room:${roomId}`, { config: { private: true } })  // private = enforces Realtime Authorization
  .on("broadcast", { event: "INSERT" }, (payload) => addMessage(payload.payload.record))
  .subscribe();
```

See [Broadcast from Database](https://supabase.com/docs/guides/realtime/broadcast#trigger-broadcast-messages-from-your-database).

## Realtime Authorization (RLS on `realtime.messages`)

Authorization for Broadcast and Presence channels uses RLS policies on the `realtime.messages` table. Required client: `supabase-js` >= **v2.44.0**.

### Mark a channel as private

```typescript
const channel = supabase.channel("room:42", { config: { private: true } });
```

Private channels require an authenticated user and check policies on `realtime.messages` before letting messages through.

### Define authorization policies

```sql
-- Only team members can subscribe to a team's broadcast/presence channel
create policy "Team members read team channel"
  on realtime.messages for select
  to authenticated
  using (
    realtime.topic() like 'team:%'
    and exists (
      select 1 from public.team_members
      where team_id = (split_part(realtime.topic(), ':', 2))::uuid
      and user_id = (select auth.uid())
    )
  );

create policy "Team members write to team channel"
  on realtime.messages for insert
  to authenticated
  with check (
    realtime.topic() like 'team:%'
    and exists (
      select 1 from public.team_members
      where team_id = (split_part(realtime.topic(), ':', 2))::uuid
      and user_id = (select auth.uid())
    )
  );
```

In the dashboard's Realtime Settings, **disable "Allow public access"** to enforce that all channels go through authorization.

## Presence

Track which users are online and sync shared state.

### Track User Presence

```typescript
const channel = supabase.channel("online-users", { config: { private: true } });

channel
  .on("presence", { event: "sync" }, () => {
    const state = channel.presenceState();
    console.log("Online users:", state);
  })
  .on("presence", { event: "join" }, ({ key, newPresences }) => {
    console.log("User joined:", key, newPresences);
  })
  .on("presence", { event: "leave" }, ({ key, leftPresences }) => {
    console.log("User left:", key, leftPresences);
  })
  .subscribe(async (status) => {
    if (status === "SUBSCRIBED") {
      await channel.track({
        user_id: "user-123",
        online_at: new Date().toISOString(),
      });
    }
  });
```

### Untrack Presence

```typescript
await channel.untrack();
```

## Unsubscribing

```typescript
supabase.removeChannel(channel);    // remove a single channel
supabase.removeAllChannels();       // remove all
```

## RLS and Realtime

For Postgres Changes, Realtime respects RLS policies on the source table — users only receive change events for rows they have SELECT access to. Ensure RLS policies are in place before enabling Realtime, or users may not receive expected events.

For Broadcast and Presence on private channels, authorization is enforced via RLS on `realtime.messages` (see Realtime Authorization above).

**Common issue with Postgres Changes:** subscription returns no events even though data is changing. Check:
1. Table is in the `supabase_realtime` publication.
2. RLS policies allow SELECT for the subscribing user.
3. `REPLICA IDENTITY FULL` is set if you need old row data on UPDATE/DELETE.

## Realtime Logs (MCP)

```
mcp__supabase__get_logs(project_id: "<id>", service: "realtime")
```

Returns WebSocket connection and subscription logs from the last 24 hours.

## Configuration (config.toml)

```toml
[realtime]
enabled = true
# ip_version = "IPv4"  # or IPv6
```

## Common Patterns

### Chat Room (Broadcast-from-Database)

```typescript
// Server side: trigger calls realtime.broadcast_changes() on insert into public.messages
// (see SQL example above)

// Client side
const channel = supabase
  .channel(`room:${roomId}`, { config: { private: true } })
  .on("broadcast", { event: "INSERT" }, ({ payload }) => addMessage(payload.record))
  .on("presence", { event: "sync" }, () => {
    updateOnlineUsers(channel.presenceState());
  })
  .on("broadcast", { event: "typing" }, ({ payload }) => {
    showTypingIndicator(payload.userId);
  })
  .subscribe(async (status) => {
    if (status === "SUBSCRIBED") {
      await channel.track({ user_id: currentUserId });
    }
  });
```

## Best Practices

1. **Default to Broadcast (especially Broadcast-from-Database) for new builds.** Reach for Postgres Changes only on small tables where row-level event semantics matter.
2. **Mark sensitive channels as `private: true`** and enforce via RLS on `realtime.messages`.
3. **Set `REPLICA IDENTITY FULL`** only on tables where old values are needed *and* the WAL cost is acceptable.
4. **Use filters** to reduce the volume of events received.
5. **Clean up subscriptions** when components unmount or users navigate away.
6. **Handle reconnection** — Supabase client auto-reconnects, but refresh state on reconnect.
7. **Use `supabase-js` >= v2.44.0** for Realtime Authorization support.
