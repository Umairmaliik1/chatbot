<template>
  <Transition
    enter-active-class="transform ease-out duration-500 transition-all"
    enter-from-class="translate-x-full opacity-0 scale-95"
    enter-to-class="translate-x-0 opacity-100 scale-100"
    leave-active-class="transition ease-in duration-300"
    leave-from-class="opacity-100 scale-100"
    leave-to-class="opacity-0 scale-95 translate-x-4"
  >
    <div v-if="isVisible" class="corporate-toast" :class="toastClasses">
      <!-- Progress bar -->
      <div class="absolute top-0 left-0 h-1 w-full bg-black/5 rounded-t-xl overflow-hidden">
        <div 
          class="h-full progress-bar" 
          :class="progressClasses"
          :style="{ animationDuration: `${props.duration}ms` }"
        ></div>
      </div>
      
      <div class="flex items-start gap-4 p-5">
        <!-- Icon with background -->
        <div class="flex-shrink-0">
          <div class="flex items-center justify-center w-10 h-10 rounded-full" :class="iconBgClasses">
            <svg class="w-5 h-5" :class="iconClasses" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" :d="iconComponent" />
            </svg>
          </div>
        </div>
        
        <!-- Content -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2">
            <h4 class="font-semibold text-gray-900 text-sm leading-5">{{ title }}</h4>
            <span class="text-xs text-gray-400 font-medium">{{ timeAgo }}</span>
          </div>
          <p v-if="message" class="mt-1 text-sm text-gray-600 leading-5">{{ message }}</p>
        </div>
        
        <!-- Close button -->
        <div class="flex-shrink-0">
          <button
            @click="close"
            class="flex items-center justify-center w-8 h-8 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-200"
          >
            <span class="sr-only">Close</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// Icon definitions
const CheckCircleIcon = 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
const ExclamationTriangleIcon = 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z'
const InformationCircleIcon = 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
const XCircleIcon = 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z'

interface Props {
  type?: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info',
  duration: 5000
})

const emit = defineEmits<{
  close: []
}>()

const isVisible = ref(false)
const startTime = ref(Date.now())

const toastClasses = computed(() => {
  const typeClasses = {
    success: 'corporate-toast-success',
    error: 'corporate-toast-error', 
    warning: 'corporate-toast-warning',
    info: 'corporate-toast-info'
  }
  return typeClasses[props.type]
})

const iconComponent = computed(() => {
  const icons = {
    success: CheckCircleIcon,
    error: XCircleIcon,
    warning: ExclamationTriangleIcon,
    info: InformationCircleIcon
  }
  return icons[props.type]
})

const iconClasses = computed(() => {
  const typeClasses = {
    success: 'text-emerald-600',
    error: 'text-red-600',
    warning: 'text-amber-600',
    info: 'text-blue-600'
  }
  return typeClasses[props.type]
})

const iconBgClasses = computed(() => {
  const typeClasses = {
    success: 'bg-emerald-50 border border-emerald-100',
    error: 'bg-red-50 border border-red-100',
    warning: 'bg-amber-50 border border-amber-100',
    info: 'bg-blue-50 border border-blue-100'
  }
  return typeClasses[props.type]
})

const progressClasses = computed(() => {
  const typeClasses = {
    success: 'bg-emerald-500',
    error: 'bg-red-500',
    warning: 'bg-amber-500',
    info: 'bg-blue-500'
  }
  return typeClasses[props.type]
})

const timeAgo = computed(() => {
  return 'now'
})

const close = () => {
  isVisible.value = false
  setTimeout(() => {
    emit('close')
  }, 300)
}

onMounted(() => {
  isVisible.value = true
  startTime.value = Date.now()
  
  if (props.duration > 0) {
    setTimeout(() => {
      close()
    }, props.duration)
  }
})
</script>
