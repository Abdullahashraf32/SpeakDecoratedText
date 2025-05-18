# SpeakDecoratedText Addon Documentation

This addon enhances NVDA screen reader by converting decorated or complex text into simplified ASCII text for easier reading and copying. It also includes features specifically to clean Arabic text and manage conversion history.

## Features

- Convert decorated text to plain ASCII and copy it to clipboard. This is very important because fancy Unicode texts are not readable with NVDA screen reader by default.
- Clean Arabic text and copy cleaned text to clipboard.
- Restore previously converted texts from history with repeated commands.

## Keyboard Shortcuts (Gestures)

- **NVDA + Shift + Z**:  
  Press once to hear the converted plain text spoken by the screen reader.  
  Press twice quickly to copy the last converted text to the clipboard.

- **NVDA + Shift + A**:  
  Clean selected Arabic text and copy it to clipboard. This improves readability by removing diacritics and decorative characters.

- **NVDA + Shift + H**:  
  Restore previously converted texts (press repeatedly to go back further in history).

## How It Works

The addon uses the `anyascii` Python library to transliterate decorated or non-ASCII characters into ASCII equivalents.  
For Arabic text, it uses a custom normalization function (`decoratedarabic.normalize_text`) to clean and simplify the text.

> **Note:** The `anyascii` library is required and is bundled automatically within the add-on folder.

## Implementation Overview

```python
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
  # Keeps a short history of converted texts (up to 3).
  # Uses time checks to detect repeated key presses.
  # Copies converted or cleaned text directly to clipboard.
  # Provides feedback messages through NVDA's UI.
```

## Usage Tips

- Use the convert shortcut twice quickly (within 0.5 seconds) to copy the converted text again.
- Use the restore shortcut multiple times to navigate backward through recent converted texts.
- Ensure text is selected or your review cursor is on the target text before using the shortcuts.
  This works on websites and in Microsoft Word using review mode.

## Used Libraries

| Library                            | Purpose                                                              |
| ---------------------------------- | -------------------------------------------------------------------- |
| `globalPluginHandler`              | Register the addon as a Global Plugin in NVDA's plugin system        |
| `ui`                               | Display messages and feedback to the user via NVDA's UI              |
| `sys`                              | Modify `sys.path` for importing local modules and `anyascii` library |
| `os`                               | Handle file paths for the addon directory                            |
| `time`                             | Measure time between key presses for gesture detection               |
| `re`                               | Pattern matching and replacing symbols                               |
| `unicodedata`                      | Normalize and clean text by removing decorations                     |
| `api`                              | Access NVDA functions and copy to clipboard                          |
| `from scriptHandler import script` | Define scripts as NVDA keyboard shortcuts                            |

## Contact & Support

- 💻 **GitHub Repository**:
  [SpeakDecoratedText on GitHub](https://github.com/Abdullahashraf32/SpeakDecoratedText)

- 📧 **Email**:
  [abdullahashraf4846@gmail.com](mailto:abdullahashraf4846@gmail.com)

- **WhatsApp**:
  [Contact me on WhatsApp](https://wa.me/+201148467527)

- **Telegram**:
  [@abdullahashraf4846](https://t.me/abdullahashraf4846)

- **YouTube Channel**:
  [Abdullah Ashraf on YouTube](https://www.youtube.com/@AbdullahAshraf-zc5dx)

```

```
