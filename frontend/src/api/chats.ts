import client from './client'

export async function getChats() {
  const res = await client.get('/chats')
  return res.data
}

export async function getChat(chatId: string) {
  const res = await client.get(`/chats/${chatId}`)
  return res.data
}

export async function getChatMessages(chatId: string, limit = 50, offset = 0) {
  const res = await client.get(`/chats/${chatId}/messages`, { params: { limit, offset } })
  return res.data
}

export async function sendMessage(chatId: string, text: string) {
  const res = await client.post(`/chats/${chatId}/messages`, { text })
  return res.data
}

export async function markChatRead(chatId: string) {
  const res = await client.patch(`/chats/${chatId}/read`)
  return res.data
}
