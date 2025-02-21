import sqlite3
import json
from xai_components.base import InArg, OutArg, Component, xai_component

@xai_component
class BufferOpenDB(Component):
    """Component to open the SQLite database for storing conversations."""
    
    db_file: InArg[str]  # Path to the SQLite database file
    connection: OutArg[sqlite3.Connection]  # Output connection to the database

    def execute(self, ctx) -> None:
        conn = sqlite3.connect(self.db_file.value)
        cursor = conn.cursor()
        
        # Create the buffer table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS buffer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                context_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                has_media BOOLEAN DEFAULT 0
            )
        ''')
        conn.commit()
        self.connection.value = conn
        ctx['buffer_conn'] = conn

@xai_component
class BufferCloseDB(Component):
    """Component to close the SQLite database connection."""
    
    connection: InArg[sqlite3.Connection]

    def execute(self, ctx) -> None:
        conn = self.connection.value if self.connection.value is not None else ctx['buffer_conn']
        conn.close()

@xai_component
class BufferAddMessage(Component):
    """Component to add a message to the buffer."""
    
    connection: InArg[sqlite3.Connection]
    context_id: InArg[str]
    role: InArg[str]
    content: InArg[str]  # Content can be a plain string or a JSON string
    has_media: OutArg[bool]  # Output flag indicating if the content has media

    def execute(self, ctx) -> None:
        # Check if content is a plain string or not
        try:
            json.loads(self.content.value)  # Try to parse as JSON
            has_media = 0  # It's a JSON string
        except (ValueError, TypeError):
            has_media = 1  # It's a plain string or non-JSON content

        conn = self.connection.value if self.connection.value is not None else ctx['buffer_conn']
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO buffer (context_id, role, content, has_media)
            VALUES (?, ?, ?, ?)
        ''', (self.context_id.value, self.role.value, self.content.value, has_media))
        conn.commit()
        self.has_media.value = bool(has_media)

@xai_component
class BufferListMessages(Component):
    """Component to list messages from the buffer."""
    
    connection: InArg[sqlite3.Connection]
    context_id: InArg[str]
    n: InArg[int]  # Number of latest messages to return
    only_text: InArg[bool]  # Flag to filter out media messages
    messages: OutArg[list]  # Output list of messages

    def execute(self, ctx) -> None:
        conn = self.connection.value if self.connection.value is not None else ctx['buffer_conn']
        cursor = conn.cursor()
        
        # Build the query based on the only_text flag
        if self.only_text.value:
            cursor.execute('''
                SELECT role, content FROM buffer
                WHERE context_id = ? AND has_media = 0
                ORDER BY id ASC
            ''', (self.context_id.value,))
        else:
            cursor.execute('''
                SELECT role, content FROM buffer
                WHERE context_id = ?
                ORDER BY id ASC
            ''', (self.context_id.value,))
        
        rows = cursor.fetchall()
        
        # Prepare the messages list
        messages = [{'role': row[0], 'content': row[1]} for row in rows]
        
        # Return the first message and the n latest messages
        if messages:
            self.messages.value = messages[:1] + messages[-self.n.value:]  # First message + latest n messages
        else:
            self.messages.value = []
