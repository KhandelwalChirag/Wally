<template>
  <div class="flex flex-col h-[700px] w-[450px] bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 border-0 rounded-3xl shadow-2xl overflow-hidden animate-fade-in">
    <!-- Header -->
    <div class="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700 text-white p-6 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-shimmer"></div>
      <div class="flex items-center justify-between relative z-10">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center animate-bounce-slow">
            🛒
          </div>
          <div>
            <h2 class="text-2xl font-bold bg-gradient-to-r from-white to-blue-100 bg-clip-text text-transparent">Wally</h2>
            <p class="text-blue-100 text-sm animate-pulse">Your Walmart Ally for best shopping Experience</p>
          </div>
        </div>
        
        <!-- User Authentication -->
        <div v-if="!user" class="flex space-x-2">
          <button @click="showLoginForm = true; showRegisterForm = false" 
                  class="bg-white/20 hover:bg-white/30 text-white text-xs px-3 py-1 rounded-lg transition-all">
            Login
          </button>
          <button @click="showRegisterForm = true; showLoginForm = false" 
                  class="bg-white/20 hover:bg-white/30 text-white text-xs px-3 py-1 rounded-lg transition-all">
            Register
          </button>
        </div>
        <div v-else class="flex items-center space-x-2">
          <span class="text-xs text-white/80">{{ user.username }}</span>
          <button @click="logout" 
                  class="bg-white/20 hover:bg-white/30 text-white text-xs px-3 py-1 rounded-lg transition-all">
            Logout
          </button>
        </div>
      </div>
    </div>

    <!-- Login Form -->
    <div v-if="showLoginForm" class="bg-white p-6 animate-fade-in">
      <h3 class="text-xl font-bold text-gray-800 mb-4">Login</h3>
      <form @submit.prevent="login" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
          <input v-model="loginUsername" type="text" required 
                 class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input v-model="loginPassword" type="password" required 
                 class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <p v-if="loginError" class="text-red-500 text-sm">{{ loginError }}</p>
        <div class="flex justify-between">
          <button type="button" @click="showLoginForm = false" 
                  class="px-4 py-2 text-gray-600 hover:text-gray-800">
            Cancel
          </button>
          <button type="submit" :disabled="isLoading" 
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">
            Login
          </button>
        </div>
      </form>
    </div>
    
    <!-- Register Form -->
    <div v-else-if="showRegisterForm" class="bg-white p-6 animate-fade-in">
      <h3 class="text-xl font-bold text-gray-800 mb-4">Register</h3>
      <form @submit.prevent="register" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
          <input v-model="registerUsername" type="text" required 
                 class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input v-model="registerPassword" type="password" required 
                 class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <p v-if="registerError" class="text-red-500 text-sm">{{ registerError }}</p>
        <div class="flex justify-between">
          <button type="button" @click="showRegisterForm = false" 
                  class="px-4 py-2 text-gray-600 hover:text-gray-800">
            Cancel
          </button>
          <button type="submit" :disabled="isLoading" 
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">
            Register
          </button>
        </div>
      </form>
    </div>
    
    <!-- Messages -->
    <div v-else class="flex-1 overflow-y-auto p-6 space-y-5" ref="messagesContainer">
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

      <!-- Interrupt UI: Category Review -->
      <div v-if="currentInterrupt && currentInterrupt.type === 'category_review'" 
           class="bg-gradient-to-br from-white via-yellow-50 to-amber-50 rounded-3xl shadow-2xl border border-yellow-100 overflow-hidden animate-fade-in-up">
        <div class="bg-gradient-to-r from-yellow-500 via-amber-500 to-orange-500 text-white p-5 relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
          <h3 class="font-bold text-xl flex items-center relative z-10">
            📝 Category Review
          </h3>
          <p class="text-yellow-100 text-sm mt-1 relative z-10">{{ currentInterrupt.message }}</p>
        </div>
        <div class="p-5 space-y-4">
          <div v-for="(category, item) in currentInterrupt.suggested_categories" :key="item" 
               class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
            <div class="font-medium text-gray-800 mb-2">{{ item }}</div>
            <div class="flex items-center">
              <input 
                v-model="interruptResponses[item]" 
                :placeholder="category"
                class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-yellow-500"
              />
            </div>
          </div>
          <button @click="submitInterruptResponse('category_review')" 
                  class="w-full bg-gradient-to-r from-yellow-500 to-amber-500 text-white py-3 px-6 rounded-xl hover:from-yellow-600 hover:to-amber-600 font-bold shadow-lg transition-all transform hover:scale-105">
            Submit Categories
          </button>
        </div>
      </div>
      
      <!-- Interrupt UI: Product Review -->
      <div v-else-if="currentInterrupt && currentInterrupt.type === 'product_review'" 
           class="bg-gradient-to-br from-white via-blue-50 to-indigo-50 rounded-3xl shadow-2xl border border-blue-100 overflow-hidden animate-fade-in-up">
        <div class="bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 text-white p-5 relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
          <h3 class="font-bold text-xl flex items-center relative z-10">
            🔍 Product Review
          </h3>
          <p class="text-blue-100 text-sm mt-1 relative z-10">{{ currentInterrupt.message }}</p>
        </div>
        <div class="p-5 space-y-4 max-h-[300px] overflow-y-auto">
          <div v-for="(product, index) in currentInterrupt.products" :key="index" 
               class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
            <div class="font-medium text-gray-800 mb-1">{{ product.item }}</div>
            <div class="text-sm text-gray-600 mb-2">Category: {{ product.category }}</div>
            <div class="text-sm text-blue-600 mb-2">{{ product.options?.length || 0 }} options found</div>
            <button @click="toggleProductOptions(index)" 
                    class="text-sm text-indigo-600 hover:text-indigo-800 underline">
              {{ expandedProducts.includes(index) ? 'Hide options' : 'Show options' }}
            </button>
            <div v-if="expandedProducts.includes(index)" class="mt-3 space-y-2 pl-3 border-l-2 border-indigo-200">
              <div v-for="(option, optIndex) in product.options" :key="optIndex" 
                   class="text-sm p-2 bg-gray-50 rounded-lg">
                <div class="font-medium">{{ option.name }}</div>
                <div class="flex justify-between text-xs mt-1">
                  <span class="text-green-600 font-bold">${{ option.price }}</span>
                  <span class="text-amber-600">⭐ {{ option.rating || 'N/A' }}</span>
                </div>
              </div>
            </div>
          </div>
          <button @click="submitInterruptResponse('product_review')" 
                  class="w-full bg-gradient-to-r from-blue-500 to-indigo-500 text-white py-3 px-6 rounded-xl hover:from-blue-600 hover:to-indigo-600 font-bold shadow-lg transition-all transform hover:scale-105">
            Accept Products
          </button>
        </div>
      </div>
      
      <!-- Interrupt UI: Optimization Review -->
      <div v-else-if="currentInterrupt && currentInterrupt.type === 'optimization_review'" 
           class="bg-gradient-to-br from-white via-green-50 to-emerald-50 rounded-3xl shadow-2xl border border-green-100 overflow-hidden animate-fade-in-up">
        <div class="bg-gradient-to-r from-green-500 via-emerald-500 to-teal-500 text-white p-5 relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
          <h3 class="font-bold text-xl flex items-center relative z-10">
            ✨ Optimization Review
          </h3>
          <p class="text-green-100 text-sm mt-1 relative z-10">{{ currentInterrupt.message }}</p>
        </div>
        <div class="p-5 space-y-4">
          <div class="flex justify-between items-center mb-2">
            <span class="font-bold text-gray-800">Budget:</span>
            <span class="font-bold text-green-600">${{ currentInterrupt.budget?.toFixed(2) }}</span>
          </div>
          <div v-for="(product, index) in currentInterrupt.optimized_products" :key="index" 
               class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
            <div class="font-bold text-gray-900 mb-1">{{ product.name }}</div>
            <div class="flex justify-between items-center mb-2">
              <span class="text-xl font-bold text-green-600">${{ product.price }}</span>
              <div class="flex items-center space-x-1 bg-yellow-100 px-2 py-1 rounded-full">
                <span class="text-yellow-500">⭐</span>
                <span class="text-xs font-semibold text-gray-700">{{ product.rating || 'N/A' }}</span>
              </div>
            </div>
            <div class="text-xs text-purple-600 font-medium mb-1">{{ product.brand }}</div>
            <div class="text-xs text-gray-600">{{ product.description }}</div>
          </div>
          <div class="flex space-x-3">
            <button @click="rejectOptimization()" 
                    class="flex-1 bg-red-500 text-white py-3 px-4 rounded-xl hover:bg-red-600 font-bold shadow-lg transition-all">
              Reject
            </button>
            <button @click="submitInterruptResponse('optimization_review')" 
                    class="flex-1 bg-gradient-to-r from-green-500 to-emerald-500 text-white py-3 px-4 rounded-xl hover:from-green-600 hover:to-emerald-600 font-bold shadow-lg transition-all">
              Accept
            </button>
          </div>
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
    <div v-if="!showLoginForm && !showRegisterForm" class="bg-white/80 backdrop-blur-sm border-t border-gray-200 p-4">
      <div class="flex space-x-3">
        <input 
          v-model="inputMessage" 
          @keypress.enter="sendMessage"
          :disabled="isLoading || currentInterrupt"
          placeholder="e.g., 'pasta dinner for $20'"
          class="flex-1 border-2 border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
        />
        <button 
          @click="sendMessage" 
          :disabled="isLoading || !inputMessage.trim() || currentInterrupt"
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
  item?: string
}

interface Interrupt {
  type: string
  message: string
  items?: string[]
  suggested_categories?: Record<string, string>
  products?: any[]
  optimized_products?: Product[]
  budget?: number
}

interface User {
  username: string
  token: string
}

const messages = ref<Message[]>([
  { id: 1, text: "👋 Welcome to Smart Cart Builder! I'm your AI shopping assistant ready to help you find the best products at optimal prices. Simply tell me what you need and your budget, and I'll create a personalized shopping cart for you!", isUser: false }
])

const inputMessage = ref('')
const isLoading = ref(false)
const optimizedProducts = ref<Product[]>([])
const cartUrl = ref('')
const messagesContainer = ref<HTMLElement>()
const currentInterrupt = ref<Interrupt | null>(null)
const interruptResponses = ref<Record<string, string>>({})
const expandedProducts = ref<number[]>([])
const threadId = ref<string>('')
const user = ref<User | null>(null)
const showLoginForm = ref(false)
const showRegisterForm = ref(false)
const loginUsername = ref('')
const loginPassword = ref('')
const registerUsername = ref('')
const registerPassword = ref('')
const loginError = ref('')
const registerError = ref('')

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

  // Clear previous products and interrupt
  optimizedProducts.value = []
  currentInterrupt.value = null

  try {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }

    // Add authorization header if user is logged in
    if (user.value?.token) {
      headers['Authorization'] = `Bearer ${user.value.token}`
    }

    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers,
      body: JSON.stringify({ 
        message: userMessage,
        thread_id: threadId.value,
        user_id: user.value?.username
      })
    })

    const data = await response.json()
    
    // Save thread ID for future interactions
    if (data.thread_id) {
      threadId.value = data.thread_id
    }

    // Check if we have an interrupt
    if (data.interrupt) {
      currentInterrupt.value = data.interrupt
      interruptResponses.value = {}
      
      // For category review, pre-populate responses with suggested categories
      if (data.interrupt.type === 'category_review' && data.interrupt.suggested_categories) {
        Object.entries(data.interrupt.suggested_categories).forEach(([item, category]) => {
          interruptResponses.value[item] = category as string
        })
      }
      
      messages.value.push({ 
        id: messageId++, 
        text: data.interrupt.message, 
        isUser: false 
      })
    } else {
      messages.value.push({ 
        id: messageId++, 
        text: data.message, 
        isUser: false 
      })

      if (data.optimized_products && data.optimized_products.length > 0) {
        optimizedProducts.value = data.optimized_products
        cartUrl.value = data.cart_url
      }
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

const submitInterruptResponse = async (type: string) => {
  if (!threadId.value) return
  
  isLoading.value = true
  
  try {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }

    // Add authorization header if user is logged in
    if (user.value?.token) {
      headers['Authorization'] = `Bearer ${user.value.token}`
    }
    
    let data: any = {}
    
    if (type === 'category_review') {
      data = interruptResponses.value
    } else if (type === 'product_review') {
      // Just accept the products as is
      data = currentInterrupt.value?.products || []
    } else if (type === 'optimization_review') {
      // Just accept the optimized products as is
      data = currentInterrupt.value?.optimized_products || []
    }
    
    const response = await fetch('http://localhost:8000/resume', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        thread_id: threadId.value,
        data,
        user_id: user.value?.username
      })
    })
    
    const result = await response.json()
    
    // Clear current interrupt
    currentInterrupt.value = null
    
    // Check if we have another interrupt
    if (result.interrupt) {
      currentInterrupt.value = result.interrupt
      interruptResponses.value = {}
      
      // For category review, pre-populate responses with suggested categories
      if (result.interrupt.type === 'category_review' && result.interrupt.suggested_categories) {
        Object.entries(result.interrupt.suggested_categories).forEach(([item, category]) => {
          interruptResponses.value[item] = category as string
        })
      }
      
      messages.value.push({ 
        id: messageId++, 
        text: result.interrupt.message, 
        isUser: false 
      })
    } else {
      messages.value.push({ 
        id: messageId++, 
        text: result.message, 
        isUser: false 
      })

      if (result.optimized_products && result.optimized_products.length > 0) {
        optimizedProducts.value = result.optimized_products
        cartUrl.value = result.cart_url
      }
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

const toggleProductOptions = (index: number) => {
  const idx = expandedProducts.value.indexOf(index)
  if (idx === -1) {
    expandedProducts.value.push(index)
  } else {
    expandedProducts.value.splice(idx, 1)
  }
}

const rejectOptimization = () => {
  currentInterrupt.value = null
  messages.value.push({ 
    id: messageId++, 
    text: "I'll try to find better options. Please provide more details about what you're looking for.", 
    isUser: false 
  })
}

const login = async () => {
  loginError.value = ''
  isLoading.value = true
  
  try {
    const formData = new FormData()
    formData.append('username', loginUsername.value)
    formData.append('password', loginPassword.value)
    
    const response = await fetch('http://localhost:8000/token', {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      const error = await response.json()
      loginError.value = error.detail || 'Login failed'
      return
    }
    
    const data = await response.json()
    user.value = {
      username: loginUsername.value,
      token: data.access_token
    }
    
    showLoginForm.value = false
    loginUsername.value = ''
    loginPassword.value = ''
    
    messages.value.push({ 
      id: messageId++, 
      text: `Welcome back, ${user.value.username}! I'll personalize your shopping experience based on your preferences.`, 
      isUser: false 
    })
  } catch (error) {
    loginError.value = 'Connection error. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const register = async () => {
  registerError.value = ''
  isLoading.value = true
  
  try {
    const response = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: registerUsername.value,
        password: registerPassword.value
      })
    })
    
    if (!response.ok) {
      const error = await response.json()
      registerError.value = error.detail || 'Registration failed'
      return
    }
    
    // Auto-login after successful registration
    const formData = new FormData()
    formData.append('username', registerUsername.value)
    formData.append('password', registerPassword.value)
    
    const loginResponse = await fetch('http://localhost:8000/token', {
      method: 'POST',
      body: formData
    })
    
    const loginData = await loginResponse.json()
    user.value = {
      username: registerUsername.value,
      token: loginData.access_token
    }
    
    showRegisterForm.value = false
    registerUsername.value = ''
    registerPassword.value = ''
    
    messages.value.push({ 
      id: messageId++, 
      text: `Welcome, ${user.value.username}! I'll help you find the best products tailored to your preferences.`, 
      isUser: false 
    })
  } catch (error) {
    registerError.value = 'Connection error. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const logout = () => {
  user.value = null
  messages.value.push({ 
    id: messageId++, 
    text: "You've been logged out. You can still use Smart Cart Builder, but your preferences won't be saved.", 
    isUser: false 
  })
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

@keyframes pulse-border {
  0%, 100% { border-color: rgba(59, 130, 246, 0.5); }
  50% { border-color: rgba(99, 102, 241, 0.8); }
}

.animate-fade-in { animation: fade-in 0.6s ease-out; }
.animate-slide-in { animation: slide-in 0.4s ease-out; }
.animate-slide-in-delayed { animation: slide-in-delayed 0.5s ease-out both; }
.animate-fade-in-up { animation: fade-in-up 0.7s ease-out; }
.animate-shimmer { animation: shimmer 2s infinite; }
.animate-bounce-slow { animation: bounce-slow 2s infinite; }
.animate-pulse-border { animation: pulse-border 2s infinite; }
.hover\:scale-102:hover { transform: scale(1.02); }
</style>