# Xircuits Conversation Buffer

A Xircuits component library for managing conversational context in agent applications. This library provides SQLite-based conversation buffer components that help maintain conversation history and context for AI agents built with Xircuits.

## Features

- Persistent storage of conversations using SQLite
- Support for multiple conversation contexts
- Ability to retrieve recent conversation history
- Handle both text and media content
- Simple interface for adding and retrieving messages

## Installation

To use this component library, ensure you have Xircuits installed, then run:

```
xircuits install https://github.com/XpressAI/xai-conversation-buffer
```

Alternatively, you can manually clone the repository to your Xircuits project directory and install dependencies:

```
pip install -r requirements.txt
```

## Components

- **BufferOpenDB**: Opens or creates a SQLite database for storing conversations
- **BufferCloseDB**: Safely closes the database connection
- **BufferAddMessage**: Adds a new message to the conversation buffer
- **BufferListMessages**: Retrieves conversation history with configurable parameters

## Usage

1. Open a database connection using `BufferOpenDB`
2. Add messages to the conversation using `BufferAddMessage`
3. Retrieve conversation history using `BufferListMessages`
4. Close the database connection with `BufferCloseDB`

The buffer stores messages with the following information:
- Context ID (for managing multiple conversations)
- Role (e.g., "user", "assistant")
- Content (text or JSON content)
- Media flag (indicates if the content includes media)

## Example

Check out the example workflows in the `examples` directory to see how to use these components in your agent applications.
