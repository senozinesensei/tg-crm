import { useEffect, useState } from 'react'
import { getSettings, updateBotToken, registerWebhook, deleteWebhook, getWebhookStatus } from '../api/settings'

export default function SettingsPage() {
  const [botToken, setBotToken] = useState('')
  const [webhookUrl, setWebhookUrl] = useState('')
  const [webhookActive, setWebhookActive] = useState(false)
  const [botTokenMasked, setBotTokenMasked] = useState<string | null>(null)
  const [botTokenSet, setBotTokenSet] = useState(false)
  const [webhookInfo, setWebhookInfo] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)

  useEffect(() => {
    loadSettings()
  }, [])

  const loadSettings = async () => {
    setLoading(true)
    try {
      const data = await getSettings()
      setBotTokenSet(data.bot_token_set)
      setBotTokenMasked(data.bot_token_masked)
      setWebhookUrl(data.webhook_url || '')
      setWebhookActive(data.webhook_active)

      if (data.bot_token_set) {
        const status = await getWebhookStatus()
        setWebhookInfo(status.info)
        setWebhookActive(status.active)
      }
    } finally {
      setLoading(false)
    }
  }

  const showMessage = (type: 'success' | 'error', text: string) => {
    setMessage({ type, text })
    setTimeout(() => setMessage(null), 4000)
  }

  const handleSaveToken = async () => {
    if (!botToken.trim()) return
    setSaving(true)
    try {
      await updateBotToken(botToken.trim())
      setBotTokenSet(true)
      setBotTokenMasked(botToken.slice(0, 8) + '...' + botToken.slice(-4))
      setBotToken('')
      showMessage('success', 'Bot token saved successfully')
    } catch (err: any) {
      showMessage('error', err.response?.data?.detail || 'Failed to save token')
    } finally {
      setSaving(false)
    }
  }

  const handleRegisterWebhook = async () => {
    if (!webhookUrl.trim()) return
    setSaving(true)
    try {
      await registerWebhook(webhookUrl.trim())
      setWebhookActive(true)
      showMessage('success', 'Webhook registered successfully')
      const status = await getWebhookStatus()
      setWebhookInfo(status.info)
    } catch (err: any) {
      showMessage('error', err.response?.data?.detail || 'Failed to register webhook')
    } finally {
      setSaving(false)
    }
  }

  const handleDeleteWebhook = async () => {
    setSaving(true)
    try {
      await deleteWebhook()
      setWebhookActive(false)
      setWebhookInfo(null)
      showMessage('success', 'Webhook deleted successfully')
    } catch (err: any) {
      showMessage('error', err.response?.data?.detail || 'Failed to delete webhook')
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="h-full overflow-y-auto bg-white dark:bg-gray-800">
      <div className="max-w-2xl mx-auto p-6 space-y-8">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Settings</h2>

        {message && (
          <div
            className={`p-3 rounded-lg text-sm ${
              message.type === 'success'
                ? 'bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400'
                : 'bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400'
            }`}
          >
            {message.text}
          </div>
        )}

        {/* Bot Token Section */}
        <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
            Telegram Bot Token
          </h3>

          {botTokenSet && (
            <div className="mb-4 flex items-center gap-2">
              <span className="text-sm text-gray-500 dark:text-gray-400">Current token:</span>
              <code className="text-sm bg-gray-200 dark:bg-gray-600 px-2 py-1 rounded">
                {botTokenMasked}
              </code>
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400">
                Active
              </span>
            </div>
          )}

          <div className="flex gap-3">
            <input
              type="password"
              value={botToken}
              onChange={(e) => setBotToken(e.target.value)}
              placeholder="Enter new bot token..."
              className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500 text-sm"
            />
            <button
              onClick={handleSaveToken}
              disabled={!botToken.trim() || saving}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg text-sm font-medium transition-colors"
            >
              Save
            </button>
          </div>
        </div>

        {/* Webhook Section */}
        <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">
              Webhook
            </h3>
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                webhookActive
                  ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400'
                  : 'bg-gray-100 dark:bg-gray-600 text-gray-800 dark:text-gray-300'
              }`}
            >
              {webhookActive ? 'Active' : 'Inactive'}
            </span>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Webhook URL (ngrok or public URL)
              </label>
              <input
                type="url"
                value={webhookUrl}
                onChange={(e) => setWebhookUrl(e.target.value)}
                placeholder="https://your-ngrok-url.ngrok-free.app"
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500 text-sm"
              />
              <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                The system will append /webhook/telegram to this URL automatically
              </p>
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleRegisterWebhook}
                disabled={!webhookUrl.trim() || !botTokenSet || saving}
                className="px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white rounded-lg text-sm font-medium transition-colors"
              >
                Register Webhook
              </button>
              <button
                onClick={handleDeleteWebhook}
                disabled={!webhookActive || saving}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white rounded-lg text-sm font-medium transition-colors"
              >
                Delete Webhook
              </button>
            </div>
          </div>

          {webhookInfo && (
            <div className="mt-4 p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-600">
              <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-2">Webhook Info</h4>
              <dl className="space-y-1 text-sm">
                <div className="flex gap-2">
                  <dt className="text-gray-500 dark:text-gray-400">URL:</dt>
                  <dd className="text-gray-900 dark:text-white break-all">{webhookInfo.url || 'Not set'}</dd>
                </div>
                {webhookInfo.pending_update_count !== undefined && (
                  <div className="flex gap-2">
                    <dt className="text-gray-500 dark:text-gray-400">Pending updates:</dt>
                    <dd className="text-gray-900 dark:text-white">{webhookInfo.pending_update_count}</dd>
                  </div>
                )}
                {webhookInfo.last_error_message && (
                  <div className="flex gap-2">
                    <dt className="text-gray-500 dark:text-gray-400">Last error:</dt>
                    <dd className="text-red-600 dark:text-red-400">{webhookInfo.last_error_message}</dd>
                  </div>
                )}
              </dl>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
