<template>
  <BaseLayout>
    <div class="space-y-8">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Knowledge Base</h1>
          <p class="text-gray-600">Manage your chatbot's instructions and FAQs</p>
        </div>
      </div>

      <!-- Tabs -->
      <div class="mb-6">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <button
              @click="activeTab = 'instructions'"
              :class="activeTab === 'instructions' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              class="whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm"
            >
              Instructions
            </button>
            <button
              @click="activeTab = 'faqs'"
              :class="activeTab === 'faqs' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              class="whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm"
            >
              FAQs
            </button>
          </nav>
        </div>
      </div>

      <!-- Instructions Tab -->
      <div v-if="activeTab === 'instructions'" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Instructions Content -->
        <div class="lg:col-span-2">
          <BaseCard>
            <template #header>
              <div class="flex items-center justify-between">
                <h3 class="text-lg font-medium text-gray-900">System Instructions</h3>
                <BaseButton
                  variant="primary"
                  size="sm"
                  @click="openInstructionModal"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  {{ userInstruction ? 'Edit Instructions' : 'Add Instructions' }}
                </BaseButton>
              </div>
            </template>

            <div v-if="isLoadingInstructions" class="flex items-center justify-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            </div>

            <div v-else-if="userInstruction" class="space-y-4">
              <div class="bg-gray-50 rounded-lg p-4">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-gray-700">Current Instructions</span>
                  <span class="text-xs text-gray-500">
                    Updated {{ formatTimeAgo(userInstruction.updated_at) }}
                  </span>
                </div>
                <div class="prose prose-sm max-w-none">
                  <pre class="whitespace-pre-wrap text-sm text-gray-800 font-mono bg-white p-3 rounded border">{{ userInstruction.instructions }}</pre>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-8">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 class="mt-2 text-sm font-medium text-gray-900">No instructions</h3>
              <p class="mt-1 text-sm text-gray-500">Get started by adding system instructions for your chatbot.</p>
              <div class="mt-6">
                <BaseButton variant="primary" @click="openInstructionModal">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Add Instructions
                </BaseButton>
              </div>
            </div>
          </BaseCard>
        </div>

        <!-- File Upload -->
        <div class="lg:col-span-1">
          <BaseCard>
            <template #header>
              <h3 class="text-lg font-medium text-gray-900">Upload Instructions File</h3>
            </template>

            <div class="space-y-4">
              <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <div class="mt-4">
                  <label for="instruction-file" class="cursor-pointer">
                    <span class="mt-2 block text-sm font-medium text-gray-900">
                      Upload .txt or .pdf file
                    </span>
                    <span class="mt-1 block text-sm text-gray-500">
                      Drag and drop or click to browse
                    </span>
                  </label>
                  <input
                    id="instruction-file"
                    ref="instructionFileInput"
                    type="file"
                    accept=".txt,.pdf"
                    class="sr-only"
                    @change="handleInstructionFileSelect"
                  />
                </div>
              </div>

              <div v-if="selectedInstructionFile" class="bg-gray-50 rounded-lg p-3">
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-3">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <div>
                      <p class="text-sm font-medium text-gray-900">{{ selectedInstructionFile.name }}</p>
                      <p class="text-xs text-gray-500">{{ formatFileSize(selectedInstructionFile.size) }}</p>
                    </div>
                  </div>
                  <BaseButton
                    variant="ghost"
                    size="sm"
                    @click="clearInstructionFile"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </BaseButton>
                </div>
              </div>

              <div class="flex space-x-3">
                <BaseButton
                  variant="primary"
                  :loading="isUploadingInstruction"
                  :disabled="!selectedInstructionFile"
                  @click="uploadInstructionFile"
                  class="flex-1"
                >
                  Upload & Parse
                </BaseButton>
                <BaseButton
                  variant="secondary"
                  :disabled="!selectedInstructionFile"
                  @click="clearInstructionFile"
                >
                  Clear
                </BaseButton>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>

      <!-- FAQs Tab -->
      <div v-if="activeTab === 'faqs'" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- FAQs List -->
        <div class="lg:col-span-2">
          <BaseCard>
            <template #header>
              <div class="flex items-center justify-between">
                <h3 class="text-lg font-medium text-gray-900">FAQs</h3>
                <BaseButton
                  variant="primary"
                  size="sm"
                  @click="openFaqModal"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Add FAQ
                </BaseButton>
              </div>
            </template>

            <div class="space-y-4">
              <!-- Search -->
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <input
                  v-model="faqSearchQuery"
                  type="text"
                  placeholder="Search FAQs..."
                  class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />
              </div>

              <!-- FAQs List -->
              <div v-if="isLoadingFaqs" class="flex items-center justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              </div>

              <div v-else-if="filteredFaqs.length === 0" class="text-center py-8">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <h3 class="mt-2 text-sm font-medium text-gray-900">No FAQs found</h3>
                <p class="mt-1 text-sm text-gray-500">Get started by adding your first FAQ.</p>
                <div class="mt-6">
                  <BaseButton variant="primary" @click="openFaqModal">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    Add FAQ
                  </BaseButton>
                </div>
              </div>

              <div v-else class="space-y-3">
                <div
                  v-for="faq in filteredFaqs"
                  :key="faq.id"
                  class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow"
                >
                  <div class="flex items-start justify-between">
                    <div class="flex-1">
                      <h4 class="text-sm font-medium text-gray-900 mb-2">{{ faq.question }}</h4>
                      <p class="text-sm text-gray-600 mb-3">{{ faq.answer }}</p>
                      <div class="flex items-center space-x-4 text-xs text-gray-500">
                        <span>Created {{ formatTimeAgo(faq.created_at) }}</span>
                        <span v-if="faq.updated_at && faq.updated_at !== faq.created_at">
                          Updated {{ formatTimeAgo(faq.updated_at) }}
                        </span>
                        <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          Priority {{ faq.priority }}
                        </span>
                      </div>
                    </div>
                    <div class="flex items-center space-x-2 ml-4">
                      <BaseButton
                        variant="ghost"
                        size="sm"
                        @click="editFaq(faq)"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </BaseButton>
                      <BaseButton
                        variant="ghost"
                        size="sm"
                        @click="deleteFaq(faq.id)"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </BaseButton>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </BaseCard>
        </div>

        <!-- FAQ File Upload -->
        <div class="lg:col-span-1">
          <BaseCard>
            <template #header>
              <h3 class="text-lg font-medium text-gray-900">Upload FAQ File</h3>
            </template>

            <div class="space-y-4">
              <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <div class="mt-4">
                  <label for="faq-file" class="cursor-pointer">
                    <span class="mt-2 block text-sm font-medium text-gray-900">
                      Upload .txt or .pdf file
                    </span>
                    <span class="mt-1 block text-sm text-gray-500">
                      Format: Q: Question\nA: Answer
                    </span>
                  </label>
                  <input
                    id="faq-file"
                    ref="faqFileInput"
                    type="file"
                    accept=".txt,.pdf"
                    class="sr-only"
                    @change="handleFaqFileSelect"
                  />
                </div>
              </div>

              <div v-if="selectedFaqFile" class="bg-gray-50 rounded-lg p-3">
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-3">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <div>
                      <p class="text-sm font-medium text-gray-900">{{ selectedFaqFile.name }}</p>
                      <p class="text-xs text-gray-500">{{ formatFileSize(selectedFaqFile.size) }}</p>
                    </div>
                  </div>
                  <BaseButton
                    variant="ghost"
                    size="sm"
                    @click="clearFaqFile"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </BaseButton>
                </div>
              </div>

              <div class="flex space-x-3">
                <BaseButton
                  variant="primary"
                  :loading="isUploadingFaq"
                  :disabled="!selectedFaqFile"
                  @click="uploadFaqFile"
                  class="flex-1"
                >
                  Upload & Parse
                </BaseButton>
                <BaseButton
                  variant="secondary"
                  :disabled="!selectedFaqFile"
                  @click="clearFaqFile"
                >
                  Clear
                </BaseButton>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>
    </div>

    <!-- Instruction Modal -->
    <BaseModal
      :is-open="showInstructionModal"
      title="System Instructions"
      size="xl"
      @close="closeInstructionModal"
    >
      <form @submit.prevent="saveInstruction" class="space-y-6">
        <div class="space-y-2">
          <label class="form-label">Instructions</label>
          <textarea
            v-model="instructionForm.instructions"
            class="form-textarea"
            rows="12"
            placeholder="Enter system instructions for your chatbot..."
            :class="instructionErrors.instructions ? 'border-error-300' : ''"
          ></textarea>
          <p v-if="instructionErrors.instructions" class="form-error">{{ instructionErrors.instructions }}</p>
          <p class="text-sm text-gray-500">
            These instructions will guide how your chatbot behaves and responds to users.
          </p>
        </div>
      </form>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <BaseButton variant="secondary" @click="closeInstructionModal">
            Cancel
          </BaseButton>
          <BaseButton
            variant="primary"
            :loading="isSavingInstruction"
            @click="saveInstruction"
          >
            {{ userInstruction ? 'Update' : 'Save' }} Instructions
          </BaseButton>
        </div>
      </template>
    </BaseModal>

    <!-- FAQ Modal -->
    <BaseModal
      :is-open="showFaqModal"
      :title="editingFaq ? 'Edit FAQ' : 'Add New FAQ'"
      size="xl"
      @close="closeFaqModal"
    >
      <form @submit.prevent="saveFaq" class="space-y-6">
        <div class="grid grid-cols-1 gap-6">
          <BaseInput
            v-model="faqForm.question"
            label="Question"
            placeholder="Enter the question..."
            :error="faqErrors.question"
            required
          />
          
          <div class="space-y-2">
            <label class="form-label">Answer</label>
            <textarea
              v-model="faqForm.answer"
              class="form-textarea"
              rows="6"
              placeholder="Enter the answer..."
              :class="faqErrors.answer ? 'border-error-300' : ''"
            ></textarea>
            <p v-if="faqErrors.answer" class="form-error">{{ faqErrors.answer }}</p>
          </div>
          
          <BaseInput
            v-model.number="faqForm.priority"
            label="Priority"
            type="number"
            min="1"
            max="10"
            placeholder="1"
            :error="faqErrors.priority"
          />
        </div>
      </form>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <BaseButton variant="secondary" @click="closeFaqModal">
            Cancel
          </BaseButton>
          <BaseButton
            variant="primary"
            :loading="isSavingFaq"
            @click="saveFaq"
          >
            {{ editingFaq ? 'Update' : 'Create' }} FAQ
          </BaseButton>
        </div>
      </template>
    </BaseModal>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useToast } from '@/composables/useToast'
import { apiService } from '@/services/api'
import BaseLayout from '@/components/BaseLayout.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseInput from '@/components/BaseInput.vue'
import BaseModal from '@/components/BaseModal.vue'

const { showSuccess, showError } = useToast()

// Tab state
const activeTab = ref('instructions')

// Instructions state
const userInstruction = ref(null)
const isLoadingInstructions = ref(false)
const showInstructionModal = ref(false)
const instructionForm = ref({
  instructions: ''
})
const instructionErrors = ref({})
const isSavingInstruction = ref(false)

// File upload state
const selectedInstructionFile = ref(null)
const instructionFileInput = ref(null)
const isUploadingInstruction = ref(false)

// FAQs state
const faqs = ref([])
const isLoadingFaqs = ref(false)
const showFaqModal = ref(false)
const editingFaq = ref(null)
const faqForm = ref({
  question: '',
  answer: '',
  priority: 1
})
const faqErrors = ref({})
const isSavingFaq = ref(false)
const faqSearchQuery = ref('')

// FAQ file upload state
const selectedFaqFile = ref(null)
const faqFileInput = ref(null)
const isUploadingFaq = ref(false)

// Computed
const filteredFaqs = computed(() => {
  if (!faqSearchQuery.value) return faqs.value
  
  const query = faqSearchQuery.value.toLowerCase()
  return faqs.value.filter(faq =>
    faq.question.toLowerCase().includes(query) ||
    faq.answer.toLowerCase().includes(query)
  )
})

// Utility functions
const formatTimeAgo = (dateString) => {
  if (!dateString) return 'Unknown'
  
  const date = new Date(dateString)
  const now = new Date()
  
  if (isNaN(date.getTime())) {
    const timestamp = parseInt(dateString)
    if (!isNaN(timestamp)) {
      const dateFromTimestamp = new Date(timestamp)
      if (!isNaN(dateFromTimestamp.getTime())) {
        const seconds = Math.round((now.getTime() - dateFromTimestamp.getTime()) / 1000)
        const minutes = Math.round(seconds / 60)
        const hours = Math.round(minutes / 60)
        const days = Math.round(hours / 24)

        if (seconds < 60) return `${seconds} sec ago`
        if (minutes < 60) return `${minutes} min ago`
        if (hours < 24) return `${hours} hr ago`
        return `${days} days ago`
      }
    }
    return 'Invalid date'
  }
  
  const seconds = Math.round((now.getTime() - date.getTime()) / 1000)
  const minutes = Math.round(seconds / 60)
  const hours = Math.round(minutes / 60)
  const days = Math.round(hours / 24)

  if (seconds < 60) return `${seconds} sec ago`
  if (minutes < 60) return `${minutes} min ago`
  if (hours < 24) return `${hours} hr ago`
  return `${days} days ago`
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Instructions functions
const loadInstructions = async () => {
  isLoadingInstructions.value = true
  
  try {
    const response = await apiService.get('/instructions')
    userInstruction.value = response
  } catch (err: any) {
    if (err.response?.status === 404) {
      userInstruction.value = null
    } else {
      showError('Failed to load instructions', err.message)
    }
  } finally {
    isLoadingInstructions.value = false
  }
}

const openInstructionModal = () => {
  if (userInstruction.value) {
    instructionForm.value.instructions = userInstruction.value.instructions
  } else {
    instructionForm.value.instructions = ''
  }
  instructionErrors.value = {}
  showInstructionModal.value = true
}

const closeInstructionModal = () => {
  showInstructionModal.value = false
  instructionForm.value.instructions = ''
  instructionErrors.value = {}
}

const saveInstruction = async () => {
  isSavingInstruction.value = true
  instructionErrors.value = {}
  
  try {
    if (!instructionForm.value.instructions.trim()) {
      instructionErrors.value.instructions = 'Instructions are required'
      return
    }
    
    const response = await apiService.post('/instructions', {
      instructions: instructionForm.value.instructions
    })
    
    userInstruction.value = response
    showSuccess('Instructions saved successfully!')
    closeInstructionModal()
  } catch (err: any) {
    showError('Failed to save instructions', err.message)
  } finally {
    isSavingInstruction.value = false
  }
}

const handleInstructionFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedInstructionFile.value = file
  }
}

const clearInstructionFile = () => {
  selectedInstructionFile.value = null
  if (instructionFileInput.value) {
    instructionFileInput.value.value = ''
  }
}

const uploadInstructionFile = async () => {
  if (!selectedInstructionFile.value) return
  
  isUploadingInstruction.value = true
  
  try {
    const formData = new FormData()
    formData.append('file', selectedInstructionFile.value)
    
    const response = await apiService.post('/parse-instructions-file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    instructionForm.value.instructions = response.content
    showSuccess('File parsed successfully!')
    clearInstructionFile()
    openInstructionModal()
  } catch (err: any) {
    showError('Failed to parse file', err.message)
  } finally {
    isUploadingInstruction.value = false
  }
}

// FAQ functions
const loadFaqs = async () => {
  isLoadingFaqs.value = true
  
  try {
    const response = await apiService.get('/faqs')
    faqs.value = response
  } catch (err: any) {
    showError('Failed to load FAQs', err.message)
  } finally {
    isLoadingFaqs.value = false
  }
}

const openFaqModal = () => {
  editingFaq.value = null
  faqForm.value = {
    question: '',
    answer: '',
    priority: 1
  }
  faqErrors.value = {}
  showFaqModal.value = true
}

const editFaq = (faq) => {
  editingFaq.value = faq
  faqForm.value = {
    question: faq.question,
    answer: faq.answer,
    priority: faq.priority
  }
  faqErrors.value = {}
  showFaqModal.value = true
}

const closeFaqModal = () => {
  showFaqModal.value = false
  editingFaq.value = null
  faqForm.value = {
    question: '',
    answer: '',
    priority: 1
  }
  faqErrors.value = {}
}

const saveFaq = async () => {
  isSavingFaq.value = true
  faqErrors.value = {}
  
  try {
    if (!faqForm.value.question.trim()) {
      faqErrors.value.question = 'Question is required'
      return
    }
    if (!faqForm.value.answer.trim()) {
      faqErrors.value.answer = 'Answer is required'
      return
    }
    
    if (editingFaq.value) {
      await apiService.put(`/faqs/${editingFaq.value.id}`, faqForm.value)
      showSuccess('FAQ updated successfully!')
    } else {
      await apiService.post('/faqs', faqForm.value)
      showSuccess('FAQ created successfully!')
    }
    
    loadFaqs()
    closeFaqModal()
  } catch (err: any) {
    showError('Failed to save FAQ', err.message)
  } finally {
    isSavingFaq.value = false
  }
}

const deleteFaq = async (id) => {
  if (!confirm('Are you sure you want to delete this FAQ?')) {
    return
  }
  
  try {
    await apiService.delete(`/faqs/${id}`)
    showSuccess('FAQ deleted successfully!')
    loadFaqs()
  } catch (err: any) {
    showError('Failed to delete FAQ', err.message)
  }
}

const handleFaqFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFaqFile.value = file
  }
}

const clearFaqFile = () => {
  selectedFaqFile.value = null
  if (faqFileInput.value) {
    faqFileInput.value.value = ''
  }
}

const uploadFaqFile = async () => {
  if (!selectedFaqFile.value) return
  
  isUploadingFaq.value = true
  
  try {
    const formData = new FormData()
    formData.append('file', selectedFaqFile.value)
    
    const response = await apiService.post('/parse-faq-file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    // Create FAQs from parsed content
    for (const faqData of response.faqs) {
      await apiService.post('/faqs', faqData)
    }
    
    showSuccess(`${response.faqs.length} FAQs created successfully!`)
    clearFaqFile()
    loadFaqs()
  } catch (err: any) {
    showError('Failed to parse FAQ file', err.message)
  } finally {
    isUploadingFaq.value = false
  }
}

// Lifecycle
onMounted(() => {
  loadInstructions()
  loadFaqs()
})
</script>