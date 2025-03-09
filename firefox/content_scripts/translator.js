const STORAGE_API_KEY = 'api_key';

let selected_text = '';
let popup = null;
let is_translation_enabled = false;

browser.runtime.onMessage.addListener((message) => {
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
  if (!is_translation_enabled) {
    return;
  }

  const selection = window.getSelection();
  selected_text = selection.toString().trim();

  if (selected_text) {
    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    showPopup(rect.left, rect.bottom + 5);
  } else {
    hidePopup();
  }
});

async function handleTranslate() {
  if (!selected_text || !is_translation_enabled) {
    return;
  }

  hidePopup();

  let container;
  try {
    const result = await browser.storage.local.get(STORAGE_API_KEY);
    if (!result[STORAGE_API_KEY]) {
      alert('Please set your OpenAI API key in the extension settings');
      return;
    }

    const selection = window.getSelection();
    const range = selection.getRangeAt(0);

    const temp_element = document.createElement('span');
    temp_element.textContent = 'Translating...';
    temp_element.style.color = '#666';
    container = document.createElement('span');
    container.appendChild(document.createElement('br'));
    container.appendChild(temp_element);

    range.collapse(false);
    range.insertNode(container);
    selection.removeAllRanges();

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${result[STORAGE_API_KEY]}`,
      },
      body: JSON.stringify({
        model: 'gpt-4o-mini',
        messages: [
          {
            role: 'system',
            content:
              'You are a translator. Translate the given text to Korean. Only respond with the translated text, without any additional explanation or context.',
          },
          {
            role: 'user',
            content: selected_text,
          },
        ],
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error?.message || 'Translation failed');
    }

    const translated_text = data.choices[0].message.content.trim();
    const translation = document.createElement('span');
    translation.textContent = translated_text;
    translation.style.color = '#666';
    temp_element.parentNode.replaceChild(translation, temp_element);
  } catch (error) {
    alert(`Translation error: ${error.message}`);
    container?.parentNode?.removeChild(container);
  }
}

document.addEventListener('mousedown', (event) => {
  if (popup && !popup.contains(event.target)) {
    hidePopup();
  }
});
