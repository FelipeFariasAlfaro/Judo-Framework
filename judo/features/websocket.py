"""
WebSocket Support
Real-time communication testing
"""

import json
import time
from typing import Optional, Dict, Any, Callable, List
from threading import Thread, Event


class WebSocketClient:
    """WebSocket client for real-time testing"""
    
    def __init__(self, url: str):
        """
        Initialize WebSocket client
        
        Args:
            url: WebSocket URL (wss:// or ws://)
        """
        try:
            import websocket
        except ImportError:
            raise ImportError("websocket-client required: pip install websocket-client")
        
        self.url = url
        self.ws = None
        self.connected = False
        self.messages: List[Dict[str, Any]] = []
        self.message_event = Event()
        self.receive_thread = None
    
    def connect(self, timeout: float = 5.0) -> bool:
        """
        Connect to WebSocket
        
        Args:
            timeout: Connection timeout in seconds
        
        Returns:
            True if connected successfully
        """
        try:
            import websocket
            
            self.ws = websocket.WebSocketApp(
                self.url,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            
            # Start receive thread
            self.receive_thread = Thread(target=self.ws.run_forever, daemon=True)
            self.receive_thread.start()
            
            # Wait for connection
            start_time = time.time()
            while not self.connected and (time.time() - start_time) < timeout:
                time.sleep(0.1)
            
            return self.connected
        except Exception as e:
            print(f"❌ WebSocket connection failed: {e}")
            return False
    
    def send(self, data: Dict[str, Any]) -> bool:
        """
        Send message through WebSocket
        
        Args:
            data: Message data (will be JSON encoded)
        
        Returns:
            True if sent successfully
        """
        if not self.connected or not self.ws:
            print("❌ WebSocket not connected")
            return False
        
        try:
            message = json.dumps(data)
            self.ws.send(message)
            return True
        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return False
    
    def send_text(self, text: str) -> bool:
        """
        Send text message through WebSocket
        
        Args:
            text: Text message
        
        Returns:
            True if sent successfully
        """
        if not self.connected or not self.ws:
            print("❌ WebSocket not connected")
            return False
        
        try:
            self.ws.send(text)
            return True
        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return False
    
    def receive(self, timeout: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """
        Receive message from WebSocket
        
        Args:
            timeout: Timeout in seconds
        
        Returns:
            Received message or None if timeout
        """
        if not self.connected:
            print("❌ WebSocket not connected")
            return None
        
        # Wait for message
        if self.message_event.wait(timeout=timeout):
            self.message_event.clear()
            if self.messages:
                return self.messages.pop(0)
        
        return None
    
    def receive_all(self, timeout: float = 1.0) -> List[Dict[str, Any]]:
        """
        Receive all pending messages
        
        Args:
            timeout: Timeout in seconds
        
        Returns:
            List of received messages
        """
        messages = []
        
        while True:
            msg = self.receive(timeout=timeout)
            if msg is None:
                break
            messages.append(msg)
        
        return messages
    
    def close(self):
        """Close WebSocket connection"""
        if self.ws:
            self.ws.close()
            self.connected = False
    
    def _on_message(self, ws, message: str):
        """Handle incoming message"""
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            data = {"text": message}
        
        self.messages.append(data)
        self.message_event.set()
    
    def _on_error(self, ws, error):
        """Handle error"""
        print(f"❌ WebSocket error: {error}")
    
    def _on_close(self, ws, close_status_code, close_msg):
        """Handle close"""
        self.connected = False
        print(f"🔌 WebSocket closed: {close_status_code} {close_msg}")
    
    def is_connected(self) -> bool:
        """Check if connected"""
        return self.connected


class WebSocketServer:
    """Simple WebSocket server for testing"""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        """
        Initialize WebSocket server
        
        Args:
            host: Server host
            port: Server port
        """
        try:
            import websockets
        except ImportError:
            raise ImportError("websockets required: pip install websockets")
        
        self.host = host
        self.port = port
        self.server = None
        self.clients: List = []
    
    async def start(self):
        """Start WebSocket server"""
        try:
            import websockets
            
            async def handler(websocket, path):
                self.clients.append(websocket)
                try:
                    async for message in websocket:
                        # Broadcast to all clients
                        for client in self.clients:
                            if client != websocket:
                                await client.send(message)
                finally:
                    self.clients.remove(websocket)
            
            self.server = await websockets.serve(handler, self.host, self.port)
            print(f"🚀 WebSocket server started on ws://{self.host}:{self.port}")
        except Exception as e:
            print(f"❌ Failed to start WebSocket server: {e}")
    
    async def stop(self):
        """Stop WebSocket server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            print("🔌 WebSocket server stopped")
