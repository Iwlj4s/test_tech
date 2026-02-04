<template>
  <div class="border-b border-gray-200 dark:border-gray-900 px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-900/50 transition cursor-pointer rounded-xl">
    <!-- Post Header -->
    <div class="flex gap-3">
      <!-- Avatar -->
      <img
        :src="post.authorAvatar"
        :alt="post.author"
        class="w-12 h-12 rounded-full"
      />

      <!-- Post Content -->
      <div class="flex-1">
        <!-- Author Info -->
        <div class="flex items-center gap-2 mb-1">
          <span class="font-bold text-gray-900 dark:text-white hover:underline">
            {{ post.author }}
          </span>
          <span class="text-gray-500 dark:text-gray-400">@{{ post.handle }}</span>
          <span class="text-gray-500 dark:text-gray-400">·</span>
          <span class="text-gray-500 dark:text-gray-400 text-sm">{{ post.time }}</span>
        </div>

        <!-- Post Text -->
        <p class="text-gray-900 dark:text-white mb-3 text-base">
          {{ post.content }}
        </p>

        <!-- Post Stats -->
        <div class="flex justify-between text-gray-500 dark:text-gray-400 max-w-xs text-sm py-2">
          <div class="flex items-center gap-2 hover:text-blue-500 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <span>{{ post.replies }}</span>
          </div>
          <div class="flex items-center gap-2 hover:text-green-500 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>{{ post.retweets }}</span>
          </div>
          <div class="flex items-center gap-2 hover:text-red-500 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            <span>{{ post.likes }}</span>
          </div>
          <div class="flex items-center gap-2 hover:text-blue-500 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  post: {
    type: Object,
    required: true
  }
})
</script>
