import { marked } from 'marked';
import DOMPurify from 'dompurify';

// Configure marked options
marked.setOptions({
  gfm: true, // GitHub Flavored Markdown
  breaks: true, // Convert \n to <br>
  headerIds: true, // Add ids to headers
  mangle: false, // Don't escape HTML
  sanitize: false // Let DOMPurify handle sanitization
});

// Custom renderer to handle specific formatting
const renderer = new marked.Renderer();

// Customize heading rendering
renderer.heading = (text, level) => {
  const escapedText = text.toLowerCase().replace(/[^\w]+/g, '-');
  return `
    <h${level} class="text-h${level} q-my-md" id="${escapedText}">
      ${text}
    </h${level}>
  `;
};

// Customize link rendering
renderer.link = (href, title, text) => {
  return `<a href="${href}" target="_blank" rel="noopener noreferrer" class="text-primary">${text}</a>`;
};

// Customize paragraph rendering
renderer.paragraph = (text) => {
  return `<p class="q-mb-md">${text}</p>`;
};

// Set the custom renderer
marked.use({ renderer });

/**
 * Converts text to markdown format
 * @param {string} text - Raw text to convert to markdown
 * @returns {string} Formatted markdown text
 */
export const formatToMarkdown = (text) => {
  if (!text) return '';

  // Convert common patterns to markdown
  let markdown = text
    // Headers
    .replace(/^(.*?)\n={3,}/gm, '# $1')
    .replace(/^(.*?)\n-{3,}/gm, '## $1')
    
    // Lists
    .replace(/^\s*[\d]+\.\s+/gm, '1. ')
    .replace(/^\s*[-*]\s+/gm, '- ')
    
    // Emphasis
    .replace(/\b_(\w[\w\s]*\w)_\b/g, '*$1*')
    .replace(/\*{2}(\w[\w\s]*\w)\*{2}/g, '**$1**')
    
    // Links
    .replace(/\b(https?:\/\/[^\s]+)\b/g, '[$1]($1)')
    
    // Paragraphs
    .replace(/\n{2,}/g, '\n\n')
    
    // Tables (basic detection)
    .replace(/(\|[^\n]+\|)\n/g, '$1\n|---|\n');

  return markdown;
};

/**
 * Converts markdown text to sanitized HTML
 * @param {string} markdown - The markdown text to convert
 * @returns {string} Sanitized HTML string
 */
export const markdownToHtml = (markdown) => {
  if (!markdown) return '';
  
  // Convert markdown to HTML
  const rawHtml = marked(markdown);
  
  // Sanitize HTML to prevent XSS
  const cleanHtml = DOMPurify.sanitize(rawHtml, {
    ADD_TAGS: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
    ADD_ATTR: ['target', 'rel']
  });
  
  return cleanHtml;
};