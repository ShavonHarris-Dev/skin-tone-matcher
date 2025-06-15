import streamlit as st
from PIL import Image
from io import BytesIO
from collections import Counter
import colorsys

st.title("Skin Tone Color Matcher")

st.write("Upload a clear photo of your skin to find colors that pair well with your skin tone.")

# Store all uploaded images in session state
if 'uploaded_images' not in st.session_state:
    st.session_state['uploaded_images'] = []

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="uploader")

if uploaded_file is not None:
    st.session_state['uploaded_images'].append(uploaded_file.getvalue())
    st.success("Image uploaded! You can upload another photo if you want.")

if st.session_state['uploaded_images']:
    for idx, img_bytes in enumerate(st.session_state['uploaded_images']):
        image = Image.open(BytesIO(img_bytes))
        st.image(image, caption=f"Uploaded Image {idx+1}", use_container_width=True)
        # Skin tone detection using Pillow and Counter
        small_image = image.resize((50, 50))  # Resize for faster processing
        pixels = list(small_image.getdata())
        filtered_pixels = [p for p in pixels if isinstance(p, tuple) and len(p) >= 3 and 30 < p[0] < 230 and 30 < p[1] < 230 and 30 < p[2] < 230]
        if filtered_pixels:
            most_common = Counter(filtered_pixels).most_common(1)[0][0]
            st.write(f"Detected skin tone (RGB): {most_common}")
            # Show matching colors
            def get_matching_colors(skin_rgb):
                r, g, b = [x / 255.0 for x in skin_rgb]
                h, l, s = colorsys.rgb_to_hls(r, g, b)
                # Use both hue and lightness for more nuanced matching
                if l < 0.3:
                    # Deep skin tones
                    if h < 0.1 or h > 0.9:
                        # Red undertone
                        return [
                            (255, 160, 122),  # Light Salmon
                            (255, 218, 185),  # Peach Puff
                            (255, 255, 224),  # Light Yellow
                            (70, 130, 180),   # Steel Blue
                            (186, 85, 211)    # Medium Orchid
                        ]
                    else:
                        # Golden/neutral undertone
                        return [
                            (255, 215, 0),    # Gold
                            (255, 239, 213),  # Papaya Whip
                            (205, 133, 63),   # Peru
                            (72, 61, 139),    # Dark Slate Blue
                            (46, 139, 87)     # Sea Green
                        ]
                elif l < 0.6:
                    # Medium skin tones
                    if h < 0.15:
                        # Warm undertone
                        return [
                            (255, 222, 173),  # Navajo White
                            (255, 182, 193),  # Light Pink
                            (255, 228, 181),  # Moccasin
                            (60, 179, 113),   # Medium Sea Green
                            (210, 180, 140)   # Tan
                        ]
                    elif h > 0.6:
                        # Olive undertone
                        return [
                            (189, 183, 107),  # Dark Khaki
                            (176, 224, 230),  # Powder Blue
                            (255, 239, 213),  # Papaya Whip
                            (255, 222, 173),  # Navajo White
                            (85, 107, 47)     # Dark Olive Green
                        ]
                    else:
                        # Neutral undertone
                        return [
                            (240, 230, 140),  # Khaki
                            (255, 239, 213),  # Papaya Whip
                            (176, 196, 222),  # Light Steel Blue
                            (152, 251, 152),  # Pale Green
                            (210, 180, 140)   # Tan
                        ]
                else:
                    # Light/fair skin tones
                    if h < 0.1 or h > 0.9:
                        # Pink undertone
                        return [
                            (255, 228, 225),  # Misty Rose
                            (255, 250, 205),  # Lemon Chiffon
                            (224, 255, 255),  # Light Cyan
                            (221, 160, 221),  # Plum
                            (255, 239, 213)   # Papaya Whip
                        ]
                    else:
                        # Yellow/neutral undertone
                        return [
                            (255, 255, 224),  # Light Yellow
                            (255, 239, 213),  # Papaya Whip
                            (255, 222, 173),  # Navajo White
                            (176, 224, 230),  # Powder Blue
                            (255, 218, 185)   # Peach Puff
                        ]
            matching_colors = get_matching_colors(most_common)
            st.write("Here are some colors that pair well with your skin tone:")
            cols = st.columns(len(matching_colors))
            # Add session state for search
            if 'search_states' not in st.session_state:
                st.session_state['search_states'] = {}
            # Helper: map hex to color name for palette colors
            COLOR_NAME_MAP = {
                '#ffa07a': 'Light Salmon',
                '#ffdab9': 'Peach Puff',
                '#ffffe0': 'Light Yellow',
                '#4682b4': 'Steel Blue',
                '#ba55d3': 'Medium Orchid',
                '#ffd700': 'Gold',
                '#ffefd5': 'Papaya Whip',
                '#cd853f': 'Peru',
                '#483d8b': 'Dark Slate Blue',
                '#2e8b57': 'Sea Green',
                '#ffdead': 'Navajo White',
                '#ffb6c1': 'Light Pink',
                '#ffe4b5': 'Moccasin',
                '#3cb371': 'Medium Sea Green',
                '#d2b48c': 'Tan',
                '#bdb76b': 'Dark Khaki',
                '#b0e0e6': 'Powder Blue',
                '#556b2f': 'Dark Olive Green',
                '#f0e68c': 'Khaki',
                '#b0c4de': 'Light Steel Blue',
                '#98fb98': 'Pale Green',
                '#ffe4e1': 'Misty Rose',
                '#fffacd': 'Lemon Chiffon',
                '#e0ffff': 'Light Cyan',
                '#dda0dd': 'Plum',
                '#ffffe0': 'Light Yellow',
                '#ffebcd': 'Blanched Almond',
                '#faebd7': 'Antique White',
                '#fffaf0': 'Floral White',
                '#fff5ee': 'Seashell',
                '#fff0f5': 'Lavender Blush',
                '#ffe4c4': 'Bisque',
                '#ffebcd': 'Blanched Almond',
                '#ffe4b5': 'Moccasin',
                '#ffefd5': 'Papaya Whip',
                '#ffdab9': 'Peach Puff',
            }
            def hex_to_name(hex_color):
                return COLOR_NAME_MAP.get(hex_color.lower(), hex_color)
            for cidx, color in enumerate(matching_colors):
                hex_color = '#%02x%02x%02x' % color
                color_name = hex_to_name(hex_color)
                key = f'search_{idx}_{cidx}'
                with cols[cidx]:
                    if st.button(hex_color, key=key):
                        st.session_state['search_states'][key] = True
                    st.markdown(f'<div style="width:60px;height:60px;background:{hex_color};border-radius:8px;"></div>', unsafe_allow_html=True)
                    st.write(color_name)
                    # If swatch clicked, show search bar
                    if st.session_state['search_states'].get(key, False):
                        clothing = st.text_input(f"Search for {color_name} ...", key=f'input_{key}', placeholder="e.g. shoes, dress, shirt")
                        if clothing:
                            # Google Images search URL using color name
                            search_url = f"https://www.google.com/search?tbm=isch&q={color_name.replace(' ', '+')}+{clothing}"
                            st.markdown(f"[See {color_name} {clothing} on Google Images]({search_url})", unsafe_allow_html=True)
                        if st.button("Close", key=f'close_{key}'):
                            st.session_state['search_states'][key] = False
        else:
            st.write("Could not detect a dominant skin tone. Try another photo.")

if st.session_state['uploaded_images']:
    if st.button("Clear all uploaded photos"):
        st.session_state['uploaded_images'] = []
        st.experimental_rerun()
