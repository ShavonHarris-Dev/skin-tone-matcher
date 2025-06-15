import React, { useState } from 'react';
import { Button, Image, View, StyleSheet, ScrollView, Text, Platform } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system';
import * as ImageManipulator from 'expo-image-manipulator';

// Helper to get the average color by cropping to 1x1 pixel in the center
async function getCenterPixelColor(uri) {
  // Crop the center 50% region, then resize to 1x1
  const cropSize = 0.5; // 50% of the image
  const { width, height } = await ImageManipulator.getInfoAsync(uri);
  const cropWidth = width * cropSize;
  const cropHeight = height * cropSize;
  const originX = (width - cropWidth) / 2;
  const originY = (height - cropHeight) / 2;
  const manipResult = await ImageManipulator.manipulateAsync(
    uri,
    [
      { crop: { originX, originY, width: cropWidth, height: cropHeight } },
      { resize: { width: 1, height: 1 } }
    ],
    { compress: 1, format: ImageManipulator.SaveFormat.PNG, base64: true }
  );
  // The result is a 1x1 PNG, get the base64 and decode the RGB
  // Use expo-image-manipulator's result.uri and FileSystem.readAsStringAsync to get the raw PNG bytes
  const pngBytes = await FileSystem.readAsStringAsync(manipResult.uri, { encoding: FileSystem.EncodingType.Base64 });
  // Convert base64 to Uint8Array
  function base64ToUint8Array(base64) {
    const binary = atob(base64);
    const len = binary.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
      bytes[i] = binary.charCodeAt(i);
    }
    return bytes;
  }
  const bytes = base64ToUint8Array(pngBytes);
  // PNG: RGBA pixel data is usually at the end for a 1x1 PNG
  // Find the IEND chunk and read the 4 bytes before it
  let r = 128, g = 100, b = 80;
  for (let i = bytes.length - 8; i >= 0; i--) {
    // Look for IEND chunk
    if (
      bytes[i] === 73 && bytes[i + 1] === 69 && bytes[i + 2] === 78 && bytes[i + 3] === 68
    ) {
      // RGBA is usually 8 bytes before IEND
      r = bytes[i - 8];
      g = bytes[i - 7];
      b = bytes[i - 6];
      break;
    }
  }
  return [r, g, b];
}

async function analyzeSkinWithBackend(uri) {
  // Read the image as a base64 string
  const base64 = await FileSystem.readAsStringAsync(uri, { encoding: FileSystem.EncodingType.Base64 });
  // Convert to a blob for fetch (Expo workaround)
  const formData = new FormData();
  formData.append('image', {
    uri,
    name: 'photo.jpg',
    type: 'image/jpeg',
  });
  // Change the URL below to your backend's address
  const apiUrl = Platform.OS === 'android' ? 'http://10.0.2.2:5000/analyze-skin' : 'http://localhost:5000/analyze-skin';
  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      body: formData,
    });
    const data = await response.json();
    if (response.ok) {
      return data;
    } else {
      throw new Error(data.error || 'API error');
    }
  } catch (err) {
    return { error: err.message };
  }
}

export default function App() {
  const [images, setImages] = useState([]);
  // Store both dominant color and palette for each image
  const [colorResults, setColorResults] = useState([]); // [{skin_rgb: [r,g,b], palette: [[r,g,b], ...]}]

  // Request permissions on mount
  React.useEffect(() => {
    (async () => {
      if (Platform.OS !== 'web') {
        const { status: cameraStatus } = await ImagePicker.requestCameraPermissionsAsync();
        const { status: mediaStatus } = await ImagePicker.requestMediaLibraryPermissionsAsync();
        if (cameraStatus !== 'granted' || mediaStatus !== 'granted') {
          alert('Sorry, we need camera and media library permissions to make this work!');
        }
      }
    })();
  }, []);

  const processImage = async (uri) => {
    // Use backend API for skin tone detection
    const result = await analyzeSkinWithBackend(uri);
    if (result.error) {
      return { skin_rgb: [128, 100, 80], palette: [] };
    }
    // result.skin_rgb is [r, g, b], result.palette is [[r,g,b], ...]
    return { skin_rgb: result.skin_rgb, palette: result.palette || [] };
  };

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 1,
    });
    if (!result.canceled) {
      const uri = result.assets[0].uri;
      setImages([...images, uri]);
      const colorResult = await processImage(uri);
      setColorResults([...colorResults, colorResult]);
    }
  };

  const takePhoto = async () => {
    let result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      quality: 1,
    });
    if (!result.canceled) {
      const uri = result.assets[0].uri;
      setImages([...images, uri]);
      const colorResult = await processImage(uri);
      setColorResults([...colorResults, colorResult]);
    }
  };

  // Add a UI hint for the user
  const topLevelHint = (
    <Text style={{marginBottom: 10, color: '#555', textAlign: 'center'}}>
      Please center your skin in the photo for best results. The app will ignore background and lighting outliers.
    </Text>
  );

  return (
    <ScrollView contentContainerStyle={styles.container}>
      {topLevelHint}
      <Button title="Select a Photo from Gallery" onPress={pickImage} />
      <View style={{ height: 10 }} />
      <Button title="Take a Photo" onPress={takePhoto} />
      {images.map((img, idx) => (
        <View key={idx} style={styles.imageBlock}>
          <Image source={{ uri: img }} style={styles.image} />
          <Text>Uploaded Image {idx + 1}</Text>
          {colorResults[idx] && (
            <>
              <View style={{ flexDirection: 'row', alignItems: 'center', marginTop: 5 }}>
                <View style={{ width: 30, height: 30, backgroundColor: `rgb(${colorResults[idx].skin_rgb.join(',')})`, borderRadius: 5, marginRight: 8 }} />
                <Text style={{color: '#fff'}}>Dominant Color: rgb({colorResults[idx].skin_rgb.join(',')})</Text>
              </View>
              {colorResults[idx].palette && colorResults[idx].palette.length > 0 && (
                <View style={{ flexDirection: 'row', marginTop: 8 }}>
                  <Text style={{color: '#fff', marginRight: 8}}>Palette:</Text>
                  {colorResults[idx].palette.map((col, cidx) => (
                    <View key={cidx} style={{ width: 24, height: 24, backgroundColor: `rgb(${col.join(',')})`, borderRadius: 4, marginRight: 4, borderWidth: 1, borderColor: '#ccc' }} />
                  ))}
                </View>
              )}
            </>
          )}
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    padding: 20,
  },
  imageBlock: {
    marginTop: 20,
    alignItems: 'center',
  },
  image: {
    width: 200,
    height: 200,
    borderRadius: 10,
    marginBottom: 5,
  },
});
