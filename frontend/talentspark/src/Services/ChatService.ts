import api from "./api";

type ChatResponsePayload = {
    response: string;
};

export async function askChat(message: string): Promise<string> {
    const response = await api.post<ChatResponsePayload>("/chat/ask", { message });
    return response.data.response;
}

export async function askCareerChat(message: string, session_id: string): Promise<string> {
    const response = await api.post<ChatResponsePayload>("/chat/ask career", { message, session_id });
    return response.data.response;
}

export async function sendChatMessage(payload: { message: string; session_id: string }): Promise<{ reply: string }> {
    const response = await api.post<ChatResponsePayload>("/chat/ask career", payload);
    return { reply: response.data.response };
}