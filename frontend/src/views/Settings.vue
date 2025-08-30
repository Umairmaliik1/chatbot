<template>
  <BaseLayout>
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Settings</h1>
          
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Settings Navigation -->
      <BaseCard class="lg:col-span-1">
        <div class="card-header">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Settings</h3>
        </div>
        <nav class="space-y-1 p-4">
          <button
            v-for="tab in settingsTabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            class="nav-item w-full text-left"
            :class="activeTab === tab.id ? 'nav-item-active' : 'nav-item-inactive'"
          >
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="tab.icon" />
            </svg>
            {{ tab.name }}
          </button>
        </nav>
      </BaseCard>

      <!-- Settings Content -->
      <BaseCard class="lg:col-span-2">
        <!-- Profile Settings -->
        <div v-if="activeTab === 'profile'" class="space-y-6">
          <div class="card-header">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Profile Information</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">Update your personal information</p>
          </div>
          
          <form @submit.prevent="updateProfile" class="space-y-6 p-6">
            <BaseInput
              v-model="profileForm.firstName"
              label="First Name"
              placeholder="Enter your first name"
              :error="profileErrors.firstName"
              required
            />

            <BaseInput
              v-model="profileForm.lastName"
              label="Last Name"
              placeholder="Enter your last name"
              :error="profileErrors.lastName"
              required
            />
            
            <div class="flex justify-end">
              <BaseButton
                type="submit"
                variant="primary"
                :loading="isUpdatingProfile"
              >
                Update Profile
              </BaseButton>
            </div>
          </form>
        </div>

        <!-- Security Settings -->
        <div v-if="activeTab === 'security'" class="space-y-6">
          <div class="card-header">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Security Settings</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">Manage your password and security preferences</p>
          </div>
          
          <form @submit.prevent="changePassword" class="space-y-6 p-6">
            <BaseInput
              v-model="passwordForm.currentPassword"
              type="password"
              label="Current Password"
              placeholder="Enter your current password"
              :error="passwordErrors.currentPassword"
              required
            />
            
            <BaseInput
              v-model="passwordForm.newPassword"
              type="password"
              label="New Password"
              placeholder="Enter your new password"
              :error="passwordErrors.newPassword"
              required
            />
            
            <BaseInput
              v-model="passwordForm.confirmPassword"
              type="password"
              label="Confirm New Password"
              placeholder="Confirm your new password"
              :error="passwordErrors.confirmPassword"
              required
            />
            
            <div class="flex justify-end">
              <BaseButton
                type="submit"
                variant="primary"
                :loading="isChangingPassword"
              >
                Change Password
              </BaseButton>
            </div>
          </form>
        </div>

        <!-- AI Settings -->
        <div v-if="activeTab === 'ai'" class="space-y-6">
          <div class="card-header">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">AI Configuration</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">Configure your AI assistant behavior and provider settings</p>
          </div>
          
          <div class="space-y-6 p-6">
            <!-- AI Provider Selection -->
            <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <h4 class="text-sm font-medium text-gray-900 dark:text-white">AI Provider</h4>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Choose your preferred AI provider</p>
                </div>
              </div>
              
              <div class="space-y-3">
                <label class="flex items-center space-x-3 cursor-pointer">
                  <input
                    v-model="aiSettings.provider"
                    type="radio"
                    value="gemini"
                    class="form-radio text-primary-600"
                  />
                  <div>
                    <span class="text-sm font-medium text-gray-900 dark:text-white">Google AI Bot</span>
                    <p class="text-xs text-gray-500 dark:text-gray-400">Fast and reliable AI responses</p>
                  </div>
                </label>
                
                <label class="flex items-center space-x-3 cursor-pointer">
                  <input
                    v-model="aiSettings.provider"
                    type="radio"
                    value="openai"
                    class="form-radio text-primary-600"
                  />
                  <div>
                    <span class="text-sm font-medium text-gray-900 dark:text-white">OpenAI GPT-3.5</span>
                    <p class="text-xs text-gray-500 dark:text-gray-400">Advanced conversational AI</p>
                  </div>
                </label>
              </div>
            </div>

            <!-- Response Time Settings -->
            <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <h4 class="text-sm font-medium text-gray-900 dark:text-white">Response Timing</h4>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Control how quickly the AI responds to messages</p>
                </div>
              </div>
              
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Response Delay: {{ aiSettings.responseDelay }}s
                  </label>
                  <div class="flex items-center space-x-4">
                    <span class="text-xs text-gray-500 dark:text-gray-400">Instant</span>
                    <input
                      v-model.number="aiSettings.responseDelay"
                      type="range"
                      min="0"
                      max="40"
                      step="5"
                      class="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
                    />
                    <span class="text-xs text-gray-500 dark:text-gray-400">40s</span>
                  </div>
                  <div class="mt-2 grid grid-cols-9 gap-1 text-xs text-gray-400">
                    <span class="text-center">0s</span>
                    <span class="text-center">5s</span>
                    <span class="text-center">10s</span>
                    <span class="text-center">15s</span>
                    <span class="text-center">20s</span>
                    <span class="text-center">25s</span>
                    <span class="text-center">30s</span>
                    <span class="text-center">35s</span>
                    <span class="text-center">40s</span>
                  </div>
                </div>
                
                <!-- Quick Selection Buttons -->
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="delay in [0, 5, 10, 15, 20, 25, 30, 35, 40]"
                    :key="delay"
                    @click="aiSettings.responseDelay = delay"
                    :class="[
                      'px-3 py-1 text-xs rounded-full border transition-colors',
                      aiSettings.responseDelay === delay
                        ? 'bg-primary-100 border-primary-500 text-primary-700'
                        : 'bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600'
                    ]"
                  >
                    {{ delay }}s
                  </button>
                </div>
                
                <div class="text-xs text-gray-500 dark:text-gray-400 bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg">
                  <strong>Note:</strong> Response delay adds a pause before the AI starts responding. 
                  This can make conversations feel more natural and give users time to read previous messages.
                </div>
              </div>
            </div>
            
            <div class="pt-4 border-t border-gray-200">
              <BaseButton
                variant="primary"
                :loading="isUpdatingAiSettings"
                @click="updateAiSettings"
              >
                Save AI Settings
              </BaseButton>
            </div>
          </div>
        </div>

        <!-- API Settings -->
        <div v-if="activeTab === 'api'" class="space-y-6">
          <div class="card-header">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">API Configuration</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">Manage your API keys and integrations</p>
          </div>
          
          <div class="space-y-6 p-6">
            <!-- Xelence Integration -->
            <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <h4 class="text-sm font-medium text-gray-900 dark:text-white">Xelence Integration</h4>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Configure your Xelence affiliate credentials for media reports</p>
                </div>
                <div class="flex items-center space-x-2">
                  <div class="w-3 h-3 rounded-full" :class="xelenceApiStatus ? 'bg-success-400' : 'bg-warning-400'"></div>
                  <span class="text-sm font-medium" :class="xelenceApiStatus ? 'text-success-600' : 'text-warning-600'">
                    {{ xelenceApiStatus ? 'Configured' : 'Not Configured' }}
                  </span>
                </div>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <BaseInput
                  v-model="xelenceForm.affiliateId"
                  label="Affiliate ID"
                  placeholder="Enter your Xelence affiliate ID"
                  :error="xelenceErrors.affiliateId"
                />
                
                <BaseInput
                  v-model="xelenceForm.apiKey"
                  type="password"
                  label="API Key"
                  placeholder="Enter your Xelence API key"
                  :error="xelenceErrors.apiKey"
                />
              </div>
              
              <div class="mt-4 flex justify-end">
                <BaseButton
                  variant="primary"
                  size="sm"
                  :loading="isUpdatingXelence"
                  @click="updateXelenceCredentials"
                >
                  Save Credentials
                </BaseButton>
              </div>
            </div>


            <!-- API Usage Stats -->
            <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
              <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-4">API Usage Statistics</h4>
              <div class="grid grid-cols-2 gap-4">
                <div class="text-center">
                  <div class="text-2xl font-bold text-primary-600">{{ apiUsage.requests }}</div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">Total Requests</div>
                </div>
                <div class="text-center">
                  <div class="text-2xl font-bold text-success-600">{{ apiUsage.tokens }}</div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">Tokens Used</div>
                </div>
              </div>
            </div>
          </div>
        </div>



        <!-- Customization -->
        <div v-if="activeTab === 'customization'" class="space-y-6">
          <div class="card-header">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Customization</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">Personalize your chatbot interface</p>
          </div>
          
          <div class="space-y-6 p-6">
            <BaseInput
              v-model="customizationForm.websiteName"
              label="Website Name"
              placeholder="Enter your website name"
              :error="customizationErrors.websiteName"
            />

            <BaseInput
              v-model="customizationForm.logoUrl"
              label="Logo URL"
              placeholder="https://example.com/logo.png"
              :error="customizationErrors.logoUrl"
            />

            <!-- Favicon Upload -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">Favicon (.ico)</label>
              <input 
                type="file" 
                accept=".ico,image/x-icon"
                @change="onFaviconSelected"
                class="block w-full text-sm text-gray-900 dark:text-gray-100 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
              />
              <p class="text-xs text-gray-500">Max 512 KB. Upload a square ICO file.</p>
              <div class="flex items-center space-x-3" v-if="currentFavicon">
                <span class="text-xs text-gray-600 dark:text-gray-300">Current:</span>
                <img :src="currentFavicon" alt="Current Favicon" class="w-6 h-6" />
              </div>
              <div class="pt-2">
                <BaseButton 
                  variant="secondary" 
                  size="sm" 
                  :loading="isUploadingFavicon"
                  :disabled="!selectedFavicon"
                  @click="uploadFavicon"
                >
                  Upload Favicon
                </BaseButton>
              </div>
            </div>

            <!-- Dark Mode Toggle -->
            <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-sm font-medium text-gray-900 dark:text-white">Dark Mode</h4>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Switch to dark theme</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input
                    v-model="darkMode"
                    type="checkbox"
                    class="sr-only peer"
                    @change="toggleDarkMode"
                  />
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
            </div>
            
            <div class="pt-4 border-t border-gray-200">
              <BaseButton
                variant="primary"
                :loading="isUpdatingCustomization"
                @click="updateCustomization"
              >
                Save Customization
              </BaseButton>
            </div>
          </div>
        </div>
      </BaseCard>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import BaseLayout from '@/components/BaseLayout.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseInput from '@/components/BaseInput.vue'
import { apiService } from '@/services/api'
// Using simple SVG icons instead of Heroicons
const UserIcon = 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z'
const ShieldCheckIcon = 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z'

const KeyIcon = 'M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z'

const authStore = useAuthStore()
const { success: showSuccess, error: showError } = useToast()

const activeTab = ref('profile')

const BotIcon = 'M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z'
const PaintBrushIcon = 'M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z'

const settingsTabs = [
  { id: 'profile', name: 'Profile', icon: UserIcon },
  { id: 'security', name: 'Security', icon: ShieldCheckIcon },
  { id: 'ai', name: 'AI Settings', icon: BotIcon },
  { id: 'api', name: 'API Settings', icon: KeyIcon },
  { id: 'customization', name: 'Customization', icon: PaintBrushIcon }
]

// Profile form
const profileForm = ref({
  firstName: '',
  lastName: ''
})

const profileErrors = ref({
  firstName: '',
  lastName: ''
})

const isUpdatingProfile = ref(false)

// Password form
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordErrors = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const isChangingPassword = ref(false)

// AI settings form
const aiSettings = ref({
  provider: 'gemini',
  responseDelay: 0
})

const isUpdatingAiSettings = ref(false)

// Xelence form
const xelenceForm = ref({
  affiliateId: '',
  apiKey: ''
})

const xelenceErrors = ref({
  affiliateId: '',
  apiKey: ''
})

const xelenceApiStatus = ref(false)
const isUpdatingXelence = ref(false)

const apiUsage = ref({
  requests: 0,
  tokens: 0
})

// Preferences
// Dark mode functionality
const darkMode = ref(false)

// Customization form
const customizationForm = ref({
  websiteName: '',
  logoUrl: '',
  faviconUrl: ''
})

const customizationErrors = ref({
  websiteName: '',
  logoUrl: '',
  faviconUrl: ''
})

const isUpdatingCustomization = ref(false)
const isUploadingFavicon = ref(false)

// Favicon upload state
const selectedFavicon = ref<File | null>(null)
const currentFavicon = ref<string>('')

const onFaviconSelected = (e: Event) => {
  const input = e.target as HTMLInputElement
  selectedFavicon.value = input.files && input.files[0] ? input.files[0] : null
}

const uploadFavicon = async () => {
  if (!selectedFavicon.value) return
  isUploadingFavicon.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFavicon.value)
    const resp = await apiService.upload<{ message: string; url: string; profile?: any }>(
      '/settings/favicon',
      formData
    )
    const url = (resp as any).url || ''
    if (authStore.user) {
      authStore.user.profile = {
        ...authStore.user.profile,
        custom_favicon_url: url
      } as any
    }
    currentFavicon.value = url
    const existing = document.querySelector("link[rel~='icon']") as HTMLLinkElement | null
    if (existing) {
      existing.href = url
    } else {
      const link = document.createElement('link')
      link.rel = 'icon'
      link.href = url
      document.head.appendChild(link)
    }
    showSuccess('Favicon uploaded successfully!')
    selectedFavicon.value = null
  } catch (err: any) {
    showError('Failed to upload favicon', err.message)
  } finally {
    isUploadingFavicon.value = false
  }
}

const updateProfile = async () => {
  // Validate form
  profileErrors.value = { firstName: '', lastName: '' }

  if (!profileForm.value.firstName.trim()) {
    profileErrors.value.firstName = 'First name is required'
  }

  if (!profileForm.value.lastName.trim()) {
    profileErrors.value.lastName = 'Last name is required'
  }

  if (profileErrors.value.firstName || profileErrors.value.lastName) {
    return
  }

  isUpdatingProfile.value = true

  try {
    await authStore.updateProfile({
      first_name: profileForm.value.firstName,
      last_name: profileForm.value.lastName
    })
    
    showSuccess('Profile updated successfully!')
  } catch (err: any) {
    showError('Failed to update profile', err.message)
  } finally {
    isUpdatingProfile.value = false
  }
}

const changePassword = async () => {
  // Validate form
  passwordErrors.value = { currentPassword: '', newPassword: '', confirmPassword: '' }
  
  if (!passwordForm.value.currentPassword) {
    passwordErrors.value.currentPassword = 'Current password is required'
  }
  
  if (!passwordForm.value.newPassword) {
    passwordErrors.value.newPassword = 'New password is required'
  } else if (passwordForm.value.newPassword.length < 6) {
    passwordErrors.value.newPassword = 'Password must be at least 6 characters'
  }
  
  if (!passwordForm.value.confirmPassword) {
    passwordErrors.value.confirmPassword = 'Please confirm your password'
  } else if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordErrors.value.confirmPassword = 'Passwords do not match'
  }
  
  if (passwordErrors.value.currentPassword || passwordErrors.value.newPassword || passwordErrors.value.confirmPassword) {
    return
  }
  
  isChangingPassword.value = true
  
  try {
    await authStore.changePassword({
      new_password: passwordForm.value.newPassword,
      confirm_password: passwordForm.value.confirmPassword
    })
    
    showSuccess('Password changed successfully!')
    passwordForm.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (err: any) {
    showError('Failed to change password', err.message)
  } finally {
    isChangingPassword.value = false
  }
}

const updateAiSettings = async () => {
  isUpdatingAiSettings.value = true
  
  try {
    console.log('Updating AI settings:', {
      ai_provider: aiSettings.value.provider,
      response_delay_seconds: aiSettings.value.responseDelay
    })
    
    const response = await apiService.post('/settings', {
      ai_provider: aiSettings.value.provider,
      response_delay_seconds: aiSettings.value.responseDelay
    })
    
    console.log('AI settings update response:', response)
    
    // Immediately update the auth store to sync the UI
    if (authStore.user) {
      authStore.user.profile = {
        ...authStore.user.profile,
        ai_provider: aiSettings.value.provider,
        response_delay_seconds: aiSettings.value.responseDelay
      }
    }
    
    showSuccess('AI settings updated successfully!')
  } catch (err: any) {
    console.error('AI settings update error:', err)
    showError('Failed to update AI settings', err.message)
  } finally {
    isUpdatingAiSettings.value = false
  }
}

const updateXelenceCredentials = async () => {
  // Validate form
  xelenceErrors.value = { affiliateId: '', apiKey: '' }
  
  if (!xelenceForm.value.affiliateId.trim()) {
    xelenceErrors.value.affiliateId = 'Affiliate ID is required'
  }
  
  if (!xelenceForm.value.apiKey.trim()) {
    xelenceErrors.value.apiKey = 'API Key is required'
  }
  
  if (xelenceErrors.value.affiliateId || xelenceErrors.value.apiKey) {
    return
  }
  
  isUpdatingXelence.value = true
  
  try {
    await apiService.post('/settings', {
      xelence_affiliateid: xelenceForm.value.affiliateId,
      xelence_x_api_key: xelenceForm.value.apiKey
    })
    
    showSuccess('Xelence credentials updated successfully!')
    xelenceApiStatus.value = true
  } catch (err: any) {
    showError('Failed to update Xelence credentials', err.message)
  } finally {
    isUpdatingXelence.value = false
  }
}



// Dark mode functionality
const toggleDarkMode = () => {
  if (darkMode.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('darkMode', 'true')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('darkMode', 'false')
  }
}

const updateCustomization = async () => {
  isUpdatingCustomization.value = true
  customizationErrors.value = { websiteName: '', logoUrl: '', faviconUrl: '' }
  
  try {
    await apiService.post('/settings', {
      custom_website_name: customizationForm.value.websiteName,
      custom_logo_url: customizationForm.value.logoUrl,
      custom_favicon_url: customizationForm.value.faviconUrl
    })
    
    // Immediately update the auth store to sync the UI
    if (authStore.user) {
      authStore.user.profile = {
        ...authStore.user.profile,
        custom_website_name: customizationForm.value.websiteName,
        custom_logo_url: customizationForm.value.logoUrl,
        custom_favicon_url: customizationForm.value.faviconUrl
      }
      
      // Update document title immediately
      if (customizationForm.value.websiteName) {
        document.title = `${customizationForm.value.websiteName} Dashboard`
      }

      // Update favicon immediately if provided
      if (customizationForm.value.faviconUrl && customizationForm.value.faviconUrl.trim()) {
        const existing = document.querySelector("link[rel~='icon']") as HTMLLinkElement | null
        if (existing) {
          existing.href = customizationForm.value.faviconUrl.trim()
        } else {
          const link = document.createElement('link')
          link.rel = 'icon'
          link.href = customizationForm.value.faviconUrl.trim()
          document.head.appendChild(link)
        }
      }
    }
    
    showSuccess('Customization updated successfully!')
  } catch (err: any) {
    showError('Failed to update customization', err.message)
  } finally {
    isUpdatingCustomization.value = false
  }
}

const loadSettings = async () => {
  try {
    // Load profile data from auth store
    if (authStore.user) {
      profileForm.value = {
        firstName: authStore.user.profile?.first_name || '',
        lastName: authStore.user.profile?.last_name || ''
      }
      
      // Load AI settings from existing user data
      if (authStore.user.profile) {
        const profile = authStore.user.profile as any
        aiSettings.value = {
          provider: profile.ai_provider || 'gemini',
          responseDelay: profile.response_delay_seconds || 0
        }
      }
      
      // Load customization settings from existing user data
      if (authStore.user.profile) {
        const profile = authStore.user.profile as any
        customizationForm.value = {
          websiteName: profile.custom_website_name || '',
          logoUrl: profile.custom_logo_url || '',
          faviconUrl: profile.custom_favicon_url || ''
        }
        currentFavicon.value = profile.custom_favicon_url || ''
      }
      
      // Load Xelence credentials from existing user data
      if (authStore.user.profile) {
        xelenceForm.value = {
          affiliateId: authStore.user.profile.xelence_affiliateid || '',
          apiKey: authStore.user.profile.xelence_x_api_key ? '••••••••' : ''
        }
        xelenceApiStatus.value = !!(authStore.user.profile.xelence_affiliateid && authStore.user.profile.xelence_x_api_key)
      }
    }
    
    // Load API settings
    const apiResponse = await apiService.get('/settings/api') as { 
      usage?: { requests: number; tokens: number };
    }
    apiUsage.value = apiResponse.usage || { requests: 0, tokens: 0 }
    
    // Load dark mode from localStorage
    const savedDarkMode = localStorage.getItem('darkMode')
    darkMode.value = savedDarkMode === 'true'
    if (darkMode.value) {
      document.documentElement.classList.add('dark')
    }
    
  } catch (err: any) {
    console.error('Failed to load settings:', err)
  }
}

onMounted(async () => {
  // Wait for auth store to be initialized if needed
  if (authStore.user === null && !authStore.isLoading) {
    await authStore.initializeAuth()
  }
  
  loadSettings()
})
</script>
