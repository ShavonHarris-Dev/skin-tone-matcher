# Instructions for Building the Skin Tone Color Matching App

This file contains prompts and steps to guide the development of a simple Python app that helps users find colors that pair well with their skin tone.

## Prompts for Pairing with GitHub Copilot

1. **Upload Photo Prompt**
   - "Please upload a clear photo of your skin."
   - (App should provide a file upload interface.)

2. **Skin Tone Detection**
   - (App analyzes the uploaded image to extract the dominant skin tone.)
   - "Detect the main skin tone from the uploaded image."

3. **Show Matching Colors**
   - "Here are some colors that pair well with your skin tone:"
   - (App displays a palette of recommended colors.)

4. **Try Another Photo**
   - "Would you like to upload another photo?"
   - (App allows the user to repeat the process.)

## Prompts for Pairing with GitHub Copilot (React Native Version)

1. **Image Upload Prompt**
   - "Please select or take a photo of your skin."
   - (App should provide an image picker interface using react-native-image-picker or expo-image-picker.)

2. **Skin Tone Detection**
   - (App analyzes the selected image to extract the dominant skin tone, either on-device using a JS library like color-thief, or by sending the image to a backend API.)
   - "Detect the main skin tone from the selected image."

3. **Show Matching Colors**
   - "Here are some colors that pair well with your skin tone:"
   - (App displays a palette of recommended colors as colored views or swatches.)

4. **Try Another Photo**
   - "Would you like to select or take another photo?"
   - (App allows the user to repeat the process and view results for multiple images.)

5. **(Optional) Backend API Prompt**
   - "Send the image to a backend API for skin tone analysis and color suggestions."
   - (If using a Python backend, describe the API endpoint and expected response.)

## Development Steps

- Decide on the app type (web app recommended, e.g., Streamlit).
- Implement image upload functionality.
- Integrate skin tone detection from the image.
- Map detected skin tone to a set of matching colors.
- Display the color palette to the user.
- Allow the user to upload another photo if desired.

---

Use these prompts to guide your collaboration with GitHub Copilot while building the app.
