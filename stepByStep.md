# Step-by-Step Guide: Build a Skin Tone Color Matching App (Streamlit)

This guide will walk you through building a web app that detects your skin tone from a photo and suggests matching colors, with clickable swatches that let you search for clothing in those colors.

---

## 1. Set Up Your Environment

1. **Install Python 3.8+** (if not already installed)
2. **Install required packages:**
   ```sh
   pip install streamlit pillow
   ```

---

## 2. Create Your Project Directory

1. Make a new folder for your project, e.g.:
   ```sh
   mkdir skin-tone-matcher
   cd skin-tone-matcher
   ```
2. Inside this folder, create a file named `app.py`.

---

## 3. Write the Streamlit App (`app.py`)

1. **Import libraries:**
   - `streamlit` for the web UI
   - `PIL` (Pillow) for image processing
   - `collections.Counter` for color analysis
   - `colorsys` for color math
2. **Set up the UI:**
   - Add a title and instructions
   - Use `st.file_uploader` to let users upload images
   - Store uploaded images in `st.session_state` for persistence
3. **Process each uploaded image:**
   - Open the image with Pillow
   - Resize for faster processing
   - Filter out background/outlier pixels
   - Find the most common (dominant) skin tone pixel
4. **Suggest matching colors:**
   - Use a function to map the detected skin tone to a palette of matching colors (using hue and lightness)
5. **Display color swatches:**
   - Show each palette color as a clickable swatch (button + colored box)
   - When clicked, show a search bar to enter a clothing item
   - When a clothing item is entered, show a Google Images link for that color + item (using a color name, not just hex)
6. **Allow clearing all uploaded photos.**

---

## 4. Run the App

1. In your terminal, run:
   ```sh
   streamlit run app.py
   ```
   If you get a `command not found` error, try:
   ```sh
   python3 -m streamlit run app.py
   ```
2. The app will open in your browser. Upload a photo and try the features!

---

## 5. (Optional) Customize

- Add more color names to the palette mapping for better search results.
- Adjust the color matching logic for your needs.
- Style the UI further with Streamlit components.

---

## 6. Example File Structure

```
skin-tone-matcher/
  app.py
```

---

## 7. Troubleshooting

- If Streamlit is not found, check your Python environment and PATH.
- If color names are missing, add them to the color name mapping in `app.py`.
- For best results, use clear, well-lit photos with your skin centered.

---

## 8. Next Steps

- Deploy your app with Streamlit Cloud or another Python web host.
- Expand to mobile (see React Native/Expo version in this project for inspiration).

---

Enjoy your personalized color matcher!
