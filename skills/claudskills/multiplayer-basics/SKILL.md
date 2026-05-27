---
name: multiplayer-basics
description: Use when implementing multiplayer — MultiplayerAPI, ENet/WebSocket peers, RPCs, and authority model
---

# Multiplayer Basics in Godot 4.3+

All examples target Godot 4.3+ with no deprecated APIs. GDScript is shown first, C# follows.

**Related skills:** See **multiplayer-sync** for state synchronization and interpolation. See **dedicated-server** for headless export and server deployment.

---

## 1. Multiplayer Architecture

Godot uses a **client-server model** built on top of `MultiplayerAPI`. One peer acts as the server; all others are clients. Every peer has a unique integer ID assigned by the network layer:

| Peer ID | Role |
|---------|------|
| `1` | The server (always) |
| `2`, `3`, … | Connected clients |

**Multiplayer authority** is the concept of ownership over a node. Only the authoritative peer should read input and drive that node's state. By default the server (peer `1`) is the authority for every node. Call `set_multiplayer_authority(peer_id)` to transfer ownership to a client.

```
Server (peer 1)
    ├── Owns game state by default
    ├── Spawns and validates objects
    └── Routes RPCs
Client (peer 2, 3, …)
    ├── Sends input to server via RPC
    └── Receives state updates from server
```

---

## 2. Setting Up ENetMultiplayerPeer

### GDScript

```gdscript
# network_manager.gd — add as autoload named NetworkManager
extends Node

const DEFAULT_PORT := 7777
const MAX_CLIENTS  := 16

var peer: ENetMultiplayerPeer


func host_game(port: int = DEFAULT_PORT) -> void:
	peer = ENetMultiplayerPeer.new()
	var err := peer.create_server(port, MAX_CLIENTS)
	if err != OK:
		push_error("NetworkManager: create_server failed — error %d" % err)
		return
	multiplayer.multiplayer_peer = peer
	_connect_signals()
	print("NetworkManager: hosting on port %d" % port)


func join_game(address: String, port: int = DEFAULT_PORT) -> void:
	peer = ENetMultiplayerPeer.new()
	var err := peer.create_client(address, port)
	if err != OK:
		push_error("NetworkManager: create_client failed — error %d" % err)
		return
	multiplayer.multiplayer_peer = peer
	_connect_signals()
	print("NetworkManager: connecting to %s:%d" % [address, port])


func disconnect_from_game() -> void:
	if peer:
		peer.close()
	multiplayer.multiplayer_peer = null


func _connect_signals() -> void:
	multiplayer.peer_connected.connect(_on_peer_connected)
	multiplayer.peer_disconnected.connect(_on_peer_disconnected)
	multiplayer.connected_to_server.connect(_on_connected_to_server)
	multiplayer.connection_failed.connect(_on_connection_failed)


func _on_peer_connected(id: int) -> void:
	print("NetworkManager: peer connected — id %d" % id)


func _on_peer_disconnected(id: int) -> void:
	print("NetworkManager: peer disconnected — id %d" % id)


func _on_connected_to_server() -> void:
	print("NetworkManager: connected to server — my id is %d" % multiplayer.get_unique_id())


func _on_connection_failed() -> void:
	push_error("NetworkManager: connection failed")
```

**Key signal summary:**

| Signal | Fires on | When |
|--------|----------|------|
| `peer_connected` | Server + clients | A new peer finishes connecting |
| `peer_disconnected` | Server + clients | A peer disconnects or times out |
| `connected_to_server` | Client only | This client successfully connected |
| `connection_failed` | Client only | This client could not connect |

### C#

```csharp
// NetworkManager.cs — add as autoload named NetworkManager
using Godot;

public partial class NetworkManager : Node
{
    private const int DefaultPort  = 7777;
    private const int MaxClients   = 16;

    private ENetMultiplayerPeer _peer;

    public void HostGame(int port = DefaultPort)
    {
        _peer = new ENetMultiplayerPeer();
        var err = _peer.CreateServer(port, MaxClients);
        if (err != Error.Ok)
        {
            GD.PushError($"NetworkManager: CreateServer failed — error {err}");
            return;
        }
        Multiplayer.MultiplayerPeer = _peer;
        ConnectSignals();
        GD.Print($"NetworkManager: hosting on port {port}");
    }

    public void JoinGame(string address, int port = DefaultPort)
    {
        _peer = new ENetMultiplayerPeer();
        var err = _peer.CreateClient(address, port);
        if (err != Error.Ok)
        {
            GD.PushError($"NetworkManager: CreateClient failed — error {err}");
            return;
        }
        Multiplayer.MultiplayerPeer = _peer;
        ConnectSignals();
        GD.Print($"NetworkManager: connecting to {address}:{port}");
    }

    public void DisconnectFromGame()
    {
        _peer?.Close();
        Multiplayer.MultiplayerPeer = null;
    }

    private void ConnectSignals()
    {
        Multiplayer.PeerConnected      += OnPeerConnected;
        Multiplayer.PeerDisconnected   += OnPeerDisconnected;
        Multiplayer.ConnectedToServer  += OnConnectedToServer;
        Multiplayer.ConnectionFailed   += OnConnectionFailed;
    }

    private void OnPeerConnected(long id)
        => GD.Print($"NetworkManager: peer connected — id {id}");

    private void OnPeerDisconnected(long id)
        => GD.Print($"NetworkManager: peer disconnected — id {id}");

    private void OnConnectedToServer()
        => GD.Print($"NetworkManager: connected — my id is {Multiplayer.GetUniqueId()}");

    private void OnConnectionFailed()
        => GD.PushError("NetworkManager: connection failed");
}
```

---

## 3. RPCs

`@rpc` (GDScript) / `[Rpc]` (C#) marks a method as callable across the network. Choose the mode and transfer settings carefully — they affect both security and performance.

### RPC Modes

| Mode | Who may call it | Executes on |
|------|-----------------|-------------|
| `"authority"` (default) | Only the authority peer | The peer(s) it is sent to |
| `"any_peer"` | Any connected peer | The peer(s) it is sent to |

### Transfer Modes

| Mode | Delivery | Order | Use For |
|------|----------|-------|---------|
| `"reliable"` | Guaranteed | In-order | Chat, spawn events, important state |
| `"unreliable"` | Best-effort | Unordered | High-frequency position updates |
| `"unreliable_ordered"` | Best-effort | In-order per channel | Smooth movement streams |

### GDScript

```gdscript
# chat.gd
extends Node

# Any peer can call this; executed on the server only.
# The server then broadcasts to all peers.
@rpc("any_peer", "reliable")
func send_chat_message(text: String) -> void:
	if not multiplayer.is_server():
		return
	var sender_id := multiplayer.get_remote_sender_id()
	_broadcast_chat.rpc(sender_id, text)


# Only the authority (server) can call this; runs on every peer.
@rpc("authority", "reliable", "call_local")
func _broadcast_chat(sender_id: int, text: String) -> void:
	print("[%d]: %s" % [sender_id, text])


# Client → server: request to spawn an object.
@rpc("any_peer", "reliable")
func request_spawn(scene_path: String, spawn_position: Vector2) -> void:
	if not multiplayer.is_server():
		return
	# Server validates and performs the actual spawn.
	var scene: PackedScene = load(scene_path)
	if scene == null:
		return
	var instance := scene.instantiate()
	instance.global_position = spawn_position
	get_tree().root.add_child(instance)


# High-frequency position sync — unreliable_ordered is acceptable here.
# transfer_channel separates this stream from other RPC traffic.
@rpc("authority", "unreliable_ordered", "call_local", 1)
func sync_position(pos: Vector2) -> void:
	global_position = pos
```

**Sending to specific peers:**

```gdscript
# Send to everyone (including self if call_local is set):
send_chat_message.rpc("Hello!")

# Send to one specific peer:
send_chat_message.rpc_id(target_peer_id, "Hello!")
```

### C#

```csharp
// Chat.cs
using Godot;

public partial class Chat : Node
{
    // Any peer can call; executes on the server only.
    [Rpc(MultiplayerApi.RpcMode.AnyPeer, TransferMode = MultiplayerPeer.TransferModeEnum.Reliable)]
    public void SendChatMessage(string text)
    {
        if (!Multiplayer.IsServer()) return;
        int senderId = Multiplayer.GetRemoteSenderId();
        Rpc(MethodName.BroadcastChat, senderId, text);
    }

    // Authority only; runs on every peer including the caller.
    [Rpc(MultiplayerApi.RpcMode.Authority,
         CallLocal = true,
         TransferMode = MultiplayerPeer.TransferModeEnum.Reliable)]
    private void BroadcastChat(int senderId, string text)
        => GD.Print($"[{senderId}]: {text}");

    // Client → server: request a spawn.
    [Rpc(MultiplayerApi.RpcMode.AnyPeer, TransferMode = MultiplayerPeer.TransferModeEnum.Reliable)]
    public void RequestSpawn(string scenePath, Vector2 spawnPosition)
    {
        if (!Multiplayer.IsServer()) return;
        var scene = GD.Load<PackedScene>(scenePath);
        if (scene == null) return;
        var instance = scene.Instantiate<Node2D>();
        instance.GlobalPosition = spawnPosition;
        GetTree().Root.AddChild(instance);
    }

    // High-frequency position sync.
    [Rpc(MultiplayerApi.RpcMode.Authority,
         CallLocal = true,
         TransferMode = MultiplayerPeer.TransferModeEnum.UnreliableOrdered,
         TransferChannel = 1)]
    public void SyncPosition(Vector2 pos)
        => GlobalPosition = pos;
}
```

**Sending to specific peers in C#:**

```csharp
// Broadcast to all:
Rpc(MethodName.SendChatMessage, "Hello!");

// Send to one peer:
RpcId(targetPeerId, MethodName.SendChatMessage, "Hello!");
```

---

## 4. Authority Model

Every node has exactly one authoritative peer — the peer that is permitted to send state updates for that node. Other peers should treat incoming state as read-only.

### GDScript

```gdscript
# player.gd
extends CharacterBody2D

func _ready() -> void:
	# multiplayer.get_unique_id() returns this peer's ID.
	# The server assigns authority during spawn (see Section 6).
	pass


func _physics_process(delta: float) -> void:
	# Guard: only the authority peer reads input and moves.
	if not is_multiplayer_authority():
		return

	var direction := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	velocity = direction * 200.0
	move_and_slide()

	# Broadcast position to all other peers.
	sync_position.rpc(global_position)


@rpc("authority", "unreliable_ordered", "call_local", 1)
func sync_position(pos: Vector2) -> void:
	if not is_multiplayer_authority():
		global_position = pos


# Check who owns this node at runtime:
func print_authority_info() -> void:
	print("My peer ID : %d" % multiplayer.get_unique_id())
	print("Authority  : %d" % get_multiplayer_authority())
	print("Am I auth? : %s" % str(is_multiplayer_authority()))
```

### C#

```csharp
// Player.cs
using Godot;

public partial class Player : CharacterBody2D
{
    public override void _PhysicsProcess(double delta)
    {
        // Guard: only the authority peer processes input.
        if (!IsMultiplayerAuthority()) return;

        var direction = Input.GetVector("ui_left", "ui_right", "ui_up", "ui_down");
        Velocity = direction * 200f;
        MoveAndSlide();

        Rpc(MethodName.SyncPosition, GlobalPosition);
    }

    [Rpc(MultiplayerApi.RpcMode.Authority,
         CallLocal = true,
         TransferMode = MultiplayerPeer.TransferModeEnum.UnreliableOrdered,
         TransferChannel = 1)]
    private void SyncPosition(Vector2 pos)
    {
        if (!IsMultiplayerAuthority())
            GlobalPosition = pos;
    }
}
```

**API summary:**

| Method | Returns | Notes |
|--------|---------|-------|
| `multiplayer.get_unique_id()` | `int` | This peer's ID |
| `get_multiplayer_authority()` | `int` | ID of the peer that owns this node |
| `is_multiplayer_authority()` | `bool` | True if this peer owns this node |
| `set_multiplayer_authority(id)` | `void` | Transfer ownership; call on the server |

---

## 5. Spawning Networked Objects

Use **MultiplayerSpawner** to replicate `add_child` calls from the server to all clients automatically. Without it, clients must handle spawning manually and objects will not appear remotely.

### Scene Setup

```
World (Node)
├── MultiplayerSpawner       ← Add this node
│       spawn_path = "../Players"
└── Players (Node)           ← Spawner watches this container
```

### GDScript

```gdscript
# world.gd
extends Node

@onready var spawner: MultiplayerSpawner = $MultiplayerSpawner
@onready var players_container: Node     = $Players


func _ready() -> void:
	# Register scenes the spawner is allowed to replicate.
	spawner.add_spawnable_scene("res://scenes/player.tscn")

	# Optional: custom spawn function lets you pass extra data
	# (e.g. initial position, skin) along with the spawn event.
	spawner.spawn_function = _custom_spawn


func _custom_spawn(data: Variant) -> Node:
	# data is whatever you passed to spawner.spawn(data).
	var scene: PackedScene = load("res://scenes/player.tscn")
	var player: Node = scene.instantiate()
	player.name = str(data["peer_id"])
	player.global_position = data["position"]
	return player


# Call only on the server — MultiplayerSpawner replicates to clients.
func server_spawn_player(peer_id: int, spawn_pos: Vector2) -> void:
	if not multiplayer.is_server():
		return
	var data := {"peer_id": peer_id, "position": spawn_pos}
	var player: Node = spawner.spawn(data)
	player.set_multiplayer_authority(peer_id)
```

### C#

```csharp
// World.cs
using Godot;

public partial class World : Node
{
    [Export] private MultiplayerSpawner _spawner;
    [Export] private Node _playersContainer;

    public override void _Ready()
    {
        _spawner.AddSpawnableScene("res://scenes/player.tscn");
        _spawner.SpawnFunction = new Callable(this, MethodName.CustomSpawn);
    }

    private Node CustomSpawn(Variant data)
    {
        var dict   = data.AsGodotDictionary();
        var scene  = GD.Load<PackedScene>("res://scenes/player.tscn");
        var player = scene.Instantiate<Node2D>();
        player.Name              = dict["peer_id"].As<int>().ToString();
        player.GlobalPosition    = dict["position"].As<Vector2>();
        return player;
    }

    public void ServerSpawnPlayer(int peerId, Vector2 spawnPos)
    {
        if (!Multiplayer.IsServer()) return;
        var data = new Godot.Collections.Dictionary
        {
            ["peer_id"]  = peerId,
            ["position"] = spawnPos,
        };
        var player = _spawner.Spawn(data);
        player.SetMultiplayerAuthority(peerId);
    }
}
```

> **Note:** `spawner.spawn()` must be called on the server. `spawn_path` must point to the container node using a NodePath relative to the MultiplayerSpawner's parent. Every scene passed to `add_spawnable_scene` must be in the project — packed-scene paths are sent over the network.

---

## 6. Player Join Flow

```
Client connects
    └── [server] peer_connected fires with new peer_id
            └── server sends initial world state to new peer  (RPC → new peer)
            └── server calls server_spawn_player(peer_id, spawn_pos)
                    └── MultiplayerSpawner replicates the new node to ALL clients
                    └── server calls set_multiplayer_authority(peer_id) on the new node
            └── server notifies existing clients of the new player  (optional RPC)
```

### GDScript

```gdscript
# game_server.gd  (runs on server only — guard with is_multiplayer_authority / is_server)
extends Node

const SPAWN_POSITIONS: Array[Vector2] = [
	Vector2(100, 300),
	Vector2(200, 300),
	Vector2(300, 300),
	Vector2(400, 300),
]

var _next_spawn_index := 0


func _ready() -> void:
	if not multiplayer.is_server():
		return
	multiplayer.peer_connected.connect(_on_peer_connected)
	multiplayer.peer_disconnected.connect(_on_peer_disconnected)


func _on_peer_connected(peer_id: int) -> void:
	# 1. Send the new client a snapshot of existing players.
	_send_initial_state.rpc_id(peer_id)

	# 2. Spawn a player node for the new peer.
	var spawn_pos := SPAWN_POSITIONS[_next_spawn_index % SPAWN_POSITIONS.size()]
	_next_spawn_index += 1
	$World.server_spawn_player(peer_id, spawn_pos)

	# 3. Notify everyone that a new player joined.
	_notify_player_joined.rpc(peer_id)


func _on_peer_disconnected(peer_id: int) -> void:
	_cleanup_player(peer_id)
	_notify_player_left.rpc(peer_id)


# Runs only on the newly connected client.
@rpc("authority", "reliable")
func _send_initial_state() -> void:
	print("Received initial state from server")
	# Populate local UI, load persistent world state, etc.


# Runs on all peers.
@rpc("authority", "reliable", "call_local")
func _notify_player_joined(peer_id: int) -> void:
	print("Player %d joined" % peer_id)


@rpc("authority", "reliable", "call_local")
func _notify_player_left(peer_id: int) -> void:
	print("Player %d left" % peer_id)


func _cleanup_player(peer_id: int) -> void:
	var player := get_tree().get_first_node_in_group("player_%d" % peer_id)
	if player:
		player.queue_free()
```

### C#

```csharp
// GameServer.cs
using Godot;

public partial class GameServer : Node
{
    private static readonly Vector2[] SpawnPositions =
    {
        new(100, 300), new(200, 300), new(300, 300), new(400, 300),
    };

    private int _nextSpawnIndex;

    public override void _Ready()
    {
        if (!Multiplayer.IsServer()) return;
        Multiplayer.PeerConnected    += OnPeerConnected;
        Multiplayer.PeerDisconnected += OnPeerDisconnected;
    }

    private void OnPeerConnected(long peerId)
    {
        RpcId(peerId, MethodName.SendInitialState);

        var spawnPos = SpawnPositions[_nextSpawnIndex++ % SpawnPositions.Length];
        GetNode<World>("World").ServerSpawnPlayer((int)peerId, spawnPos);

        Rpc(MethodName.NotifyPlayerJoined, (int)peerId);
    }

    private void OnPeerDisconnected(long peerId)
    {
        CleanupPlayer((int)peerId);
        Rpc(MethodName.NotifyPlayerLeft, (int)peerId);
    }

    [Rpc(MultiplayerApi.RpcMode.Authority, TransferMode = MultiplayerPeer.TransferModeEnum.Reliable)]
    private void SendInitialState()
        => GD.Print("Received initial state from server");

    [Rpc(MultiplayerApi.RpcMode.Authority,
         CallLocal = true,
         TransferMode = MultiplayerPeer.TransferModeEnum.Reliable)]
    private void NotifyPlayerJoined(int peerId)
        => GD.Print($"Player {peerId} joined");

    [Rpc(MultiplayerApi.RpcMode.Authority,
         CallLocal = true,
         TransferMode = MultiplayerPeer.TransferModeEnum.Reliable)]
    private void NotifyPlayerLeft(int peerId)
        => GD.Print($"Player {peerId} left");

    private void CleanupPlayer(int peerId)
    {
        var player = GetTree().GetFirstNodeInGroup($"player_{peerId}");
        player?.QueueFree();
    }
}
```

---

## 7. Disconnect Handling

### Timeout Detection

ENet detects broken connections automatically after a configurable timeout (~30 s by default). `peer_disconnected` fires on both sides when the timeout expires.

### GDScript

```gdscript
# disconnect_handler.gd
extends Node

# Track active peer IDs so we know what to clean up.
var _connected_peers: Dictionary = {}   # peer_id → player_node


func register_peer(peer_id: int, player_node: Node) -> void:
	_connected_peers[peer_id] = player_node


func _ready() -> void:
	multiplayer.peer_disconnected.connect(_on_peer_disconnected)
	# Clients also handle losing the server connection.
	multiplayer.server_disconnected.connect(_on_server_disconnected)


func _on_peer_disconnected(peer_id: int) -> void:
	if _connected_peers.has(peer_id):
		var player: Node = _connected_peers[peer_id]
		if is_instance_valid(player):
			player.queue_free()
		_connected_peers.erase(peer_id)
	print("Cleaned up peer %d" % peer_id)


func _on_server_disconnected() -> void:
	# Server dropped — return to main menu.
	print("Lost connection to server — returning to main menu")
	multiplayer.multiplayer_peer = null
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")


# Reconnection: simply call NetworkManager.join_game() again.
# Godot does not have built-in reconnect; implement a retry loop:
func attempt_reconnect(address: String, port: int, max_attempts: int = 3) -> void:
	for attempt in range(max_attempts):
		print("Reconnect attempt %d / %d" % [attempt + 1, max_attempts])
		NetworkManager.join_game(address, port)
		await multiplayer.connected_to_server
		return   # Success — connected_to_server fired.
	push_error("Failed to reconnect after %d attempts" % max_attempts)
```

### C#

```csharp
// DisconnectHandler.cs
using System.Collections.Generic;
using Godot;

public partial class DisconnectHandler : Node
{
    private readonly Dictionary<long, Node> _connectedPeers = new();

    public void RegisterPeer(long peerId, Node playerNode)
        => _connectedPeers[peerId] = playerNode;

    public override void _Ready()
    {
        Multiplayer.PeerDisconnected   += OnPeerDisconnected;
        Multiplayer.ServerDisconnected += OnServerDisconnected;
    }

    private void OnPeerDisconnected(long peerId)
    {
        if (_connectedPeers.TryGetValue(peerId, out var player))
        {
            if (GodotObject.IsInstanceValid(player))
                player.QueueFree();
            _connectedPeers.Remove(peerId);
        }
        GD.Print($"Cleaned up peer {peerId}");
    }

    private void OnServerDisconnected()
    {
        GD.Print("Lost connection to server — returning to main menu");
        Multiplayer.MultiplayerPeer = null;
        GetTree().ChangeSceneToFile("res://scenes/main_menu.tscn");
    }
}
```

> **Always check `is_instance_valid(node)`** before accessing a node reference that may have been freed. `peer_disconnected` and `queue_free` can race in the same frame.

---

## 8. Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Calling an RPC on the wrong authority | `rpc_id` silently ignored; method never runs | Check `is_multiplayer_authority()` before sending; use `"any_peer"` only where intentional |
| Desync from unordered RPCs | Positions jitter or snap | Use `"unreliable_ordered"` for streams; use `"reliable"` for critical state changes |
| Reading input in `_process` vs `_physics_process` | Movement desyncs on different frame rates | Always move `CharacterBody2D` in `_physics_process`; send sync RPCs from there too |
| Not checking `is_multiplayer_authority()` before input | Every peer controls every player | Add an `if not is_multiplayer_authority(): return` guard at the top of input handling |
| Spawning without `MultiplayerSpawner` | Object appears on server, missing on clients | Every runtime `add_child` on the server that should be replicated must go through `MultiplayerSpawner.spawn()` |
| Forgetting `call_local` on authority RPCs | Server state diverges from its own node | Add `"call_local"` when the sender also needs to execute the RPC locally |
| Using `rpc()` before the peer is assigned | Crash or silent failure | Assign `multiplayer.multiplayer_peer` before calling any RPC |
| Not stripping `res://` scenes from exported builds | Clients can read server-only scripts | Use `export_exclude` or PCK encryption for sensitive server code |

---

## 9. Checklist

- [ ] `ENetMultiplayerPeer.create_server()` / `create_client()` return `OK` before assigning to `multiplayer.multiplayer_peer`
- [ ] All four multiplayer signals connected: `peer_connected`, `peer_disconnected`, `connected_to_server`, `connection_failed`
- [ ] Every node that reads player input guards with `if not is_multiplayer_authority(): return`
- [ ] Input processing and `sync_position` RPC are both in `_physics_process`, not `_process`
- [ ] RPC modes chosen deliberately: `"any_peer"` only for client → server calls; `"authority"` for server → client
- [ ] Unreliable RPCs used only for high-frequency updates (position, rotation); reliable for events (spawn, damage, chat)
- [ ] `MultiplayerSpawner` configured with all spawnable scenes before the first player joins
- [ ] `set_multiplayer_authority(peer_id)` called on the server after each player node is spawned
- [ ] `peer_disconnected` handler frees the player node and removes it from tracking collections
- [ ] `server_disconnected` handler on clients returns to main menu and nulls `multiplayer.multiplayer_peer`
- [ ] `is_instance_valid()` checked before dereferencing any stored node reference in disconnect callbacks
- [ ] No `rpc()` calls made before `multiplayer.multiplayer_peer` is assigned
