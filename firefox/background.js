const tab_states = new Map();

function updateIcon(tab_id, is_enabled) {
  const path = is_enabled
    ? {
        48: 'icons/icon-48.png',
        96: 'icons/icon-96.png',
      }
    : {
        48: 'icons/icon-48-disabled.png',
        96: 'icons/icon-96-disabled.png',
      };
  browser.browserAction.setIcon({
    path: path,
    tabId: tab_id,
  });
}

async function toggleTranslation(tab_id) {
  const current_state = tab_states.get(tab_id) || false;
  const new_state = !current_state;

  tab_states.set(tab_id, new_state);
  updateIcon(tab_id, new_state);

  try {
    await browser.tabs.sendMessage(tab_id, {
      type: 'translationStateChanged',
      enabled: new_state,
    });
  } catch (error) {
    console.error('Failed to notify content script:', error);
  }
}

browser.browserAction.onClicked.addListener(async (tab) => {
  await toggleTranslation(tab.id);
});

browser.tabs.onCreated.addListener((tab) => {
  tab_states.set(tab.id, false);
  updateIcon(tab.id, false);
});

browser.tabs.onRemoved.addListener((tab_id) => {
  tab_states.delete(tab_id);
});

browser.tabs.onUpdated.addListener(async (tab_id, change_info, _tab) => {
  if (change_info.status === 'complete') {
    const is_enabled = tab_states.get(tab_id) || false;
    updateIcon(tab_id, is_enabled);

    try {
      await browser.tabs.sendMessage(tab_id, {
        type: 'translationStateChanged',
        enabled: is_enabled,
      });
    } catch (error) {
      console.error('Failed to notify content script on page update:', error);
    }
  }
});
