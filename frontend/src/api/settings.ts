import client from './client'

export async function getSettings() {
  const res = await client.get('/settings')
  return res.data
}

export async function updateBotToken(bot_token: string) {
  const res = await client.put('/settings/bot-token', { bot_token })
  return res.data
}

export async function updateOpenRouterSettings(data: {
  openrouter_api_key?: string
  openrouter_model: string
  openrouter_system_prompt: string
  openrouter_history_limit: number
  ai_auto_reply_enabled: boolean
}) {
  const res = await client.put('/settings/openrouter', data)
  return res.data
}

export async function registerWebhook(webhook_url: string) {
  const res = await client.post('/settings/webhook/register', { webhook_url })
  return res.data
}

export async function deleteWebhook() {
  const res = await client.delete('/settings/webhook')
  return res.data
}

export async function getWebhookStatus() {
  const res = await client.get('/settings/webhook/status')
  return res.data
}
