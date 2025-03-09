const STORAGE_API_KEY = 'api_key';
const STORAGE_TARGET_LANG = 'target_lang';

document.addEventListener('DOMContentLoaded', async () => {
  const api_key_input = document.getElementById('apiKeyInput');
  const target_lang_select = document.getElementById('targetLangSelect');
  const save_button = document.getElementById('saveButton');
  const message_area = document.getElementById('messageArea');

  const storage = await chrome.storage.local.get([STORAGE_API_KEY, STORAGE_TARGET_LANG]).catch(() => ({}));
  api_key_input.value = storage[STORAGE_API_KEY] || '';
  target_lang_select.value = storage[STORAGE_TARGET_LANG] || 'ko';

  save_button.addEventListener('click', async () => {
    const api_key = api_key_input.value.trim();
    const target_lang = target_lang_select.value;

    if (!api_key) {
      message_area.textContent = 'Please enter an API key';
      return;
    }

    try {
      await chrome.storage.local.set({
        [STORAGE_API_KEY]: api_key,
        [STORAGE_TARGET_LANG]: target_lang,
      });
      message_area.textContent = 'Settings saved successfully!';
      setTimeout(() => {
        message_area.textContent = '';
      }, 2000);
    } catch (error) {
      message_area.textContent = error.message;
    }
  });
});
