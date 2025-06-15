import React, { useState } from 'react';
import { Button, Image, View, StyleSheet, ScrollView, Text, Platform } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

export default function App() {
  const [images, setImages] = useState([]);

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

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 1,
    });
    if (!result.canceled) {
      setImages([...images, result.assets[0].uri]);
    }
  };

  const takePhoto = async () => {
    let result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      quality: 1,
    });
    if (!result.canceled) {
      setImages([...images, result.assets[0].uri]);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Button title="Select a Photo from Gallery" onPress={pickImage} />
      <View style={{ height: 10 }} />
      <Button title="Take a Photo" onPress={takePhoto} />
      {images.map((img, idx) => (
        <View key={idx} style={styles.imageBlock}>
          <Image source={{ uri: img }} style={styles.image} />
          <Text>Uploaded Image {idx + 1}</Text>
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
