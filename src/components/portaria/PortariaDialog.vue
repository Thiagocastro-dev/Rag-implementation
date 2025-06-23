<template>
  <q-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    maximized
    transition-show="slide-up"
    transition-hide="slide-down"
  >
    <q-card>
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">{{ formatPortariaId(portaria?._id) }}</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>

      <q-card-section class="q-pt-md">
        <div class="portaria-content" v-html="formattedContent"></div>
      </q-card-section>

      <q-card-section v-if="portaria?.tags?.length">
        <div class="text-subtitle2 q-mb-sm">Tags:</div>
        <q-chip
          v-for="tag in portaria.tags"
          :key="tag"
          size="sm"
          color="primary"
          text-color="white"
        >
          {{ tag }}
        </q-chip>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Fechar" color="primary" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { computed } from 'vue';
import { formatPortariaId } from '../../utils/formatters';
import { formatToMarkdown, markdownToHtml } from '../../utils/markdown';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  portaria: {
    type: Object,
    default: () => ({})
  }
});

defineEmits(['update:modelValue']);

const formattedContent = computed(() => {
  if (!props.portaria?.content) return '';
  const markdown = formatToMarkdown(props.portaria.content);
  return markdownToHtml(markdown);
});
</script>

<style>
.portaria-content {
  font-size: 16px;
  line-height: 1.6;
  max-width: 800px;
  margin: 0 auto;
}

.portaria-content h1,
.portaria-content h2,
.portaria-content h3,
.portaria-content h4,
.portaria-content h5,
.portaria-content h6 {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.portaria-content a {
  color: var(--q-primary);
  text-decoration: none;
}

.portaria-content a:hover {
  text-decoration: underline;
}

.portaria-content ul,
.portaria-content ol {
  padding-left: 1.5em;
  margin-bottom: 1em;
}

.portaria-content li {
  margin-bottom: 0.5em;
}

.portaria-content blockquote {
  border-left: 4px solid var(--q-primary);
  margin: 1em 0;
  padding-left: 1em;
  color: #666;
}

.portaria-content code {
  background-color: #f5f5f5;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: monospace;
}

.portaria-content pre {
  background-color: #f5f5f5;
  padding: 1em;
  border-radius: 4px;
  overflow-x: auto;
}

.portaria-content table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

.portaria-content th,
.portaria-content td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.portaria-content th {
  background-color: #f5f5f5;
}
</style>