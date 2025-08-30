<template>
  <BaseLayout>
    <!-- Enhanced Header with Status Badge -->
    <div class="mb-8">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 class="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-primary-600 to-blue-600 bg-clip-text text-transparent">
            Kommo Integration
          </h1>
          <p class="text-gray-600 dark:text-gray-400 mt-2 text-lg">Connect your AI chatbot to Kommo CRM for seamless workflow automation</p>
        </div>
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-2 px-4 py-2 rounded-full border" 
               :class="status?.active ? 'bg-emerald-50 border-emerald-200' : 'bg-amber-50 border-amber-200'">
            <div class="w-2 h-2 rounded-full" 
                 :class="status?.active ? 'bg-emerald-500' : 'bg-amber-500'"></div>
            <span class="text-sm font-medium" 
                  :class="status?.active ? 'text-emerald-700' : 'text-amber-700'">
              {{ status?.active ? 'Connected' : 'Not Connected' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left: Configuration Panel -->
      <div class="lg:col-span-2">
        <BaseCard class="overflow-hidden">
          <div class="p-6 border-b border-gray-100 dark:border-gray-700">
            <div class="flex items-start gap-4">
              <div class="flex items-center justify-center w-12 h-12 bg-blue-50 rounded-xl border border-blue-100">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Configuration</h3>
                <p class="text-gray-600 dark:text-gray-400 mt-1">Enter your Kommo credentials to establish the connection</p>
              </div>
            </div>
          </div>
          
          <div class="p-6 space-y-6">
            <!-- Form Fields -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Kommo Subdomain
                </label>
                <div class="relative">
                  <BaseInput
                    v-model="form.subdomain"
                    placeholder="theaiexpert735.kommo.com"
                    class="pl-10"
                  />
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
                    </svg>
                  </div>
                </div>
                <p class="text-xs text-gray-500 dark:text-gray-400">Your Kommo account subdomain</p>
              </div>
              
              <div class="space-y-2">
                <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Access Token (API Key)
                </label>
                <div class="relative">
                  <BaseInput
                    v-model="form.api_key"
                    type="password"
                    placeholder="eyJ0eXAiOiJKV1Qi..."
                    class="pl-10"
                  />
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                    </svg>
                  </div>
                </div>
                <p class="text-xs text-gray-500 dark:text-gray-400">Long-lived token from Kommo</p>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex flex-col sm:flex-row gap-3 pt-4">
              <BaseButton
                variant="primary"
                :loading="saving"
                :disabled="!form.subdomain || !form.api_key"
                @click="save"
                class="flex-1 sm:flex-none"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                {{ saving ? 'Connecting...' : 'Save & Connect' }}
              </BaseButton>
              
              <BaseButton
                variant="secondary"
                :loading="probing"
                :disabled="!form.subdomain || !form.api_key"
                @click="probe"
                class="flex-1 sm:flex-none"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Test Connection
              </BaseButton>
            </div>

            <!-- Status Message -->
            <div v-if="saveMsg" class="mt-4">
              <div class="flex items-center gap-3 p-4 rounded-lg border" 
                   :class="saveOk ? 'bg-emerald-50 border-emerald-200 text-emerald-800' : 'bg-red-50 border-red-200 text-red-800'">
                <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path v-if="saveOk" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="font-medium">{{ saveMsg }}</span>
              </div>
            </div>
          </div>
        </BaseCard>
      </div>

      <!-- Right: Integration Details -->
      <div class="space-y-6">
        <!-- Integration Key Card -->
        <BaseCard>
          <div class="p-6">
            <div class="flex items-start gap-4 mb-6">
              <div class="flex items-center justify-center w-10 h-10 bg-purple-50 rounded-lg border border-purple-100">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900">Integration Key</h3>
                <p class="text-sm text-gray-600 mt-1">Used in your Salesbot widget webhook URL</p>
              </div>
            </div>
            
            <div class="space-y-4">
              <!-- Integration Key -->
              <div class="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                <div class="flex items-center justify-between mb-2">
                  <label class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">Key</label>
                  <BaseButton
                    variant="secondary"
                    size="sm"
                    @click="copy(status?.integration_key)"
                    :disabled="!status?.integration_key"
                  >
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    Copy
                  </BaseButton>
                </div>
                <code class="block text-sm text-gray-900 bg-white p-3 rounded border break-all font-mono">
                  {{ status?.integration_key || 'Not generated yet' }}
                </code>
              </div>

              <!-- Webhook URL -->
              <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <div class="flex items-center justify-between mb-2">
                  <label class="text-xs font-medium text-gray-500 uppercase tracking-wide">Webhook URL</label>
                  <BaseButton
                    variant="secondary"
                    size="sm"
                    @click="copy(status?.webhook_url)"
                    :disabled="!status?.webhook_url"
                  >
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    Copy
                  </BaseButton>
                </div>
                <code class="block text-sm text-gray-900 bg-white p-3 rounded border break-all font-mono">
                  {{ status?.webhook_url || 'Not available' }}
                </code>
              </div>

              <!-- Rotate Key Button -->
              <BaseButton
                variant="secondary"
                @click="rotateKey"
                :disabled="!status?.integration_key"
                class="w-full"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Rotate Key
              </BaseButton>
            </div>
          </div>
        </BaseCard>

        <!-- Help Card -->
        <BaseCard>
          <div class="p-6">
            <div class="flex items-start gap-4 mb-4">
              <div class="flex items-center justify-center w-10 h-10 bg-blue-50 rounded-lg border border-blue-100">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900">Setup Guide</h3>
                <p class="text-sm text-gray-600 mt-1">Quick steps to get started</p>
              </div>
            </div>
            
            <div class="space-y-3 text-sm text-gray-600">
              <div class="flex items-start gap-3">
                <span class="flex items-center justify-center w-5 h-5 bg-blue-100 text-blue-600 rounded-full text-xs font-bold mt-0.5">1</span>
                <span>Get your API token from Kommo settings</span>
              </div>
              <div class="flex items-start gap-3">
                <span class="flex items-center justify-center w-5 h-5 bg-blue-100 text-blue-600 rounded-full text-xs font-bold mt-0.5">2</span>
                <span>Enter subdomain and token above</span>
              </div>
              <div class="flex items-start gap-3">
                <span class="flex items-center justify-center w-5 h-5 bg-blue-100 text-blue-600 rounded-full text-xs font-bold mt-0.5">3</span>
                <span>Copy webhook URL to your Salesbot</span>
              </div>
            </div>
          </div>
        </BaseCard>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { IntegrationStatus, kommoService } from '../services/kommo'
import { useToast } from '@/composables/useToast'
import BaseLayout from '@/components/BaseLayout.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseInput from '@/components/BaseInput.vue'

const { success: showSuccess, error: showError } = useToast()

const status = ref<IntegrationStatus | null>(null)
const saving = ref(false)
const probing = ref(false)
const saveOk = ref(false)
const saveMsg = ref('')
const form = reactive({
  subdomain: '',
  api_key: '',
})

async function load() {
  try {
    status.value = await kommoService.getStatus()
  } catch (e: any) {
    showError('Failed to load integration status', e?.message || 'Unknown error')
  }
}

async function save() {
  try {
    saving.value = true
    saveMsg.value = ''
    const res = await kommoService.configure({ subdomain: form.subdomain, api_key: form.api_key })
    saveOk.value = true
    saveMsg.value = 'Successfully connected to Kommo!'
    showSuccess('Integration Saved', 'Your Kommo integration has been configured successfully.')
    await load()
  } catch (e: any) {
    saveOk.value = false
    saveMsg.value = e?.response?.data?.detail || e?.message || 'Failed to save configuration'
    showError('Configuration Failed', saveMsg.value)
  } finally {
    saving.value = false
  }
}

async function probe() {
  try {
    probing.value = true
    await kommoService.testConnection()
    saveOk.value = true
    saveMsg.value = 'Connection test successful!'
    showSuccess('Connection Test', 'Successfully connected to Kommo API.')
  } catch (e: any) {
    saveOk.value = false
    saveMsg.value = 'Connection test failed. Please check your credentials.'
    showError('Connection Failed', e?.response?.data?.detail || e?.message || 'Unable to connect to Kommo')
  } finally {
    probing.value = false
  }
}

async function copy(v?: string) {
  if (!v) {
    showError('Copy Failed', 'No value to copy')
    return
  }
  try {
    await navigator.clipboard.writeText(v)
    showSuccess('Copied!', 'Value copied to clipboard')
  } catch (e) {
    showError('Copy Failed', 'Unable to copy to clipboard')
  }
}

async function rotateKey() {
  try {
    const res = await kommoService.rotateIntegrationKey()
    status.value = { ...(status.value || {}), ...res, active: status.value?.active || false }
    showSuccess('Key Rotated', 'Integration key has been rotated successfully.')
  } catch (e: any) {
    showError('Rotation Failed', e?.response?.data?.detail || e?.message || 'Failed to rotate key')
  }
}

onMounted(load)
</script>


