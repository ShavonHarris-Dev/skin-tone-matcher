from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
from collections import Counter
import colorsys

app = Flask(__name__)

@app.route('/analyze-skin', methods=['POST'])
def analyze_skin():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    image = Image.open(file.stream)
    small_image = image.resize((50, 50))
    pixels = list(small_image.getdata())
    filtered_pixels = [p for p in pixels if isinstance(p, tuple) and len(p) >= 3 and 30 < p[0] < 230 and 30 < p[1] < 230 and 30 < p[2] < 230]
    if not filtered_pixels:
        return jsonify({'error': 'Could not detect a dominant skin tone'}), 400
    most_common = Counter(filtered_pixels).most_common(1)[0][0]
    r, g, b = [x / 255.0 for x in most_common]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    # Use same color matching logic as your Streamlit app
    if l < 0.3:
        if h < 0.1 or h > 0.9:
            palette = [
                (255, 160, 122), (255, 218, 185), (255, 255, 224), (70, 130, 180), (186, 85, 211)
            ]
        else:
            palette = [
                (255, 215, 0), (255, 239, 213), (205, 133, 63), (72, 61, 139), (46, 139, 87)
            ]
    elif l < 0.6:
        if h < 0.15:
            palette = [
                (255, 222, 173), (255, 182, 193), (255, 228, 181), (60, 179, 113), (210, 180, 140)
            ]
        elif h > 0.6:
            palette = [
                (189, 183, 107), (176, 224, 230), (255, 239, 213), (255, 222, 173), (85, 107, 47)
            ]
        else:
            palette = [
                (240, 230, 140), (255, 239, 213), (176, 196, 222), (152, 251, 152), (210, 180, 140)
            ]
    else:
        if h < 0.1 or h > 0.9:
            palette = [
                (255, 228, 225), (255, 250, 205), (224, 255, 255), (221, 160, 221), (255, 239, 213)
            ]
        else:
            palette = [
                (255, 255, 224), (255, 239, 213), (255, 222, 173), (176, 224, 230), (255, 218, 185)
            ]
    return jsonify({
        'skin_rgb': most_common,
        'palette': [f'#{r:02x}{g:02x}{b:02x}' for r, g, b in palette]
    })

if __name__ == '__main__':
    app.run(debug=True)
