# Capture the Rofi pages

Run these commands in a desktop terminal, from the repository root. Each waits 20 seconds so you can open Rofi on your main display and choose a tab. Run one command at a time:

```sh
python3 scripts/capture-rofi.py launcher
python3 scripts/capture-rofi.py windows
python3 scripts/capture-rofi.py clipboard
python3 scripts/capture-rofi.py screenshot-menu
python3 scripts/capture-rofi.py calculator
python3 scripts/capture-rofi.py wifi
python3 scripts/capture-rofi.py bluetooth
python3 scripts/capture-rofi.py packages
python3 scripts/capture-rofi.py package-details
python3 scripts/capture-rofi.py power
```

The default monitor is `DP-1` (the landscape display in the source desktop configuration). Check `hyprctl monitors` and use `--monitor NAME` if needed. Set `--delay 30` for more time. Repeat the same command for as many captures as you need: existing images are preserved and new captures receive numbered names such as `launcher-02.png`, `launcher-03.png`, and so on.

By default, the helper finds Rofi in Hyprland's layer/window list and captures only its rectangular bounds on the specified monitor. It fails without capturing if it cannot identify exactly one Rofi window there. Run it from a terminal on the other monitor, open Rofi on DP-1, and leave it open until capture completes. Avoid clicking outside a toggle-launched menu because that dismisses it.

This excludes the surrounding desktop, but does not create a transparent PNG: wallpaper visible through the translucent menu or its rounded corners remains part of the capture. To hide wallpaper through the panel, launch a temporary opaque preview:

```sh
~/.local/bin/rofi-recent -monitor DP-1 -theme-str 'window { background-color: #000000FF; opacity: 100%; }'
```

The override only applies to that launch. For the entire main monitor instead, use:

```sh
python3 scripts/capture-rofi.py main-monitor --full-monitor
```

Images are saved in this directory. Choose representative non-sensitive entries for clipboard, network and window previews before sharing them.
