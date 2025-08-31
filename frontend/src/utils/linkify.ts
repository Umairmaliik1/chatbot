// Lightweight, safe linkify: escapes HTML, converts http/https URLs to <a>, and preserves newlines.
// Intended for rendering assistant (LLM) messages only.

const escapeHtml = (text: string) =>
  text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')

// Enhanced URL regex for http/https and www domains, handles more edge cases while stopping at problematic chars
const urlRegex = /((?:https?:\/\/|www\.)[^\s<>"'\[\](){}]+)/gi

export function linkify(input: string): string {
  console.log('🔍 Linkify called with input:', input)
  if (!input) return ''
  // 1) Escape HTML to avoid XSS
  const escaped = escapeHtml(input)
  console.log('🔍 After escaping:', escaped)
  // 2) Replace URLs with anchors
  const withLinks = escaped.replace(urlRegex, (url) => {
    console.log('🔗 Found URL:', url)
    // Add https:// prefix for www. URLs
    const safeHref = url.startsWith('www.') ? `https://${url}` : url
    const safeText = url
    const linkHtml = `<a href="${safeHref}" target="_blank" rel="nofollow noopener noreferrer" class="text-blue-600 dark:text-blue-400 underline decoration-blue-600 dark:decoration-blue-400 break-words hover:text-blue-800 dark:hover:text-blue-300 hover:decoration-blue-800 dark:hover:decoration-blue-300 transition-colors cursor-pointer">${safeText}</a>`
    console.log('🔗 Generated link HTML:', linkHtml)
    return linkHtml
  })
  console.log('🔍 Final result:', withLinks)
  // 3) Preserve line breaks
  return withLinks.replace(/\n/g, '<br/>')
}

