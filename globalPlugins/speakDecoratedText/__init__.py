import globalPluginHandler
import ui
import sys
import os
import time
from scriptHandler import script
import api
plugin_dir = os.path.dirname(__file__)
if plugin_dir not in sys.path:
  sys.path.insert(0, plugin_dir)
try:
  from anyascii import anyascii
except ImportError as e:
  ui.message(f"Failed to import anyascii library: {e}")
  anyascii = None
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
  lastConvertedText = None
  lastPressTime = None
  def __init__(self):
    super().__init__()
  @script(
    description="Convert the current text to ASCII or copy it if it has already been converted.",
    gesture="kb:NVDA+Shift+Z"
  )
  def script_convertDecoratedText(self, gesture):
    try:
      currentTime = time.time()
      if GlobalPlugin.lastPressTime and (currentTime - GlobalPlugin.lastPressTime) < 0.5:
        if GlobalPlugin.lastConvertedText:
          api.copyToClip(GlobalPlugin.lastConvertedText)
          ui.message("Text copied to clipboard.")
          GlobalPlugin.lastConvertedText = None
        return
      GlobalPlugin.lastPressTime = currentTime
      reviewPos = api.getReviewPosition()
      text = reviewPos.text
      if text:
        if anyascii:
          converted = anyascii(text).lower()
          GlobalPlugin.lastConvertedText = converted
          ui.message(converted)
        else:
          ui.message("Anyascii library is unavailable.")
      else:
        ui.message("Nothing selected")
    except Exception as e:
      ui.message(f"An error occurred during conversion: {str(e)}")
  @script(
    description="Convert the current text to ASCII and copy it immediately to the clipboard",
    gesture="kb:control+shift+Z"
  )
  def script_convertAndCopyDecoratedText(self, gesture):
    try:
      reviewPos = api.getReviewPosition()
      text = reviewPos.text
      if text:
        if anyascii:
          converted = anyascii(text).lower()
          api.copyToClip(converted)
          GlobalPlugin.lastConvertedText = None
          ui.message("Text converted and copied to clipboard.")
        else:
          ui.message("Anyascii library is unavailable.")
      else:
        ui.message("Nothing selected.")
    except Exception as e:
      ui.message(f"An error occurred while copying: {str(e)}")
