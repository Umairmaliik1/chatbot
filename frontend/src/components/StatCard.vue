<template>
  <BaseCard class="relative overflow-hidden">
    <div class="flex items-center justify-between">
      <div class="flex-1">
        <p class="text-sm font-medium text-gray-600 mb-1">{{ title }}</p>
        <div class="flex items-baseline">
          <p v-if="loading" class="text-2xl font-semibold text-gray-300">
            <div class="skeleton h-8 w-16"></div>
          </p>
          <p v-else class="text-2xl font-semibold text-gray-900">{{ formattedValue }}</p>
          <div v-if="trend" class="ml-2 flex items-baseline text-sm font-semibold" :class="trendClass">
            <svg class="self-center flex-shrink-0 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="trendIcon" />
            </svg>
            <span class="sr-only">{{ trend > 0 ? 'Increased' : 'Decreased' }} by</span>
            {{ Math.abs(trend) }}%
          </div>
        </div>
        <p v-if="!loading" class="text-sm text-gray-500 mt-1">{{ period }}</p>
      </div>
      <div class="flex-shrink-0">
        <div class="w-12 h-12 rounded-lg flex items-center justify-center" :class="iconBgClass">
          <svg class="w-6 h-6" :class="iconClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="icon" />
          </svg>
        </div>
      </div>
    </div>
    
    <!-- Loading overlay -->
    <div v-if="loading" class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center">
      <div class="spinner w-6 h-6"></div>
    </div>
  </BaseCard>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Component } from 'vue'
import BaseCard from './BaseCard.vue'
// Using simple SVG icons instead of Heroicons
const ArrowUpIcon = 'M5 10l7-7m0 0l7 7m-7-7v18'
const ArrowDownIcon = 'M19 14l-7 7m0 0l-7-7m7 7V3'
const MinusIcon = 'M20 12H4'

interface Props {
  title: string
  value: number
  period: string
  loading?: boolean
  icon: string
  trend?: number
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const formattedValue = computed(() => {
  if (typeof props.value === 'number') {
    if (props.value >= 1000000) {
      return (props.value / 1000000).toFixed(1) + 'M'
    } else if (props.value >= 1000) {
      return (props.value / 1000).toFixed(1) + 'K'
    }
    return props.value.toLocaleString()
  }
  return props.value
})

const trendClass = computed(() => {
  if (!props.trend) return ''
  return props.trend > 0 ? 'text-success-600' : 'text-error-600'
})

const trendIcon = computed(() => {
  if (!props.trend) return MinusIcon
  return props.trend > 0 ? ArrowUpIcon : ArrowDownIcon
})

const iconBgClass = computed(() => {
  // Generate consistent background color based on icon
  const colors = [
    'bg-primary-100',
    'bg-success-100', 
    'bg-warning-100',
    'bg-error-100',
    'bg-purple-100',
    'bg-indigo-100',
    'bg-pink-100',
    'bg-blue-100'
  ]
  
  // Simple hash function to get consistent color
  const hash = props.title.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0)
    return a & a
  }, 0)
  
  return colors[Math.abs(hash) % colors.length]
})

const iconClass = computed(() => {
  const bgClass = iconBgClass.value
  if (bgClass.includes('primary')) return 'text-primary-600'
  if (bgClass.includes('success')) return 'text-success-600'
  if (bgClass.includes('warning')) return 'text-warning-600'
  if (bgClass.includes('error')) return 'text-error-600'
  if (bgClass.includes('purple')) return 'text-purple-600'
  if (bgClass.includes('indigo')) return 'text-indigo-600'
  if (bgClass.includes('pink')) return 'text-pink-600'
  if (bgClass.includes('blue')) return 'text-blue-600'
  return 'text-gray-600'
})
</script>
