<template>
  <div class="flex flex-col h-[700px] w-[450px] bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 border-0 rounded-3xl shadow-2xl overflow-hidden animate-fade-in">
    <!-- Header -->
    <div class="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700 text-white p-6 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-shimmer"></div>
      <div class="flex items-center space-x-4 relative z-10">
        <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center animate-bounce-slow">
          🛒
        </div>
        <div>
          <h2 class="text-2xl font-bold bg-gradient-to-r from-white to-blue-100 bg-clip-text text-transparent">Wally</h2>
          <p class="text-blue-100 text-sm animate-pulse">Your Walmart Ally for best shopping Experience</p>
        </div>
      </div>
    </div>

    <!-- Messages -->
    <div class="flex-1 overflow-y-auto p-6 space-y-5" ref="messagesContainer">
      <div v-for="message in messages" :key="message.id" 
           :class="['flex', message.isUser ? 'justify-end' : 'justify-start']">
        <div :class="[
          'max-w-sm px-5 py-4 rounded-2xl text-sm shadow-lg transform transition-all duration-300 hover:scale-105 animate-slide-in',
          message.isUser 
            ? 'bg-gradient-to-r from-blue-500 via-purple-500 to-indigo-600 text-white shadow-blue-200' 
            : 'bg-gradient-to-r from-white to-gray-50 text-gray-800 border border-gray-200 shadow-gray-200'
        ]">
          {{ message.text }}
        </div>
      </div>

      <!-- Products Display -->
      <div v-if="optimizedProducts.length > 0" class="bg-gradient-to-br from-white via-green-50 to-emerald-50 rounded-3xl shadow-2xl border border-green-100 overflow-hidden animate-fade-in-up">
        <div class="bg-gradient-to-r from-green-500 via-emerald-500 to-teal-600 text-white p-5 relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
          <h3 class="font-bold text-xl flex items-center relative z-10">
            ✨ Your Optimized Smart Cart
          </h3>
          <p class="text-green-100 text-sm mt-1 relative z-10">AI-selected best value products</p>
        </div>
        <div class="p-5 space-y-4">
          <div v-for="(product, index) in optimizedProducts" :key="product.name" 
               class="bg-gradient-to-r from-white via-blue-50 to-purple-50 p-5 rounded-2xl border border-gray-200 hover:shadow-xl transition-all duration-300 transform hover:scale-102 animate-slide-in-delayed"
               :style="{animationDelay: index * 100 + 'ms'}">
            <div class="font-bold text-gray-900 mb-2 text-lg">{{ product.name }}</div>
            <div class="flex justify-between items-center mb-3">
              <span class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">${{ product.price }}</span>
              <div class="flex items-center space-x-2 bg-yellow-100 px-3 py-1 rounded-full">
                <span class="text-yellow-500 animate-pulse">⭐</span>
                <span class="text-sm font-semibold text-gray-700">{{ product.rating || 'N/A' }}</span>
              </div>
            </div>
            <div class="text-sm text-purple-600 font-medium mb-2">🏢 {{ product.brand }}</div>
            <div class="text-sm text-gray-600 leading-relaxed">{{ product.description }}</div>
          </div>
        </div>
        <div class="bg-gradient-to-r from-gray-50 via-green-50 to-blue-50 px-5 py-4 border-t border-gray-200">
          <div class="flex justify-between items-center mb-4">
            <span class="font-bold text-xl text-gray-900">💰 Total Cost:</span>
            <span class="font-bold text-3xl bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent animate-pulse">${{ totalPrice.toFixed(2) }}</span>
          </div>
          <button @click="goToCart" 
                  class="w-full bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700 text-white py-4 px-8 rounded-2xl hover:from-blue-700 hover:via-purple-700 hover:to-indigo-800 font-bold text-lg shadow-2xl transition-all duration-300 transform hover:scale-105 hover:shadow-purple-300 animate-bounce-slow">
            🛒 Proceed to Walmart Cart
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="flex justify-start">
        <div class="bg-gradient-to-r from-white via-blue-50 to-purple-50 px-6 py-4 rounded-2xl shadow-lg border border-blue-200 animate-pulse">
          <div class="flex items-center space-x-4">
            <div class="animate-spin rounded-full h-6 w-6 border-3 border-gradient-to-r from-blue-600 to-purple-600 border-t-transparent"></div>
            <div>
              <span class="text-gray-800 font-semibold">🤖 AI is analyzing your request...</span>
              <div class="text-xs text-gray-600 mt-1">Finding the best products and prices for you</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input -->
    <div class="bg-white/80 backdrop-blur-sm border-t border-gray-200 p-4">
      <div class="flex space-x-3">
        <input 
          v-model="inputMessage" 
          @keypress.enter="sendMessage"
          :disabled="isLoading"
          placeholder="e.g., 'pasta dinner for $20'"
          class="flex-1 border-2 border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
        />
        <button 
          @click="sendMessage" 
          :disabled="isLoading || !inputMessage.trim()"
          class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-xl hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold shadow-lg transition-all transform hover:scale-105"
        >
          Send
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, computed } from 'vue'

interface Message {
  id: number
  text: string
  isUser: boolean
}

interface Product {
  name: string
  price: number
  rating?: number
  brand: string
  category: string
  description: string
}

const messages = ref<Message[]>([
  { id: 1, text: "👋 Welcome to Smart Cart Builder! I'm your AI shopping assistant ready to help you find the best products at optimal prices. Simply tell me what you need and your budget, and I'll create a personalized shopping cart for you!", isUser: false }
])

const inputMessage = ref('')
const isLoading = ref(false)
const optimizedProducts = ref<Product[]>([])
const cartUrl = ref('')
const messagesContainer = ref<HTMLElement>()

let messageId = 2

const totalPrice = computed(() => {
  return optimizedProducts.value.reduce((sum, product) => sum + (product.price || 0), 0)
})

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isLoading.value) return

  const userMessage = inputMessage.value.trim()
  messages.value.push({ id: messageId++, text: userMessage, isUser: true })
  inputMessage.value = ''
  isLoading.value = true

  // Clear previous products
  optimizedProducts.value = []

  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: userMessage })
    })

    const data = await response.json()
    
    messages.value.push({ 
      id: messageId++, 
      text: data.message, 
      isUser: false 
    })

    if (data.optimized_products && data.optimized_products.length > 0) {
      optimizedProducts.value = data.optimized_products
      cartUrl.value = data.cart_url
    }

  } catch (error) {
    messages.value.push({ 
      id: messageId++, 
      text: "Sorry, I'm having trouble connecting to the server. Please try again.", 
      isUser: false 
    })
  } finally {
    isLoading.value = false
    await nextTick()
    scrollToBottom()
  }
}

const goToCart = () => {
  if (cartUrl.value) {
    window.open(cartUrl.value, '_blank')
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}
</script>

<style scoped>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slide-in {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes slide-in-delayed {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

@keyframes bounce-slow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.animate-fade-in { animation: fade-in 0.6s ease-out; }
.animate-slide-in { animation: slide-in 0.4s ease-out; }
.animate-slide-in-delayed { animation: slide-in-delayed 0.5s ease-out both; }
.animate-fade-in-up { animation: fade-in-up 0.7s ease-out; }
.animate-shimmer { animation: shimmer 2s infinite; }
.animate-bounce-slow { animation: bounce-slow 2s infinite; }
.hover\:scale-102:hover { transform: scale(1.02); }
</style>