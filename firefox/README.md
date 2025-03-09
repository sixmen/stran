# S-Trans Firefox Extension

S-Trans is a Firefox browser extension that translates webpage text using OpenAI's API.

## Features

- Translate selected text to multiple languages (Korean, English, Japanese, Chinese, Spanish, French, German)
- Translation popup appears when text is selected on a webpage
- Click any text element to automatically select and translate it
- Quick translate with Command/Ctrl + Click (translates immediately without showing popup)
- Works on all websites

## Installation

1. Open Firefox browser and navigate to `about:debugging`
2. Click on "This Firefox" tab
3. Click "Load Temporary Add-on" button
4. Select the `firefox/manifest.json` file from this repository

## How to Use

1. Click the extension icon to open settings
2. Enter your OpenAI API Key and select your target translation language
3. There are three ways to translate text:
   - Select any text and click the "Translate" button that appears
   - Click on any text element to select it and show the translate button
   - Hold Command (Mac) or Ctrl (Windows/Linux) and click text to translate immediately
4. The translation will appear below the original text in gray

## Important Notes

- OpenAI API Key is required to use this extension
- API usage may incur costs depending on your OpenAI account plan
