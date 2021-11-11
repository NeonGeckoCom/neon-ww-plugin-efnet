## Description

plugin for https://github.com/Ant-Brain/EfficientWord-Net

## Install

`pip install neon_ww_plugin_efnet`

Then configure a wake_word with module set to `neon_ww_plugin_efnet`

```json
 "listener": {
      "wake_word": "hey mycroft"
 },
 "hotwords": {
    "hey mycroft": {
        "module": "neon_ww_plugin_efnet",
        "reference_file": "path/to/hey_mycroft_ref.json"
    }
  }
 
```
