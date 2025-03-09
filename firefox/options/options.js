const STORAGE_API_KEY = 'api_key';

document.addEventListener('DOMContentLoaded', async () => {
  const api_key_input = document.getElementById('apiKeyInput');
  const save_button = document.getElementById('saveButton');
  const message_area = document.getElementById('messageArea');

  const storage = await browser.storage.local.get([STORAGE_API_KEY]).catch(() => ({}));
  api_key_input.value = storage[STORAGE_API_KEY] || '';

  save_button.addEventListener('click', async () => {
    const api_key = api_key_input.value.trim();
    if (!api_key) {
      message_area.textContent = 'Please enter an API key';
      return;
    }

    try {
      await browser.storage.local.set({
        [STORAGE_API_KEY]: api_key,
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
