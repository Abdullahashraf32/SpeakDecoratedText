# -*- coding: UTF-8 -*-
# Import necessary NVDA and Python libraries
import globalPluginHandler
import ui
import sys
import os
import time
from scriptHandler import script
import api
from . import decoratedarabic  # Custom module for Arabic text normalization

# Add the current plugin directory to sys.path to allow relative imports
plugin_dir = os.path.dirname(__file__)
if plugin_dir not in sys.path:
  sys.path.insert(0, plugin_dir)

# Attempt to import the anyascii library used for transliteration
try:
  from anyascii import anyascii
except ImportError as e:
  ui.message(f"Failed to import anyascii library: {e}")
  anyascii = None

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
  """
  This class defines a global plugin for NVDA that provides:
  - Decorated (fancy) text conversion to plain ASCII.
  - Arabic text cleaning and normalization.
  - History-based restoration of previously converted texts.
  """

  # Static fields to maintain plugin state across gestures
  history = []           # Stores last few converted/cleaned texts
  lastPressTime = None   # Time of last key press (for double press detection)
  historyIndex = -1      # Current index while navigating history
  restoring = False      # Flag indicating if restore mode is active

  def __init__(self):
    """Initialize the global plugin."""
    super().__init__()

  def _addToHistory(self, text):
    """
    Add a new text entry to the history if it is different from the last one.
    Keeps a maximum of 3 history items.
    """
    if not GlobalPlugin.history or text != GlobalPlugin.history[-1]: 
      GlobalPlugin.history.append(text)
      if len(GlobalPlugin.history) > 3:
        GlobalPlugin.history.pop(0)
    GlobalPlugin.historyIndex = -1

  @script(
    description="Convert the current text to ASCII or copy it if it has already been converted.",
    gesture="kb:NVDA+Shift+Z"
  )
  def script_convertDecoratedText(self, gesture):
    """
    This script converts decorated (fancy Unicode) text at the review cursor
    to simplified ASCII using the anyascii library. If pressed twice quickly,
    it simply copies the last converted text to the clipboard.
    """
    try:
      currentTime = time.time()

      # If the key is pressed twice quickly, copy last result
      if GlobalPlugin.lastPressTime and (currentTime - GlobalPlugin.lastPressTime) < 0.5:
        if GlobalPlugin.history and GlobalPlugin.history[-1]:
          api.copyToClip(GlobalPlugin.history[-1])
          ui.message("Text copied to clipboard.")
        return

      GlobalPlugin.lastPressTime = currentTime
      reviewPos = api.getReviewPosition()
      text = reviewPos.text

      if text:
        if anyascii:
          converted = anyascii(text).lower()
          self._addToHistory(converted)
          api.copyToClip(converted)
          ui.message(converted)
        else:
          ui.message("Anyascii library is unavailable.")
      else:
        ui.message("No selection.")
    except Exception as e:
      ui.message(f"An error occurred during conversion: {str(e)}")

  @script(
    description="Clean Arabic text and copy to clipboard",
    gesture="kb:NVDA+Shift+A"
  )
  def script_cleanArabicText(self, gesture):
    """
    This script cleans selected Arabic text using a custom normalization
    function, removing diacritics and decorative characters, then copies
    the cleaned result to the clipboard.
    """
    try:
      reviewPos = api.getReviewPosition()
      text = reviewPos.text
      if not text:
        ui.message("No selection.")
        return
      cleaned = decoratedarabic.normalize_text(text)
      self._addToHistory(cleaned)
      api.copyToClip(cleaned)
      ui.message("The Arabic text cleaned and copied to clipboard.")
    except Exception as e:
      ui.message(f"An error occurred during Arabic text cleaning: {str(e)}")

  @script(
    description="Restore previously processed texts. Press repeatedly to go back further.",
    gesture="kb:NVDA+Shift+H"
  )
  def script_restorePreviousProcessedText(self, gesture):
    """
    This script allows users to restore previously converted or cleaned texts
    from history. Pressing the shortcut repeatedly quickly navigates further back.
    """
    try:
      currentTime = time.time()
      if GlobalPlugin.lastPressTime:
        timeDiff = currentTime - GlobalPlugin.lastPressTime
      else:
        timeDiff = None

      # If user is already restoring and pressed again quickly, go back further
      if timeDiff is not None and timeDiff < 0.5 and GlobalPlugin.restoring:
        GlobalPlugin.historyIndex -= 1
      else:
        GlobalPlugin.historyIndex = -1
        GlobalPlugin.restoring = True

      GlobalPlugin.lastPressTime = currentTime

      if abs(GlobalPlugin.historyIndex) <= len(GlobalPlugin.history):
        restoredText = GlobalPlugin.history[GlobalPlugin.historyIndex]
        api.copyToClip(restoredText)
        ui.message(f"Restored text: {restoredText}")
      else:
        ui.message("No more history to restore.")
        GlobalPlugin.restoring = False
    except Exception as e:
      ui.message(f"An error occurred while restoring: {str(e)}")
