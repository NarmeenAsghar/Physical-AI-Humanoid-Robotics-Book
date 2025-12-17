/**
 * RAG Chatbot Component for Docusaurus
 * =====================================
 * A floating chatbot widget that queries the RAG backend
 * to answer questions about the Physical AI & Humanoid Robotics book.
 *
 * SECURITY NOTE:
 * - This component contains NO API keys or secrets
 * - All sensitive operations happen on the backend
 * - Frontend only sends queries and receives answers
 *
 * Features:
 * - Floating toggle button
 * - Chat window with message history
 * - Text selection from page content
 * - Source citations with links
 * - Light/dark mode support (via CSS)
 * - Responsive design
 * - Error handling with friendly messages
 *
 * @author AI Frontend Developer
 * @version 2.0.0
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import styles from './Chatbot.module.css';

// =============================================================================
// CONFIGURATION
// =============================================================================

/**
 * Backend API URL - hardcoded for security (no process.env in browser)
 *
 * For production, change this to your deployed backend URL:
 * - Development: 'https://narmeenasghar-rag-chatbot.hf.space'
 * - Production: 'https://your-backend.railway.app' or similar
 *
 * IMPORTANT: Never put API keys here! The backend handles all secrets.
 */
const BACKEND_URL = 'https://narmeenasghar-rag-chatbot.hf.space';

/**
 * API endpoint for chat - uses the simplified /chat endpoint
 * Accepts: { query: string, selected_text?: string }
 * Returns: { answer: string, sources: array, confidence: number }
 */
const CHAT_ENDPOINT = `${BACKEND_URL}/chat`;

// =============================================================================
// CUSTOM HOOKS
// =============================================================================

/**
 * useTextSelection - Captures text selected by the user on the page
 *
 * This hook listens for mouse selection events and captures any text
 * the user selects from the book content (excluding the chatbot itself).
 *
 * @returns {Object} { selectedText: string, clearSelection: function }
 */
function useTextSelection() {
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    /**
     * Handler for when user finishes selecting text
     */
    const handleSelectionChange = () => {
      // Get the current selection from the browser
      const selection = window.getSelection();
      const text = selection?.toString().trim() || '';

      // Only capture if there's actual text selected
      if (text && selection.anchorNode) {
        // Make sure selection is NOT from inside the chatbot widget
        const isInChatbot = selection.anchorNode.parentElement?.closest(
          '[data-chatbot-widget]'
        );

        if (!isInChatbot) {
          setSelectedText(text);
        }
      }
    };

    /**
     * Slight delay on mouseup to ensure selection is complete
     */
    const handleMouseUp = () => {
      setTimeout(handleSelectionChange, 50);
    };

    // Add event listeners
    document.addEventListener('mouseup', handleMouseUp);

    // Cleanup on unmount
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);

  /**
   * Clear the current selection
   */
  const clearSelection = useCallback(() => {
    setSelectedText('');
    // Also clear the browser's visual selection
    if (typeof window !== 'undefined') {
      window.getSelection()?.removeAllRanges();
    }
  }, []);

  return { selectedText, clearSelection };
}

// =============================================================================
// SUB-COMPONENTS
// =============================================================================

/**
 * MessageBubble - Displays a single chat message
 *
 * @param {Object} props
 * @param {Object} props.message - Message object with content, sources, etc.
 * @param {boolean} props.isUser - Whether this is a user message
 */
function MessageBubble({ message, isUser }) {
  return (
    <div
      className={`${styles.messageBubble} ${
        isUser ? styles.userMessage : styles.botMessage
      }`}
    >
      {/* Message content */}
      <div className={styles.messageContent}>
        {message.content}
      </div>

      {/* Source citations (only for bot messages with sources) */}
      {!isUser && message.sources && message.sources.length > 0 && (
        <div className={styles.sources}>
          <span className={styles.sourcesLabel}>Sources:</span>
          {message.sources.map((source, idx) => (
            <span key={idx} className={styles.sourceTag}>
              {source.chapter} &gt; {source.section}
              {source.relevance_score && (
                <span className={styles.sourceScore}>
                  ({Math.round(source.relevance_score * 100)}%)
                </span>
              )}
            </span>
          ))}
        </div>
      )}

      {/* Confidence indicator (only for bot messages) */}
      {!isUser && typeof message.confidence === 'number' && message.confidence > 0 && (
        <div className={styles.confidence}>
          Confidence: {Math.round(message.confidence * 100)}%
        </div>
      )}
    </div>
  );
}

/**
 * SelectionContext - Shows indicator when user has selected text
 *
 * @param {Object} props
 * @param {string} props.text - The selected text
 * @param {function} props.onClear - Callback to clear selection
 */
function SelectionContext({ text, onClear }) {
  // Don't render if no text selected
  if (!text) return null;

  // Truncate long selections for display
  const displayText = text.length > 100
    ? text.substring(0, 100) + '...'
    : text;

  return (
    <div className={styles.selectionContext}>
      <div className={styles.selectionHeader}>
        <span className={styles.selectionIcon}>📝</span>
        <span>Selected text will be used as context</span>
        <button
          className={styles.clearSelection}
          onClick={onClear}
          aria-label="Clear selection"
          type="button"
        >
          ✕
        </button>
      </div>
      <div className={styles.selectionPreview}>{displayText}</div>
    </div>
  );
}

/**
 * TypingIndicator - Animated dots showing bot is "thinking"
 */
function TypingIndicator() {
  return (
    <div className={styles.typingIndicator}>
      <span></span>
      <span></span>
      <span></span>
    </div>
  );
}

/**
 * ChatInput - Input form for user messages
 *
 * @param {Object} props
 * @param {function} props.onSubmit - Callback when user submits message
 * @param {boolean} props.isLoading - Whether a request is in progress
 * @param {string} props.placeholder - Placeholder text for input
 */
function ChatInput({ onSubmit, isLoading, placeholder }) {
  const [input, setInput] = useState('');
  const inputRef = useRef(null);

  /**
   * Handle form submission
   */
  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmedInput = input.trim();

    if (trimmedInput && !isLoading) {
      onSubmit(trimmedInput);
      setInput(''); // Clear input after sending
    }
  };

  /**
   * Handle Enter key to submit (Shift+Enter for newline)
   */
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Auto-focus input when loading completes
  useEffect(() => {
    if (!isLoading && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isLoading]);

  return (
    <form className={styles.inputForm} onSubmit={handleSubmit}>
      <input
        ref={inputRef}
        type="text"
        className={styles.input}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder || 'Ask about the book...'}
        disabled={isLoading}
        aria-label="Type your question"
        autoComplete="off"
      />
      <button
        type="submit"
        className={styles.sendButton}
        disabled={!input.trim() || isLoading}
        aria-label="Send message"
      >
        {isLoading ? '...' : '→'}
      </button>
    </form>
  );
}

// =============================================================================
// MAIN CHATBOT COMPONENT
// =============================================================================

/**
 * Chatbot - Main chatbot widget component
 *
 * This component provides a floating chat interface that:
 * 1. Allows users to ask questions about the book
 * 2. Captures selected text from the page as context
 * 3. Sends queries to the backend API (NO secrets in frontend!)
 * 4. Displays answers with source citations
 *
 * @example
 * // In your Docusaurus theme/Root.js:
 * import Chatbot from '@site/src/components/Chatbot';
 *
 * export default function Root({ children }) {
 *   return (
 *     <>
 *       {children}
 *       <Chatbot />
 *     </>
 *   );
 * }
 */
export default function Chatbot() {
  // ==========================================================================
  // STATE
  // ==========================================================================

  // Whether the chat window is open
  const [isOpen, setIsOpen] = useState(false);

  // Array of chat messages
  const [messages, setMessages] = useState([]);

  // Loading state for API requests
  const [isLoading, setIsLoading] = useState(false);

  // Error message to display
  const [error, setError] = useState(null);

  // ==========================================================================
  // REFS
  // ==========================================================================

  // Reference to scroll to bottom of messages
  const messagesEndRef = useRef(null);

  // ==========================================================================
  // HOOKS
  // ==========================================================================

  // Text selection hook
  const { selectedText, clearSelection } = useTextSelection();

  // ==========================================================================
  // EFFECTS
  // ==========================================================================

  /**
   * Auto-scroll to bottom when new messages arrive
   */
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  /**
   * Add welcome message when chat opens for the first time
   */
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      setMessages([
        {
          id: 'welcome',
          role: 'assistant',
          content:
            "👋 Hi! I'm here to help you understand the Physical AI & Humanoid Robotics book.\n\n" +
            "Ask me anything about ROS2, digital twins, kinematics, or any topic in the book!\n\n" +
            '💡 Tip: Select text on the page and ask "explain this" for context-aware answers.',
          sources: [],
          confidence: 1.0,
          timestamp: new Date().toISOString(),
        },
      ]);
    }
  }, [isOpen, messages.length]);

  // ==========================================================================
  // HANDLERS
  // ==========================================================================

  /**
   * Send a message to the backend API
   *
   * SECURITY: This function only sends the query and optional selected text.
   * NO API keys or secrets are sent from the frontend.
   * All authentication/authorization happens on the backend.
   *
   * @param {string} query - The user's question
   */
  const sendMessage = useCallback(
    async (query) => {
      // Set loading state
      setIsLoading(true);
      setError(null);

      // Add user message to chat immediately (optimistic update)
      const userMessage = {
        id: `user-${Date.now()}`,
        role: 'user',
        content: query,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, userMessage]);

      // Store selected text before clearing
      const contextText = selectedText;

      // Clear selection after capturing it
      if (selectedText) {
        clearSelection();
      }

      try {
        // =================================================================
        // BACKEND API CALL
        // =================================================================
        // Send POST request to backend /chat endpoint
        // The backend handles all sensitive operations (Qdrant, embeddings, etc.)
        // =================================================================

        const response = await fetch(CHAT_ENDPOINT, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            // NO Authorization header - backend doesn't require it for chat
            // All API keys are stored securely on the backend
          },
          body: JSON.stringify({
            query: query,
            selected_text: contextText || undefined,
            // Note: We could add current_page here for analytics
            // current_page: typeof window !== 'undefined' ? window.location.pathname : undefined,
          }),
        });

        // Check for HTTP errors
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Server error (${response.status}): ${errorText}`);
        }

        // Parse response
        const data = await response.json();

        // Add bot response to chat
        const botMessage = {
          id: `bot-${Date.now()}`,
          role: 'assistant',
          content: data.answer || 'I received your question but got an empty response.',
          sources: data.sources || [],
          confidence: data.confidence || 0,
          intent: data.intent,
          timestamp: new Date().toISOString(),
        };

        setMessages((prev) => [...prev, botMessage]);

      } catch (err) {
        // Log error for debugging (visible in browser console)
        console.error('Chatbot API error:', err);

        // Set user-friendly error message
        setError('Failed to get a response. Is the backend running?');

        // Add error message to chat
        const errorMessage = {
          id: `error-${Date.now()}`,
          role: 'assistant',
          content:
            '⚠️ Sorry, I couldn\'t connect to the server.\n\n' +
            'Please make sure:\n' +
            '1. The backend is running (python main.py)\n' +
            '2. It\'s accessible at ' + BACKEND_URL + '\n\n' +
            'Error: ' + err.message,
          sources: [],
          confidence: 0,
          isError: true,
          timestamp: new Date().toISOString(),
        };

        setMessages((prev) => [...prev, errorMessage]);

      } finally {
        // Always clear loading state
        setIsLoading(false);
      }
    },
    [selectedText, clearSelection]
  );

  /**
   * Clear all chat messages and start fresh
   */
  const clearChat = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  /**
   * Toggle the chat window open/closed
   */
  const toggleChat = useCallback(() => {
    setIsOpen((prev) => !prev);
  }, []);

  // ==========================================================================
  // RENDER
  // ==========================================================================

  return (
    <div className={styles.chatbotWidget} data-chatbot-widget>
      {/* ================================================================== */}
      {/* CHAT WINDOW (shown when isOpen is true) */}
      {/* ================================================================== */}
      {isOpen && (
        <div className={styles.chatWindow}>
          {/* ------------------------------------------------------------ */}
          {/* Header */}
          {/* ------------------------------------------------------------ */}
          <div className={styles.header}>
            <div className={styles.headerTitle}>
              <span className={styles.headerIcon}>🤖</span>
              <span>Book Assistant</span>
            </div>
            <div className={styles.headerActions}>
              {/* Clear chat button */}
              <button
                className={styles.headerButton}
                onClick={clearChat}
                title="Clear chat"
                aria-label="Clear chat history"
                type="button"
              >
                🗑️
              </button>
              {/* Close button */}
              <button
                className={styles.headerButton}
                onClick={toggleChat}
                title="Close chat"
                aria-label="Close chat window"
                type="button"
              >
                ✕
              </button>
            </div>
          </div>

          {/* ------------------------------------------------------------ */}
          {/* Messages Area */}
          {/* ------------------------------------------------------------ */}
          <div className={styles.messagesArea}>
            {/* Render all messages */}
            {messages.map((msg) => (
              <MessageBubble
                key={msg.id}
                message={msg}
                isUser={msg.role === 'user'}
              />
            ))}

            {/* Show typing indicator while loading */}
            {isLoading && (
              <div className={`${styles.messageBubble} ${styles.botMessage}`}>
                <TypingIndicator />
              </div>
            )}

            {/* Invisible element to scroll to */}
            <div ref={messagesEndRef} />
          </div>

          {/* ------------------------------------------------------------ */}
          {/* Selection Context (shown when text is selected) */}
          {/* ------------------------------------------------------------ */}
          <SelectionContext
            text={selectedText}
            onClear={clearSelection}
          />

          {/* ------------------------------------------------------------ */}
          {/* Error Banner (shown when there's an error) */}
          {/* ------------------------------------------------------------ */}
          {error && (
            <div className={styles.errorBanner}>
              {error}
            </div>
          )}

          {/* ------------------------------------------------------------ */}
          {/* Input Area */}
          {/* ------------------------------------------------------------ */}
          <div className={styles.inputArea}>
            <ChatInput
              onSubmit={sendMessage}
              isLoading={isLoading}
              placeholder={
                selectedText
                  ? 'Ask about the selected text...'
                  : 'Ask about the book...'
              }
            />
          </div>
        </div>
      )}

      {/* ================================================================== */}
      {/* TOGGLE BUTTON (always visible) */}
      {/* ================================================================== */}
      <button
        className={`${styles.toggleButton} ${isOpen ? styles.toggleOpen : ''}`}
        onClick={toggleChat}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
        aria-expanded={isOpen}
        type="button"
      >
        {isOpen ? '✕' : '💬'}
      </button>
    </div>
  );
}
