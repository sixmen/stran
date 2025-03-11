const STORAGE_API_KEY = 'api_key';
const STORAGE_TARGET_LANG = 'target_lang';

let popup = null;
let is_translation_enabled = false;
let last_highlighted_element = null;
let translating = false;

const LANGUAGES = {
  ko: '한국어',
  en: 'English',
  ja: '日本語',
  zh: '中文',
  es: 'Español',
  fr: 'Français',
  de: 'Deutsch',
};

const style = document.createElement('style');
style.textContent = `
  .s-trans-hoverable {
    background-color: rgba(0, 96, 223, 0.1) !important;
    cursor: pointer !important;
  }
`;
document.head.appendChild(style);

chrome.runtime.onMessage.addListener((message) => {
  if (message.type === 'translationStateChanged') {
    is_translation_enabled = message.enabled;
    if (!is_translation_enabled) {
      hidePopup();
    }
  }
});

function createPopup() {
  const popup = document.createElement('div');
  popup.style.cssText = `
    position: fixed;
    background: white;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    z-index: 10000;
    font-family: system-ui, -apple-system, sans-serif;
    font-size: 14px;
    display: none;
  `;

  const translate_button = document.createElement('button');
  translate_button.textContent = 'Translate';
  translate_button.style.cssText = `
    background: #0060df;
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
  `;

  translate_button.addEventListener('click', handleTranslate);
  popup.appendChild(translate_button);
  document.body.appendChild(popup);
  return popup;
}

function showPopup(x, y) {
  if (!is_translation_enabled) {
    return;
  }

  if (!popup) {
    popup = createPopup();
  }

  popup.style.display = 'block';
  popup.style.left = `${x}px`;
  popup.style.top = `${y}px`;
}

function hidePopup() {
  if (popup) {
    popup.style.display = 'none';
  }
}

document.addEventListener('mouseup', (event) => {
  if (!is_translation_enabled || translating) {
    return;
  }

  const selection = window.getSelection();
  const selected_text = selection.toString().trim();
  if (selected_text) {
    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    showPopup(rect.left, rect.bottom + 5);
  } else {
    hidePopup();
  }
});

async function handleTranslate() {
  if (!is_translation_enabled || translating) {
    return;
  }

  hidePopup();

  const storage = await chrome.storage.local.get([STORAGE_API_KEY, STORAGE_TARGET_LANG]);
  const api_key = storage[STORAGE_API_KEY];
  const target_lang = storage[STORAGE_TARGET_LANG] || 'ko'; // Default to Korean if not set
  if (!api_key) {
    alert('Please set your OpenAI API key in the extension settings');
    return;
  }

  try {
    translating = true;

    const selection = window.getSelection();
    const common_ancestor = selection.getRangeAt(0).commonAncestorContainer;
    selection.removeAllRanges();
    const range = document.createRange();
    range.selectNodeContents(common_ancestor);
    selection.addRange(range);
    const selected_text = selection.toString().trim();
    const paragraphs = selected_text
      .split(/\n+/)
      .map((p) => p.trim())
      .filter((p) => p);
    const paragraph_nodes = [];
    const paragraph_node_next_siblings = [];

    // Find last text nodes that contain the paragraph text
    let paragraph_index = 0;
    let remain_paragraph_text = paragraphs[paragraph_index];
    const walker = document.createTreeWalker(common_ancestor, NodeFilter.SHOW_TEXT, () => NodeFilter.FILTER_ACCEPT);
    let node;
    while ((node = walker.nextNode())) {
      const lines = node.textContent
        .trim()
        .split(/\n+/)
        .map((p) => p.trim())
        .filter((p) => p);
      for (const line of lines) {
        if (line && remain_paragraph_text.startsWith(line)) {
          remain_paragraph_text = remain_paragraph_text.slice(line.length).trim();
          if (remain_paragraph_text.length === 0) {
            paragraph_nodes.push(node);
            paragraph_node_next_siblings.push(node.nextSibling);
            paragraph_index++;
            remain_paragraph_text = paragraphs[paragraph_index];
          }
        }
      }
    }
    while (paragraph_index < paragraphs.length) {
      paragraph_nodes.push(range.endContainer);
      paragraph_node_next_siblings.push(range.endContainer.nextSibling);
      paragraph_index++;
    }
    selection.removeAllRanges();

    for (let i = 0; i < paragraphs.length; i++) {
      let result_element;
      try {
        const paragraph = paragraphs[i];
        const paragraph_node = paragraph_nodes[i];
        const paragraph_node_next_sibling = paragraph_node_next_siblings[i];

        result_element = document.createElement('span');
        result_element.textContent = 'Translating...';
        result_element.style.cssText = `
            color: #666;
            margin-top: 0.5em;
            margin-bottom: 0.5em;
          `;
        const container = document.createElement('span');
        container.appendChild(document.createElement('br'));
        container.appendChild(result_element);
        paragraph_node.parentNode.insertBefore(container, paragraph_node_next_sibling);

        const response = await fetch('https://api.openai.com/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${api_key}`,
          },
          body: JSON.stringify({
            model: 'gpt-4o-mini',
            messages: [
              {
                role: 'system',
                content: `You are a translator. Translate the given text to ${LANGUAGES[target_lang]}. Only respond with the translated text, without any additional explanation or context.`,
              },
              {
                role: 'user',
                content: paragraph,
              },
            ],
          }),
        });
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error?.message || 'Translation failed');
        }
        const translated_text = data.choices[0].message.content.trim();
        result_element.textContent = translated_text;
      } catch (error) {
        result_element.textContent = `Translation error: ${error.message}`;
      }
    }
  } catch (error) {
    alert(`Translation error: ${error.message}`);
  } finally {
    translating = false;
  }
}

document.addEventListener('mousedown', (event) => {
  if (popup && !popup.contains(event.target)) {
    hidePopup();
  }
});

function isInteractiveElement(element) {
  return (
    element.tagName === 'INPUT' ||
    element.tagName === 'TEXTAREA' ||
    element.tagName === 'SELECT' ||
    element.tagName === 'BUTTON' ||
    element.tagName === 'A'
  );
}

document.addEventListener('mousemove', (event) => {
  if (!is_translation_enabled || translating) {
    return;
  }

  const target = event.target;
  if (last_highlighted_element === target) {
    return;
  }

  removeHighlight();

  // Skip if hovering over the popup or interactive elements
  if (popup?.contains(target) || isInteractiveElement(target)) {
    return;
  }

  // Add highlight to current element if it has text
  if (target.textContent?.trim()) {
    target.classList.add('s-trans-hoverable');
    last_highlighted_element = target;
  }
});

document.addEventListener('mouseleave', () => {
  removeHighlight();
});

document.addEventListener('click', (event) => {
  if (!is_translation_enabled || translating) {
    return;
  }

  removeHighlight();

  const clicked_element = event.target;

  // Skip if clicking on the popup or if element is interactive
  if (popup?.contains(clicked_element) || isInteractiveElement(clicked_element)) {
    return;
  }

  const text = clicked_element.textContent?.trim();
  if (!text) {
    return;
  }

  const selection = window.getSelection();
  selection.removeAllRanges();
  const range = document.createRange();
  range.selectNodeContents(clicked_element);
  selection.addRange(range);

  if (event.ctrlKey || event.metaKey) {
    handleTranslate();
  } else {
    const rect = range.getBoundingClientRect();
    showPopup(rect.left, rect.bottom + 5);
  }
});

function removeHighlight() {
  if (last_highlighted_element) {
    last_highlighted_element.classList.remove('s-trans-hoverable');
    last_highlighted_element = null;
  }
}
