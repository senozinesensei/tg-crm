import { create } from 'zustand'

interface SettingsState {
  botTokenSet: boolean
  botTokenMasked: string | null
  webhookUrl: string | null
  webhookActive: boolean
  setSettings: (data: Partial<SettingsState>) => void
}

export const useSettingsStore = create<SettingsState>((set) => ({
  botTokenSet: false,
  botTokenMasked: null,
  webhookUrl: null,
  webhookActive: false,
  setSettings: (data) => set(data),
}))
