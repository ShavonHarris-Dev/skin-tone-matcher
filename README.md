# Skin Tone Matcher

A web app that detects your skin tone from a photo and suggests matching colors, with clickable swatches that let you search for clothing in those colors. Built using [Streamlit](https://streamlit.io/) and [Pillow](https://python-pillow.org/).

---

## Features

- 📸 **Upload a Photo:** Detect the dominant skin tone from your image.
- 🎨 **Color Suggestions:** Get a palette of colors that match your skin tone.
- 🖱️ **Clickable Swatches:** Click on a color to search for clothing items in that color.
- 🔄 **Easy Reset:** Clear all uploaded images and try again.
- 💡 **Customizable:** Easily expand palettes, color logic, and UI.

---

## Quick Start

### 1. Installation

First, clone this repo and install the required Python packages:

```sh
git clone https://github.com/ShavonHarris-Dev/skin-tone-matcher.git
cd skin-tone-matcher
pip install streamlit pillow
```

### 2. Run the App

```sh
streamlit run app.py
```
- If you get a `command not found` error, try:
  ```sh
  python3 -m streamlit run app.py
  ```

### 3. Using the App

- The app will open in your browser.
- Upload a clear, well-lit photo with your skin centered.
- Explore suggested color palettes and click swatches to search for clothing items in those colors.

---

## Project Structure

```
skin-tone-matcher/
  app.py
  README.md
  stepByStep.md
```

---

## How It Works

1. **Image Upload:** User uploads a photo.
2. **Skin Tone Detection:** The app analyzes the image using Pillow, filters out background pixels, and finds the dominant skin tone.
3. **Palette Mapping:** Maps the detected skin tone to a palette of matching colors.
4. **Search Links:** Each color swatch can be clicked to search for clothing of that color using Google Images.

---

## Customization

- **Color Names:** Add or edit color names for better search results.
- **Matching Logic:** Adjust how skin tone maps to palettes in `app.py`.
- **UI Enhancements:** Style the interface further with Streamlit components.

---

## Troubleshooting

- **Streamlit not found:** Check your Python environment and PATH.
- **Missing color names:** Add them in the color name mapping in `app.py`.
- **Detection issues:** Use clear, well-lit, centered photos.

---

## Next Steps

- **Deploy:** Use [Streamlit Cloud](https://streamlit.io/cloud) or another Python web host to share your app.
- **Mobile:** Expand to mobile (see the React Native/Expo version in this repo for inspiration).

---

## License

MIT License

---

Enjoy your personalized color matcher!  
Feel free to open issues or PRs for improvements.
