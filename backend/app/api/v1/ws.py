"""WebSocket API — real-time updates for transactions, balances, alerts."""

import json
import logging
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

router = APIRouter(tags=["websocket"])


class ConnectionManager:
    """Manages active WebSocket connections per tenant/user."""

    def __init__(self) -> None:
        self._connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str) -> None:
        await websocket.accept()
        if user_id not in self._connections:
            self._connections[user_id] = []
        self._connections[user_id].append(websocket)
        logger.info("WebSocket connected user=%s total=%d", user_id, len(self._connections[user_id]))

    def disconnect(self, websocket: WebSocket, user_id: str) -> None:
        if user_id in self._connections:
            self._connections[user_id] = [ws for ws in self._connections[user_id] if ws != websocket]
            if not self._connections[user_id]:
                del self._connections[user_id]
        logger.info("WebSocket disconnected user=%s", user_id)

    async def send_to_user(self, user_id: str, event: str, data: dict[str, Any]) -> None:
        """Send a message to all connections for a specific user."""
        connections = self._connections.get(user_id, [])
        message = json.dumps({"event": event, "data": data})
        disconnected: list[WebSocket] = []
        for ws in connections:
            try:
                await ws.send_text(message)
            except Exception:
                disconnected.append(ws)

        for ws in disconnected:
            self.disconnect(ws, user_id)

    async def broadcast_to_tenant(self, tenant_id: str, event: str, data: dict[str, Any]) -> None:
        """Broadcast to all users in a tenant (for admin alerts)."""
        message = json.dumps({"event": event, "data": data})
        for user_id, connections in self._connections.items():
            for ws in connections:
                try:
                    await ws.send_text(message)
                except Exception:
                    pass


manager = ConnectionManager()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str) -> None:
    """WebSocket connection for real-time events.

    Requires a valid JWT token passed as ?token= query parameter.
    Events pushed to client:
    - transaction.completed — when a transfer completes
    - transaction.failed — when a transfer fails
    - balance.updated — when account balance changes
    - compliance.alert — when a compliance issue is detected
    - kyc.status_changed — when KYC verification status updates
    """
    # Authenticate before accepting connection
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008, reason="Authentication required")
        return

    # Validate token claims match the requested user_id
    try:
        from app.middleware.auth import decode_token
        claims = decode_token(token)
        if claims.get("sub") != user_id:
            await websocket.close(code=1008, reason="Token does not match user_id")
            return
    except Exception:
        await websocket.close(code=1008, reason="Invalid token")
        return

    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text(json.dumps({"event": "pong"}))
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)


# Export manager for use in services
def get_ws_manager() -> ConnectionManager:
    return manager
