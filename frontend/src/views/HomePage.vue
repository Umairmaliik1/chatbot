<template>
  <div class="min-h-screen bg-white">
    <!-- Header -->
    <header class="main-header">
      <div class="container">
        <router-link to="/" class="logo">
          <div class="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <span>AI Chatbot</span>
        </router-link>
        <nav class="main-nav">
          <!-- Future links can go here -->
        </nav>
        <div class="header-actions">
          <router-link to="/login" class="btn btn-secondary">Log In</router-link>
          <router-link to="/signup" class="btn btn-primary">Get Started</router-link>
        </div>
      </div>
    </header>

    <main>
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="container">
          <h1>Create Your Own AI Assistant</h1>
          <p class="subtitle">Build a custom AI chatbot powered by Google's Gemini API. Integrate with your tools and automate your customer support.</p>
          <router-link to="/signup" class="btn btn-primary btn-large">Get Started for Free</router-link>
          <p class="sub-cta">No credit card required. Start chatting in minutes.</p>
        </div>
      </section>

      <!-- Features Section -->
      <section id="features" class="features-section">
        <div class="container">
          <h2>One Tool for All Your Needs</h2>
          <p class="section-subtitle">From knowledge base integration to performance analytics, we've got you covered.</p>
          <div class="features-grid">
            <div v-for="feature in features" :key="feature.title" class="feature-card">
              <div class="feature-icon">
                <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="feature.icon" />
                </svg>
              </div>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="cta-section">
        <div class="container">
          <h2>Ready to Get Started?</h2>
          <p>Create your AI assistant today and transform your customer interactions.</p>
          <router-link to="/signup" class="btn btn-primary btn-large">Sign Up Now</router-link>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="main-footer">
      <div class="container">
        <p>&copy; 2024 AI Chatbot Service. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
// Using simple SVG icons instead of Heroicons
const CpuChipIcon = 'M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z'
const CogIcon = 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z'
const ChartBarIcon = 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
const ShieldCheckIcon = 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z'

const features = [
  {
    title: 'AI-Powered',
    description: 'Powered by Google\'s Gemini AI for intelligent, context-aware responses to your questions and support needs.',
    icon: CpuChipIcon
  },
  {
    title: 'Easy Integration',
    description: 'Connect your chatbot with external services like Kommo CRM to streamline your workflows and data synchronization.',
    icon: CogIcon
  },
  {
    title: 'Analytics & Reports',
    description: 'Monitor your bot\'s performance with a detailed dashboard showing usage statistics, conversation history, and more.',
    icon: ChartBarIcon
  },
  {
    title: 'Self-Hosted & Secure',
    description: 'Keep your data private. Our solution is fully self-hosted, giving you complete control over your information.',
    icon: ShieldCheckIcon
  }
]

const scrollToFeatures = () => {
  document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })
}
</script>
