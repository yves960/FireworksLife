<template>
  <div class="comment-item">
    <div class="comment-header">
      <span class="comment-author">{{ comment.author }}</span>
      <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
      <button
        v-if="canDelete"
        @click="handleDelete"
        class="delete-btn"
      >
        删除
      </button>
    </div>
    <div class="comment-content">{{ comment.content }}</div>
    
    <div v-if="comment.replies && comment.replies.length > 0" class="replies">
      <CommentItem
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
        @delete="$emit('delete', $event)"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../store/auth'

const props = defineProps({
  comment: {
    type: Object,
    required: true
  }
})

const authStore = useAuthStore()

const emit = defineEmits(['delete'])

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const canDelete = computed(() => {
  return authStore.isAuthenticated && authStore.user?.id === props.comment.author_id
})

const handleDelete = () => {
  if (confirm('确定要删除这条评论吗？')) {
    emit('delete', props.comment.id)
  }
}
</script>

<style scoped>
.comment-item {
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 6px;
}

.replies .comment-item {
  margin-top: 1rem;
  margin-left: 2rem;
  background: #f9f9f9;
}

.comment-header {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-weight: 500;
  color: #333;
}

.comment-date {
  color: #999;
  font-size: 0.85rem;
}

.delete-btn {
  margin-left: auto;
  padding: 0.25rem 0.75rem;
  border: 1px solid #fee;
  background: #fee;
  color: #c33;
  cursor: pointer;
  border-radius: 4px;
  font-size: 0.85rem;
}

.delete-btn:hover {
  background: #fcc;
  border-color: #fcc;
}

.comment-content {
  color: #555;
  line-height: 1.6;
}
</style>
