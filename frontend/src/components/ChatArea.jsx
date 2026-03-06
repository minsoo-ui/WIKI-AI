import { useState, useRef, useEffect } from 'react'
import { Sun, Moon, Send, Menu, Bot, User } from 'lucide-react'
import { chatService } from '../services/api'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

/**
 * ChatArea – Khu vực chat chính.
 * 
 * Bố cục:
 * - Header: Tên app + Theme Toggle (góc trên bên phải)
 * - Messages: Luồng tin nhắn cuộn
 * - Input: Khung nhập liệu cố định dưới cùng
 */
function ChatArea({ darkMode, onToggleDarkMode, sidebarOpen, onOpenSidebar }) {
    const [message, setMessage] = useState('')
    const [messages, setMessages] = useState([
        {
            id: 1,
            role: 'assistant',
            content: 'Xin chào! Tôi là **WIKI-AI**, trợ lý thông minh chạy hoàn toàn trên máy của bạn. 🧠\n\nTôi có thể giúp bạn tra cứu, tóm tắt và quản lý kho kiến thức WIKI cá nhân. Hãy hỏi tôi bất cứ điều gì!',
        },
    ])
    const [isLoading, setIsLoading] = useState(false)
    const [sessionId] = useState(`session-${Date.now()}`) // Basic session ID
    const scrollRef = useRef(null)

    // Tự động cuộn xuống cuối khi có tin nhắn mới
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight
        }
    }, [messages])

    const handleSend = async () => {
        if (!message.trim() || isLoading) return

        const userMsg = { id: Date.now(), role: 'user', content: message }
        setMessages((prev) => [...prev, userMsg])
        setMessage('')
        setIsLoading(true)

        try {
            const response = await chatService.sendMessage(userMsg.content, sessionId, 'user-001')

            setMessages((prev) => [
                ...prev,
                {
                    id: Date.now() + 1,
                    role: 'assistant',
                    content: response.reply,
                    meta: {
                        agentUsed: response.agent_used,
                        traceId: response.trace_id
                    }
                },
            ])
        } catch (error) {
            setMessages((prev) => [
                ...prev,
                {
                    id: Date.now() + 1,
                    role: 'assistant',
                    content: '❌ Lỗi kết nối đến máy chủ WIKI-AI. Hãy thử lại sau!',
                    isError: true
                },
            ])
        } finally {
            setIsLoading(false)
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    return (
        <div className="flex-1 flex flex-col h-screen">
            {/* === HEADER === */}
            <header
                className="flex items-center justify-between px-4 py-3 border-b shrink-0"
                style={{
                    backgroundColor: 'var(--color-surface)',
                    borderColor: 'var(--color-border)',
                }}
            >
                <div className="flex items-center gap-3">
                    {!sidebarOpen && (
                        <button
                            onClick={onOpenSidebar}
                            className="p-1.5 rounded-md transition-colors"
                            style={{ color: 'var(--color-text-muted)' }}
                            title="Mở sidebar"
                        >
                            <Menu size={20} />
                        </button>
                    )}
                    <div className="flex items-center gap-2">
                        <Bot size={20} style={{ color: 'var(--color-primary)' }} />
                        <h1
                            className="text-base font-semibold"
                            style={{ color: 'var(--color-text)' }}
                        >
                            WIKI-AI
                        </h1>
                    </div>
                </div>

                {/* Theme Toggle – Góc trên cùng bên phải */}
                <button
                    onClick={onToggleDarkMode}
                    className="p-2 rounded-lg transition-all"
                    style={{
                        backgroundColor: 'var(--color-bg)',
                        border: '1px solid var(--color-border)',
                        color: 'var(--color-text-muted)',
                    }}
                    title={darkMode ? 'Chuyển sang Light Mode' : 'Chuyển sang Dark Mode'}
                >
                    {darkMode ? <Sun size={18} /> : <Moon size={18} />}
                </button>
            </header>

            {/* === MESSAGES === */}
            <main
                ref={scrollRef}
                className="flex-1 overflow-y-auto"
                style={{ backgroundColor: 'var(--color-bg)' }}
            >
                <div
                    className="mx-auto px-4 py-8 max-w-4xl"
                >
                    {messages.map((msg) => (
                        <div
                            key={msg.id}
                            className={`mb-8 flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
                        >
                            {/* Avatar */}
                            <div className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${msg.role === 'user' ? 'bg-blue-600' : 'bg-green-600'}`}>
                                {msg.role === 'user' ? <User size={16} color="#FFF" /> : <Bot size={16} color="#FFF" />}
                            </div>

                            {/* Message Content */}
                            <div
                                className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'} max-w-[80%]`}
                            >
                                <div
                                    className={`px-5 py-3.5 rounded-2xl text-[15px] leading-relaxed shadow-sm prose dark:prose-invert prose-p:leading-relaxed prose-pre:bg-slate-800 prose-pre:text-slate-100 ${msg.role === 'user' ? 'bg-blue-600 text-white rounded-tr-sm' : 'bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 rounded-tl-sm border border-slate-200 dark:border-slate-700'
                                        }`}
                                    style={msg.isError ? { borderColor: 'red', color: 'red' } : {}}
                                >
                                    {msg.role === 'user' ? (
                                        <p className="m-0 whitespace-pre-wrap">{msg.content}</p>
                                    ) : (
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                            {msg.content}
                                        </ReactMarkdown>
                                    )}
                                </div>
                                {msg.meta && msg.meta.agentUsed && (
                                    <div className="flex gap-2 mt-2 text-[11px] text-slate-400 font-mono items-center">
                                        <span className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800/50 uppercase tracking-wider">
                                            {msg.meta.agentUsed}
                                        </span>
                                        {msg.meta.traceId && (
                                            <span className="opacity-60 cursor-help" title={`Trace ID: ${msg.meta.traceId}`}>
                                                • trace: {msg.meta.traceId.slice(0, 8)}
                                            </span>
                                        )}
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                    {isLoading && (
                        <div className="mb-8 flex gap-4 flex-row">
                            <div className="shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-green-600">
                                <Bot size={16} color="#FFF" />
                            </div>
                            <div className="px-5 py-3.5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-tl-sm flex items-center gap-2">
                                <div className="w-1.5 h-1.5 rounded-full bg-slate-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                                <div className="w-1.5 h-1.5 rounded-full bg-slate-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                                <div className="w-1.5 h-1.5 rounded-full bg-slate-400 animate-bounce" style={{ animationDelay: '300ms' }} />
                            </div>
                        </div>
                    )}
                </div>
            </main>

            {/* === INPUT BOX === */}
            <div
                className="shrink-0 border-t px-4 py-3"
                style={{
                    backgroundColor: 'var(--color-surface)',
                    borderColor: 'var(--color-border)',
                }}
            >
                <div
                    className="mx-auto flex items-end gap-2"
                    style={{ maxWidth: 'var(--chat-max-width)' }}
                >
                    <textarea
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyDown={handleKeyDown}
                        rows={1}
                        placeholder="Hỏi WIKI-AI bất kỳ điều gì..."
                        className="flex-1 resize-none rounded-xl px-4 py-3 text-sm outline-none transition-colors"
                        style={{
                            backgroundColor: 'var(--color-bg)',
                            color: 'var(--color-text)',
                            border: '1px solid var(--color-border)',
                        }}
                    />
                    <button
                        onClick={handleSend}
                        disabled={!message.trim()}
                        className="p-3 rounded-xl text-white transition-all disabled:opacity-40"
                        style={{
                            backgroundColor: 'var(--color-primary)',
                        }}
                        title="Gửi tin nhắn"
                    >
                        <Send size={18} />
                    </button>
                </div>
            </div>
        </div>
    )
}

export default ChatArea
