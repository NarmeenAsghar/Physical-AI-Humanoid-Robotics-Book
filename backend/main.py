"""
RAG Chatbot Backend - FastAPI Application
=========================================
A Retrieval-Augmented Generation chatbot for the Physical AI & Humanoid Robotics book.
Answers questions exclusively from book content with source citations.

This version uses a FREE simulated LLM - no paid API keys required!

Spec Reference: specs/002-rag-chatbot/spec.yaml
"""

import os
import time
import uuid
import re
from datetime import datetime, timedelta
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

# from utils import (
#     embed_text,
#     retrieve_from_qdrant,
#     get_qdrant_client,
#     get_neon_connection,  # <- comment or remove this line
#     init_qdrant_collection,
# )
from utils import (
    embed_text,
    retrieve_from_qdrant,
    get_qdrant_client,
    init_qdrant_collection,
)


# Load environment variables
load_dotenv()

# =============================================================================
# CONFIGURATION
# =============================================================================

class Settings:
    """Application settings from environment variables."""
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "5"))
    SCORE_THRESHOLD: float = float(os.getenv("SCORE_THRESHOLD", "0.5"))

settings = Settings()

# =============================================================================
# FREE LLM FUNCTION (NO PAID API REQUIRED)
# =============================================================================

def call_llm(prompt: str, context: str, query: str, selected_text: Optional[str] = None) -> str:
    """
    Free LLM function that generates answers based on retrieved context.

    This is a simulated LLM that extracts and formats relevant information
    from the retrieved book content. No paid API required!

    For production, you can replace this with:
    - Ollama (free, local): https://ollama.ai
    - LM Studio (free, local): https://lmstudio.ai
    - HuggingFace Inference (free tier): https://huggingface.co/inference-api

    Args:
        prompt: The system prompt with instructions
        context: Retrieved book content chunks
        query: The user's question
        selected_text: Optional text the user selected

    Returns:
        Generated answer string based on context
    """
    # Parse context to extract key information
    context_lines = context.strip().split('\n\n')

    # If no context, return appropriate message
    if not context or context.strip() == "":
        return (
            "I couldn't find specific information about this in the book. "
            "Try asking about topics like ROS2, digital twins, kinematics, "
            "simulation, or humanoid robotics."
        )

    # Extract the most relevant content
    relevant_content = []
    for chunk in context_lines:
        if chunk.strip():
            # Remove chunk numbers like [1], [2]
            clean_chunk = re.sub(r'^\[\d+\]\s*', '', chunk.strip())
            if clean_chunk:
                relevant_content.append(clean_chunk)

    if not relevant_content:
        return "I found some content but couldn't extract a clear answer. Please try rephrasing your question."

    # Build a structured answer from the context
    answer_parts = []

    # Generate introductory sentence based on the query
    query_lower = query.lower()

    if "what is" in query_lower or "what are" in query_lower:
        intro = "Based on the book content:\n\n"
    elif "how" in query_lower:
        intro = "According to the book:\n\n"
    elif "why" in query_lower:
        intro = "The book explains:\n\n"
    elif "explain" in query_lower:
        intro = "Here's an explanation from the book:\n\n"
    elif selected_text:
        intro = "Regarding the selected text:\n\n"
    else:
        intro = "From the book content:\n\n"

    answer_parts.append(intro)

    # Add the most relevant content (first 2-3 chunks)
    for i, content in enumerate(relevant_content[:3]):
        # Truncate if too long
        if len(content) > 500:
            content = content[:500] + "..."

        if i == 0:
            answer_parts.append(content)
        else:
            answer_parts.append(f"\n\nAdditionally:\n{content}")

    # Add selected text explanation if present
    if selected_text:
        answer_parts.append(f"\n\n**About your selected text:** The passage you highlighted relates to the concepts discussed above.")

    return "".join(answer_parts)


# =============================================================================
# PYDANTIC SCHEMAS
# =============================================================================

class ChatRequest(BaseModel):
    """Request schema for /chat endpoint."""
    session_id: Optional[str] = Field(default=None, description="Session UUID")
    query: str = Field(..., min_length=1, max_length=1000, description="User question")
    selected_text: Optional[str] = Field(default=None, max_length=2000, description="Selected text context")
    current_page: Optional[str] = Field(default=None, description="Current book page path")

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Validate and sanitize query input."""
        v = v.strip()
        if not v:
            raise ValueError("Query cannot be empty")
        return v


class Source(BaseModel):
    """Source citation schema."""
    chapter: str
    section: str
    relevance_score: float
    content_preview: Optional[str] = None


class ChatResponse(BaseModel):
    """Response schema for /chat endpoint."""
    session_id: str
    response: dict  # Contains answer, sources, confidence
    intent: str
    processing_time_ms: int


class SessionRequest(BaseModel):
    """Request schema for /session endpoint."""
    initial_page: Optional[str] = None


class SessionResponse(BaseModel):
    """Response schema for /session endpoint."""
    session_id: str
    expires_at: str


class HealthResponse(BaseModel):
    """Response schema for /health endpoint."""
    status: str
    version: str
    dependencies: dict


# =============================================================================
# IN-MEMORY SESSION STORAGE
# =============================================================================

class SessionStore:
    """In-memory session storage with timeout."""

    def __init__(self, timeout_minutes: int = 30):
        self._sessions: dict = {}
        self._timeout = timedelta(minutes=timeout_minutes)

    def create_session(self, initial_page: Optional[str] = None) -> dict:
        """Create a new session."""
        session_id = str(uuid.uuid4())
        now = datetime.utcnow()
        session = {
            "id": session_id,
            "created_at": now,
            "last_activity": now,
            "expires_at": now + self._timeout,
            "messages": [],
            "current_page": initial_page,
        }
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session by ID, return None if expired or not found."""
        session = self._sessions.get(session_id)
        if not session:
            return None

        now = datetime.utcnow()
        if now > session["expires_at"]:
            del self._sessions[session_id]
            return None

        # Update last activity
        session["last_activity"] = now
        session["expires_at"] = now + self._timeout
        return session

    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Add a message to session history."""
        session = self.get_session(session_id)
        if session:
            session["messages"].append({
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow().isoformat()
            })
            # Keep only last 10 messages for context
            if len(session["messages"]) > 10:
                session["messages"] = session["messages"][-10:]

    def cleanup_expired(self) -> int:
        """Remove expired sessions. Returns count of removed sessions."""
        now = datetime.utcnow()
        expired = [sid for sid, s in self._sessions.items() if now > s["expires_at"]]
        for sid in expired:
            del self._sessions[sid]
        return len(expired)


# Global session store
session_store = SessionStore(timeout_minutes=settings.SESSION_TIMEOUT_MINUTES)

# =============================================================================
# INTENT CLASSIFIER
# =============================================================================

class IntentClassifier:
    """Rule-based intent classification for user messages."""

    GREETING_PATTERNS = [
        r"^(hi|hello|hey|greetings|good\s*(morning|afternoon|evening))[\s!.,]*$",
        r"^(what'?s\s*up|howdy|yo)[\s!.,]*$",
    ]

    HELP_PATTERNS = [
        r"^(help|how\s*(do|can)\s*(i|you)|what\s*can\s*you\s*do)",
        r"(show|tell)\s*me\s*(how|what)",
        r"^(usage|instructions|guide)$",
    ]

    CLARIFICATION_PATTERNS = [
        r"^(what|how)\s*(do\s*you\s*mean|does\s*that\s*mean)",
        r"^(can\s*you\s*)?(explain|elaborate|clarify)",
        r"^(tell\s*me\s*)?more(\s*about\s*(that|this))?$",
        r"^(and|also|what\s*about)\b",
    ]

    # Book topic keywords for content detection
    BOOK_TOPICS = [
        "ros2", "ros", "robot", "humanoid", "kinematics", "inverse kinematics",
        "digital twin", "simulation", "isaac", "nvidia", "vla", "vision",
        "language", "action", "control", "sensor", "actuator", "joint",
        "trajectory", "planning", "perception", "manipulation", "locomotion",
        "denavit", "hartenberg", "urdf", "gazebo", "rviz", "tf", "transform",
        "node", "topic", "service", "publisher", "subscriber", "message",
        "physical ai", "embodied", "reinforcement learning", "imitation",
    ]

    def classify(
        self,
        message: str,
        selected_text: Optional[str] = None,
        chat_history: Optional[list] = None
    ) -> str:
        """
        Classify user intent.

        Returns one of:
        - content_query: Question about book content
        - selection_query: Question about selected text
        - clarification: Follow-up question
        - greeting: Social greeting
        - help: Request for usage help
        - out_of_scope: Query outside book content
        """
        message_lower = message.lower().strip()

        # Check for greetings
        for pattern in self.GREETING_PATTERNS:
            if re.match(pattern, message_lower, re.IGNORECASE):
                return "greeting"

        # Check for help requests
        for pattern in self.HELP_PATTERNS:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return "help"

        # Check for selection query (has selected text + short/contextual query)
        if selected_text:
            if len(message_lower.split()) <= 10:  # Short query with selection
                return "selection_query"
            # Check for selection-related phrases
            if any(phrase in message_lower for phrase in [
                "this", "explain this", "what does this mean", "break this down",
                "simplify", "in simpler terms", "what is this"
            ]):
                return "selection_query"

        # Check for clarification (has chat history + clarification patterns)
        if chat_history and len(chat_history) > 0:
            for pattern in self.CLARIFICATION_PATTERNS:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    return "clarification"
            # Short follow-up with history
            if len(message_lower.split()) <= 5:
                return "clarification"

        # Check for book content topics
        for topic in self.BOOK_TOPICS:
            if topic in message_lower:
                return "content_query"

        # Check if it's a question (ends with ? or starts with question words)
        question_words = ["what", "how", "why", "when", "where", "which", "who", "can", "does", "is", "are"]
        if message_lower.endswith("?") or any(message_lower.startswith(qw) for qw in question_words):
            return "content_query"

        # Default to content_query to be more permissive
        return "content_query"


# Global intent classifier
intent_classifier = IntentClassifier()

# =============================================================================
# AGENTS
# =============================================================================

class BaseAgent:
    """Base class for agents."""

    def __init__(self, name: str):
        self.name = name

    async def handle(self, **kwargs) -> dict:
        """Handle a request. Override in subclasses."""
        raise NotImplementedError


class ContentAgent(BaseAgent):
    """
    Handles book content queries.
    Orchestrates retrieval and generates cited responses using FREE LLM.
    """

    SYSTEM_PROMPT = """You are a knowledgeable assistant for the Physical AI & Humanoid Robotics book.

CONSTRAINTS:
- ONLY answer questions using information from the retrieved book content provided below
- NEVER use external knowledge or make assumptions beyond the provided content
- ALWAYS cite the chapter and section for your answers
- If the retrieved content doesn't contain the answer, say "I couldn't find specific information about this in the book"
- Keep responses concise and technically accurate

RETRIEVED BOOK CONTENT:
{context}

USER QUESTION: {query}
{selection_context}"""

    def __init__(self):
        super().__init__("ContentAgent")

    async def handle(
        self,
        query: str,
        selected_text: Optional[str] = None,
        chat_history: Optional[list] = None,
    ) -> dict:
        """
        Handle a content query.

        Pipeline:
        1. Generate query embedding
        2. Retrieve relevant chunks from Qdrant
        3. Call FREE LLM function with context
        4. Format with citations
        """
        # Step 1: Prepare query (combine with selection if present)
        search_query = query
        if selected_text:
            search_query = f"{query}\n\nContext: {selected_text[:500]}"

        # Step 2: Retrieve from Qdrant (uses local embedded mode)
        # The retrieve_from_qdrant function handles embedding internally
        try:
            retrieved_chunks = retrieve_from_qdrant(
                query=search_query,
                top_k=settings.TOP_K_RESULTS,
                score_threshold=settings.SCORE_THRESHOLD
            )
        except Exception as e:
            print(f"Error in retrieval: {e}")
            retrieved_chunks = []

        # Step 3: Build context from retrieved chunks
        if not retrieved_chunks:
            return {
                "answer": "I couldn't find relevant information in the book for your question. "
                         "Try rephrasing or asking about specific topics like ROS2, digital twins, "
                         "kinematics, or humanoid robotics.",
                "sources": [],
                "confidence": 0.0,
                "is_from_book": False,
            }

        # Build context and sources
        context_parts = []
        sources = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            context_parts.append(f"[{i}] {chunk['content']}")
            sources.append(Source(
                chapter=chunk.get("chapter", "Unknown"),
                section=chunk.get("section", "Unknown"),
                relevance_score=round(chunk.get("score", 0.0), 3),
                content_preview=chunk["content"][:150] + "..." if len(chunk["content"]) > 150 else chunk["content"]
            ))

        context = "\n\n".join(context_parts)

        # Step 4: Generate response with FREE LLM
        selection_context = ""
        if selected_text:
            selection_context = f"\n\nUSER SELECTED TEXT: {selected_text[:500]}"

        prompt = self.SYSTEM_PROMPT.format(
            context=context,
            query=query,
            selection_context=selection_context
        )

        # Call the FREE LLM function
        answer = call_llm(
            prompt=prompt,
            context=context,
            query=query,
            selected_text=selected_text
        )

        # Step 5: Calculate confidence based on retrieval scores
        avg_score = sum(s.relevance_score for s in sources) / len(sources) if sources else 0
        confidence = min(avg_score + 0.1, 1.0)  # Slight boost for having results

        return {
            "answer": answer,
            "sources": [s.model_dump() for s in sources],
            "confidence": round(confidence, 3),
            "is_from_book": True,
        }


class UserAgent(BaseAgent):
    """
    Handles user interactions.
    Classifies intent and routes to appropriate handler.
    """

    GREETING_RESPONSE = (
        "Hello! I'm here to help you understand the Physical AI & Humanoid Robotics book. "
        "Ask me anything about ROS2, digital twins, kinematics, humanoid robots, or any "
        "topic covered in the book!"
    )

    HELP_RESPONSE = (
        "I can help you with:\n\n"
        "- **Answering questions** about book content (e.g., 'What is inverse kinematics?')\n"
        "- **Explaining selected text** - Select text in the book and ask 'explain this'\n"
        "- **Follow-up questions** - Ask for more details on previous answers\n"
        "- **Finding related topics** - I'll point you to relevant sections\n\n"
        "Try asking: 'How does ROS2 handle message passing?' or select a code snippet "
        "and ask 'break this down for me'!"
    )

    OUT_OF_SCOPE_RESPONSE = (
        "I can only answer questions about the Physical AI & Humanoid Robotics book content. "
        "Your question seems to be outside the book's scope. Could you rephrase it to relate "
        "to topics like ROS2, digital twins, simulation, kinematics, or humanoid robotics?"
    )

    def __init__(self):
        super().__init__("UserAgent")
        self.content_agent = ContentAgent()

    async def handle(
        self,
        message: str,
        selected_text: Optional[str] = None,
        session_id: Optional[str] = None,
        current_page: Optional[str] = None,
    ) -> dict:
        """
        Handle user message.

        1. Get or create session
        2. Classify intent
        3. Route to appropriate handler
        4. Update session
        5. Return response
        """
        # Get or create session
        session = None
        if session_id:
            session = session_store.get_session(session_id)

        if not session:
            session = session_store.create_session(initial_page=current_page)

        session_id = session["id"]
        chat_history = session.get("messages", [])

        # Classify intent
        intent = intent_classifier.classify(
            message=message,
            selected_text=selected_text,
            chat_history=chat_history
        )

        # Route based on intent
        if intent == "greeting":
            response = {"answer": self.GREETING_RESPONSE, "sources": [], "confidence": 1.0, "is_from_book": False}

        elif intent == "help":
            response = {"answer": self.HELP_RESPONSE, "sources": [], "confidence": 1.0, "is_from_book": False}

        elif intent == "out_of_scope":
            response = {"answer": self.OUT_OF_SCOPE_RESPONSE, "sources": [], "confidence": 1.0, "is_from_book": False}

        elif intent in ["content_query", "selection_query", "clarification"]:
            # Route to ContentAgent
            response = await self.content_agent.handle(
                query=message,
                selected_text=selected_text,
                chat_history=chat_history
            )

        else:
            # Default to content query
            response = await self.content_agent.handle(
                query=message,
                selected_text=selected_text,
                chat_history=chat_history
            )

        # Update session with messages
        session_store.add_message(session_id, "user", message)
        session_store.add_message(session_id, "assistant", response["answer"])

        return {
            "session_id": session_id,
            "response": response,
            "intent": intent,
        }


# Global user agent
user_agent = UserAgent()

# =============================================================================
# FASTAPI APPLICATION
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown."""
    # Startup
    print("=" * 60)
    print("Starting RAG Chatbot Backend (FREE - No Paid APIs!)")
    print("=" * 60)

    # Initialize Qdrant collection if needed
    try:
        init_qdrant_collection()
        print("✓ Qdrant collection initialized")
    except Exception as e:
        print(f"⚠ Warning: Could not initialize Qdrant: {e}")

    # Preload embedding model
    try:
        _ = embed_text("warmup")
        print("✓ Embedding model loaded (sentence-transformers)")
    except Exception as e:
        print(f"⚠ Warning: Could not preload embedding model: {e}")

    print("✓ Using FREE simulated LLM (no API key required)")
    print("=" * 60)
    print("Server ready! Visit http://localhost:8000/docs for API docs")
    print("=" * 60)

    yield

    # Shutdown
    print("Shutting down RAG Chatbot Backend...")


app = FastAPI(
    title="RAG Book Chatbot API (FREE)",
    description="Retrieval-Augmented Generation chatbot for the Physical AI & Humanoid Robotics book. "
                "Uses FREE local embeddings and simulated LLM - no paid API keys required!",
    version="1.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Send a message to the chatbot.

    - Accepts user query and optional selected text context
    - Classifies intent and routes to appropriate agent
    - Returns answer with source citations
    - Uses FREE local processing (no paid APIs)
    """
    start_time = time.time()

    try:
        result = await user_agent.handle(
            message=request.query,
            selected_text=request.selected_text,
            session_id=request.session_id,
            current_page=request.current_page,
        )

        processing_time_ms = int((time.time() - start_time) * 1000)

        return ChatResponse(
            session_id=result["session_id"],
            response=result["response"],
            intent=result["intent"],
            processing_time_ms=processing_time_ms,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )


@app.post("/chat")
async def chat_simple(request: ChatRequest):
    """
    Simplified chat endpoint (alternative to /api/v1/chat).

    Accepts: {"query": "...", "selected_text": "..."}
    Returns: {"answer": "...", "sources": [...]}
    """
    start_time = time.time()

    try:
        result = await user_agent.handle(
            message=request.query,
            selected_text=request.selected_text,
            session_id=request.session_id,
            current_page=request.current_page,
        )

        processing_time_ms = int((time.time() - start_time) * 1000)

        return {
            "answer": result["response"]["answer"],
            "sources": result["response"]["sources"],
            "confidence": result["response"]["confidence"],
            "intent": result["intent"],
            "processing_time_ms": processing_time_ms,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )


@app.post("/api/v1/session", response_model=SessionResponse)
async def create_session(request: SessionRequest) -> SessionResponse:
    """Create a new chat session."""
    session = session_store.create_session(initial_page=request.initial_page)

    return SessionResponse(
        session_id=session["id"],
        expires_at=session["expires_at"].isoformat() + "Z",
    )


@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns status of all dependencies.
    """
    dependencies = {}

    # Check Qdrant
    try:
        client = get_qdrant_client()
        if client:
            client.get_collections()
            dependencies["qdrant"] = "connected"
        else:
            dependencies["qdrant"] = "not_configured"
    except Exception as e:
        dependencies["qdrant"] = f"error: {str(e)}"

    # Check Neon Postgres
# Skip Neon Postgres (we are using FREE local RAG)
        dependencies["neon"] = "not_configured"


    # Check embedding model
    try:
        _ = embed_text("test")
        dependencies["embedding_model"] = "loaded"
    except Exception as e:
        dependencies["embedding_model"] = f"error: {str(e)}"

    # LLM is always available (free simulated)
    dependencies["llm"] = "free_simulated"

    # Determine overall status
    critical_deps = ["embedding_model"]
    all_ok = all(
        dependencies.get(dep) in ["connected", "loaded", "configured", "not_configured", "free_simulated"]
        for dep in critical_deps
    )

    return HealthResponse(
        status="healthy" if all_ok else "degraded",
        version="1.1.0",
        dependencies=dependencies,
    )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "RAG Book Chatbot API",
        "version": "1.1.0",
        "description": "FREE RAG chatbot - no paid API keys required!",
        "docs": "/docs",
        "health": "/api/v1/health",
        "endpoints": {
            "chat": "POST /chat or POST /api/v1/chat",
            "session": "POST /api/v1/session",
            "health": "GET /api/v1/health",
        }
    }


# =============================================================================
# DEVELOPMENT SERVER
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
