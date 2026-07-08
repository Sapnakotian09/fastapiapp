export type ChatMessage = {
  role: "user" | "bot";
  text: string;
};

export type ChatRequest = {
  message: string;
  session_id?: string;
};

export type ChatResponse = {
  response: string;
};