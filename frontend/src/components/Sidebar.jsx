import { LogOut, Monitor, Settings, Search, MessageSquarePlus, RefreshCw } from 'lucide-react'

function Sidebar({ isOpen, onClose }) {
    if (!isOpen) return null;

    return (
        <aside
            className="fixed inset-y-0 left-0 z-50 flex flex-col w-[var(--sidebar-width)] border-r shadow-xl md:static md:shadow-none transition-transform duration-300"
            style={{
                backgroundColor: 'var(--color-surface)',
                borderColor: 'var(--color-border)',
            }}
        >
            {/* Top: User Profile */}
            <div className="p-4 border-b" style={{ borderColor: 'var(--color-border)' }}>
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">
                        U
                    </div>
                    <div className="flex-1 overflow-hidden">
                        <h3 className="text-sm font-semibold truncate" style={{ color: 'var(--color-text)' }}>
                            User Account
                        </h3>
                        <p className="text-xs truncate" style={{ color: 'var(--color-text-muted)' }}>
                            user@example.com
                        </p>
                    </div>
                </div>
                <div className="mt-4 flex flex-col gap-2">
                    <button className="flex items-center gap-2 text-xs font-medium px-2 py-1.5 rounded-md w-full transition-colors hover:bg-gray-100 dark:hover:bg-slate-700" style={{ color: 'var(--color-text-muted)' }}>
                        <RefreshCw size={14} /> Swich Account
                    </button>
                    <button className="flex items-center gap-2 text-xs font-medium px-2 py-1.5 rounded-md w-full transition-colors hover:bg-red-50 dark:hover:bg-red-900/20 text-red-600">
                        <LogOut size={14} /> Logout
                    </button>
                </div>
            </div>

            {/* Middle: Actions & History */}
            <div className="flex-1 overflow-y-auto p-3 flex flex-col gap-1">
                <button
                    className="flex items-center gap-2 px-3 py-2.5 rounded-lg mb-2 text-sm font-medium transition-colors"
                    style={{
                        backgroundColor: 'var(--color-primary)',
                        color: '#FFF',
                    }}
                >
                    <MessageSquarePlus size={18} /> New Chat
                </button>

                <div className="mt-4 px-2">
                    <p className="text-xs font-semibold uppercase tracking-wider mb-2" style={{ color: 'var(--color-text-muted)' }}>
                        Recent Chats
                    </p>
                    {/* Placeholder for history */}
                    <div className="flex flex-col gap-1">
                        <button className="text-left text-sm px-2 py-1.5 rounded-md truncate hover:bg-gray-100 dark:hover:bg-slate-800 transition-colors" style={{ color: 'var(--color-text)' }}>
                            Tìm hiểu về RAG
                        </button>
                        <button className="text-left text-sm px-2 py-1.5 rounded-md truncate hover:bg-gray-100 dark:hover:bg-slate-800 transition-colors" style={{ color: 'var(--color-text)' }}>
                            Giá CPU Intel I3
                        </button>
                    </div>
                </div>
            </div>

            {/* Bottom: System/Settings */}
            <div className="p-3 border-t" style={{ borderColor: 'var(--color-border)' }}>
                <button className="flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-lg w-full transition-colors hover:bg-gray-100 dark:hover:bg-slate-800" style={{ color: 'var(--color-text)' }}>
                    <Search size={16} /> WIKI Knowledge Base
                </button>
                <button className="flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-lg w-full transition-colors hover:bg-gray-100 dark:hover:bg-slate-800" style={{ color: 'var(--color-text)' }}>
                    <Monitor size={16} /> System Status
                </button>
            </div>

            {/* Mobile close overlay */}
            <div className="md:hidden fixed inset-0 bg-black/50 z-[-1]" onClick={onClose} />
        </aside>
    )
}

export default Sidebar
