"""
Tool-specific errors.

The agent runtime can catch these predictable errors and return a safe, useful
message instead of exposing a database exception.  API adapters may later map
them to HTTP status codes, while LangGraph can use the error text in a tool
result without treating a normal 'not found' outcome as a system failure.
"""


class ToolError(Exception):
    """Base exception for an expected tool failure."""


class ToolNotFoundError(ToolError):
    """Raised when an entity requested by a tool does not exist."""


class ToolOperationError(ToolError):
    """Raised when a validated write cannot be completed by its service."""


class ToolPermissionDeniedError(ToolError):
    """Raised when an agent is not allowed to invoke a registered tool."""


class InvalidToolInputError(ToolError):
    """Raised by adapters that cannot turn a tool payload into its input schema."""
