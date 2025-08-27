<template>
  <BaseLayout>
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold">Kommo Integration</h1>
          <p class="text-gray-600 mt-1">Connect your AI chatbot to Kommo CRM</p>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full" :class="status?.active ? 'bg-green-500' : 'bg-orange-500'"/>
          <span class="text-sm" :class="status?.active ? 'text-green-600' : 'text-orange-600'">
            {{ status?.active ? 'Connected' : 'Not Connected' }}
          </span>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left: Configure -->
      <BaseCard class="lg:col-span-2">
        <div class="space-y-6">
          <div>
            <h3 class="font-semibold text-lg">Configure</h3>
            <p class="text-sm text-gray-600">Paste your Kommo long-lived token (or access token) and your account subdomain.</p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="text-sm font-medium">Kommo Subdomain</label>
              <input v-model="form.subdomain" placeholder="theaiexpert735.kommo.com" class="input"/>
            </div>
            <div>
              <label class="text-sm font-medium">Access Token (api_key)</label>
              <input v-model="form.api_key" placeholder="eyJ0eXAiOiJKV1Qi..." class="input"/>
            </div>
          </div>
          <div class="flex gap-3">
            <button class="btn btn-primary" @click="save" :disabled="saving">
              {{ saving ? 'Saving…' : 'Save & Connect' }}
            </button>
            <button class="btn" @click="probe" :disabled="probing">Test Connection</button>
          </div>
          <p v-if="saveMsg" class="text-sm mt-2" :class="saveOk ? 'text-green-600' : 'text-red-600'">{{ saveMsg }}</p>
        </div>
      </BaseCard>

      <!-- Right: Integration Key & Webhook URL -->
      <BaseCard>
        <div class="space-y-4">
          <div>
            <h3 class="font-semibold text-lg">Integration Key</h3>
            <p class="text-sm text-gray-600">Used in your Salesbot widget webhook URL.</p>
          </div>
          <div class="bg-gray-50 p-3 rounded">
            <div class="text-xs text-gray-500 mb-1">Key</div>
            <div class="flex items-center gap-2">
              <code class="text-sm break-all">{{ status?.integration_key || '—' }}</code>
              <button class="btn btn-xs" @click="copy(status?.integration_key)">Copy</button>
            </div>
          </div>

          <div class="bg-gray-50 p-3 rounded">
            <div class="text-xs text-gray-500 mb-1">Webhook URL</div>
            <div class="flex items-center gap-2">
              <code class="text-sm break-all">{{ status?.webhook_url || '—' }}</code>
              <button class="btn btn-xs" @click="copy(status?.webhook_url)">Copy</button>
            </div>
          </div>

          <button class="btn btn-outline w-full" @click="rotateKey">Rotate Key</button>
        </div>
      </BaseCard>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { IntegrationStatus, kommoService } from '../services/kommo'

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
  status.value = await kommoService.getStatus()
}

async function save() {
  try {
    saving.value = true
    saveMsg.value = ''
    const res = await kommoService.configure({ subdomain: form.subdomain, api_key: form.api_key })
    saveOk.value = true
    saveMsg.value = 'Saved!'
    await load()
  } catch (e: any) {
    saveOk.value = false
    saveMsg.value = e?.response?.data?.detail || e?.message || 'Failed to save'
  } finally {
    saving.value = false
  }
}

async function probe() {
  try {
    probing.value = true
    await kommoService.testConnection()
    saveOk.value = true
    saveMsg.value = 'Connection OK'
  } catch (e: any) {
    saveOk.value = false
    saveMsg.value = 'Connection failed'
  } finally {
    probing.value = false
  }
}

function copy(v?: string) {
  if (!v) return
  navigator.clipboard.writeText(v)
}

async function rotateKey() {
  const res = await kommoService.rotateIntegrationKey()
  status.value = { ...(status.value || {}), ...res, active: status.value?.active || false }
}

onMounted(load)
</script>

<style scoped>
.input { @apply w-full border rounded px-3 py-2; }
.btn { @apply border rounded px-3 py-2 text-sm; }
.btn-primary { @apply bg-blue-600 text-white hover:bg-blue-700; }
.btn-outline { @apply border-gray-300 hover:bg-gray-50; }
.btn-xs { @apply px-2 py-1; }
</style>
