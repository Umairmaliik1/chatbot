<template>
  <BaseLayout>
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Settings</h1>
          <p class="mt-2 text-gray-600">Manage your account settings and preferences.</p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Settings Navigation -->
      <BaseCard class="lg:col-span-1">
        <div class="card-header">
          <h3 class="text-lg font-semibold text-gray-900">Settings</h3>
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
            <h3 class="text-lg font-semibold text-gray-900">Profile Information</h3>
            <p class="text-sm text-gray-600 mt-1">Update your personal information</p>
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
            <h3 class="text-lg font-semibold text-gray-900">Security Settings</h3>
            <p class="text-sm text-gray-600 mt-1">Manage your password and security preferences</p>
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

        <!-- API Settings -->
        <div v-if="activeTab === 'api'" class="space-y-6">
          <div class="card-header">
            <h3 class="text-lg font-semibold text-gray-900">API Configuration</h3>
            <p class="text-sm text-gray-600 mt-1">Manage your API keys and integrations</p>
          </div>
          
          <div class="space-y-6 p-6">
            <!-- Xelence Integration -->
            <div class="border border-gray-200 rounded-lg p-4">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <h4 class="text-sm font-medium text-gray-900">Xelence Integration</h4>
                  <p class="text-sm text-gray-500">Configure your Xelence affiliate credentials for media reports</p>
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

            <!-- Google Gemini API -->
            <div class="border border-gray-200 rounded-lg p-4">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <h4 class="text-sm font-medium text-gray-900">Google Gemini API</h4>
                  <p class="text-sm text-gray-500">Configure your Gemini API key for AI responses</p>
                </div>
                <div class="flex items-center space-x-2">
                  <div class="w-3 h-3 rounded-full" :class="geminiApiStatus ? 'bg-success-400' : 'bg-warning-400'"></div>
                  <span class="text-sm font-medium" :class="geminiApiStatus ? 'text-success-600' : 'text-warning-600'">
                    {{ geminiApiStatus ? 'Configured' : 'Not Configured' }}
                  </span>
                </div>
              </div>
              
              <BaseInput
                v-model="apiForm.geminiApiKey"
                type="password"
                label="Gemini API Key"
                placeholder="Enter your Gemini API key"
                hint="You can get your API key from Google AI Studio"
              />
              
              <div class="mt-4 flex justify-end">
                <BaseButton
                  variant="primary"
                  size="sm"
                  :loading="isUpdatingApi"
                  @click="updateGeminiApiKey"
                >
                  Save API Key
                </BaseButton>
              </div>
            </div>

            <!-- API Usage Stats -->
            <div class="border border-gray-200 rounded-lg p-4">
              <h4 class="text-sm font-medium text-gray-900 mb-4">API Usage Statistics</h4>
              <div class="grid grid-cols-2 gap-4">
                <div class="text-center">
                  <div class="text-2xl font-bold text-primary-600">{{ apiUsage.requests }}</div>
                  <div class="text-sm text-gray-500">Total Requests</div>
                </div>
                <div class="text-center">
                  <div class="text-2xl font-bold text-success-600">{{ apiUsage.tokens }}</div>
                  <div class="text-sm text-gray-500">Tokens Used</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Preferences -->
        <div v-if="activeTab === 'preferences'" class="space-y-6">
          <div class="card-header">
            <h3 class="text-lg font-semibold text-gray-900">Preferences</h3>
            <p class="text-sm text-gray-600 mt-1">Customize your experience</p>
          </div>
          
          <div class="space-y-6 p-6">
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-sm font-medium text-gray-900">Email Notifications</h4>
                  <p class="text-sm text-gray-500">Receive email updates about your chatbot</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input
                    v-model="preferences.emailNotifications"
                    type="checkbox"
                    class="sr-only peer"
                  />
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-sm font-medium text-gray-900">Dark Mode</h4>
                  <p class="text-sm text-gray-500">Switch to dark theme</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input
                    v-model="preferences.darkMode"
                    type="checkbox"
                    class="sr-only peer"
                  />
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-sm font-medium text-gray-900">Auto-save</h4>
                  <p class="text-sm text-gray-500">Automatically save your work</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input
                    v-model="preferences.autoSave"
                    type="checkbox"
                    class="sr-only peer"
                  />
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
            </div>
            
            <div class="pt-4 border-t border-gray-200">
              <BaseButton
                variant="primary"
                :loading="isUpdatingPreferences"
                @click="updatePreferences"
              >
                Save Preferences
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
const CogIcon = 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z'
const KeyIcon = 'M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z'

const authStore = useAuthStore()
const { success: showSuccess, error: showError } = useToast()

const activeTab = ref('profile')

const settingsTabs = [
  { id: 'profile', name: 'Profile', icon: UserIcon },
  { id: 'security', name: 'Security', icon: ShieldCheckIcon },
  { id: 'api', name: 'API Settings', icon: KeyIcon },
  { id: 'preferences', name: 'Preferences', icon: CogIcon }
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

// API form
const apiForm = ref({
  geminiApiKey: ''
})

const geminiApiStatus = ref(false)
const isUpdatingApi = ref(false)
const apiUsage = ref({
  requests: 0,
  tokens: 0
})

// Preferences
const preferences = ref({
  emailNotifications: true,
  darkMode: false,
  autoSave: true
})

const isUpdatingPreferences = ref(false)

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

const updateGeminiApiKey = async () => {
  isUpdatingApi.value = true
  
  try {
    await apiService.post('/settings/gemini-api', {
      api_key: apiForm.value.geminiApiKey
    })
    
    showSuccess('Gemini API key updated successfully!')
    geminiApiStatus.value = true
  } catch (err: any) {
    showError('Failed to update API key', err.message)
  } finally {
    isUpdatingApi.value = false
  }
}

const updatePreferences = async () => {
  isUpdatingPreferences.value = true
  
  try {
    await apiService.put('/settings/preferences', preferences.value)
    showSuccess('Preferences updated successfully!')
  } catch (err: any) {
    showError('Failed to update preferences', err.message)
  } finally {
    isUpdatingPreferences.value = false
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
    const apiResponse = await apiService.get('/settings/api')
    geminiApiStatus.value = apiResponse.gemini_configured || false
    apiUsage.value = apiResponse.usage || { requests: 0, tokens: 0 }
    
    // Load preferences
    const prefsResponse = await apiService.get('/settings/preferences')
    preferences.value = { ...preferences.value, ...prefsResponse }
    
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
