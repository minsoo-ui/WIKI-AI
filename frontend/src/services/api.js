import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api'; // Trỏ về server FastAPI

export const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const chatService = {
    async sendMessage(message, sessionId, userId) {
        try {
            const response = await api.post('/chat/send', {
                message,
                session_id: sessionId,
                user_id: userId
            });
            return response.data;
        } catch (error) {
            console.error('Lỗi khi gọi API Chat:', error);
            throw error;
        }
    },

    async getSystemStatus() {
        try {
            const response = await api.get('/system/status');
            return response.data;
        } catch (error) {
            console.error('Lỗi khi gọi API System Status:', error);
            throw error;
        }
    }
};
