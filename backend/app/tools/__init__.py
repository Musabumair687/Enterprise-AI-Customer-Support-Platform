"""
Application tool layer.

Tools are small, typed adapters around business services.  An agent or future
LangGraph node calls a tool with a Pydantic input model; the tool validates the
input, delegates to the appropriate service, and returns a Pydantic output
model.  Tools never embed SQL statements or bypass service-layer checks.
"""
