import os
import sqlite3
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Vanna imports
from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.core.user import UserResolver, User

# Gemini LLM
from vanna.integrations.google import GeminiLlmService

# -----------------------------
# STEP 1: Setup LLM
# -----------------------------

llm = GeminiLlmService(
    model="gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# -----------------------------
# STEP 2: Setup SQLite Runner
# -----------------------------

print("USING CORRECT SQLITE RUNNER")

conn = sqlite3.connect("clinic.db")
sql_runner = SqliteRunner(conn)

# -----------------------------
# STEP 3: Tool Registry
# -----------------------------

tool_registry = ToolRegistry()
tool_registry.tools = [
    RunSqlTool(sql_runner),
    VisualizeDataTool(),
    SaveQuestionToolArgsTool(),
    SearchSavedCorrectToolUsesTool()
]

# -----------------------------
# STEP 4: Memory
# -----------------------------

memory = DemoAgentMemory()

# -----------------------------
# STEP 5: User Resolver
# -----------------------------

class SimpleUserResolver(UserResolver):
    def resolve_user(self, request_context):
        return User(id="default_user")

# -----------------------------
# STEP 6: Create Agent
# -----------------------------

agent = Agent(
    llm_service=llm,
    tool_registry=tool_registry,
    user_resolver=SimpleUserResolver(),
    agent_memory=memory
)

print("Vanna Agent Initialized Successfully!")
print("API KEY:", os.getenv("GOOGLE_API_KEY"))