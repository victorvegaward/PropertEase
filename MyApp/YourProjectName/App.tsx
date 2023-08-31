import React, { useState } from 'react';
import {
  SafeAreaView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
  Image,
  ImageBackground
} from 'react-native';

const App = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    // Handle login logic here.
    console.log('Login button pressed with username:', username);
  };

  return (
    <SafeAreaView style={styles.container}>
      <ImageBackground source={{ uri: 'https://imgur.com/okWXIxm.png' }} style={styles.backgroundImage}>
      {/* <Image
        style={styles.logo}
        source={{ uri: 'https://imgur.com/uksglDC.png' }} // Replace with your logo or a relevant image
      /> */}
      
      <Text style={styles.title}>PropertyEase</Text>
      <Text style={styles.subtitle}>Professional Property Management</Text>
      
      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
        placeholderTextColor="#aaa"
      />

      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        placeholderTextColor="#aaa"
      />

      <TouchableOpacity style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>Login</Text>
      </TouchableOpacity>
      </ImageBackground>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    backgroundColor: '#f5f5f5',
  },
  logo: {
    width: 200,  // Adjust as needed
    height: 200, // Adjust as needed
    resizeMode: 'contain', // This will ensure the image maintains its aspect ratio
    margin: 10 // Optional, for spacing around the image
  },
  title: {
    fontSize: 28,
    marginBottom: 5,
    color: '#333',
    fontWeight: 'bold',
  },
  subtitle: {
    fontSize: 14,
    marginBottom: 20,
    color: '#777',
  },
  input: {
    width: '100%',
    padding: 15,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 25,
    backgroundColor: '#fff',
    marginBottom: 10,
    fontSize: 16,
  },
  button: {
    width: '100%',
    padding: 15,
    borderRadius: 25,
    backgroundColor: '#007BFF',
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
  },
  backgroundImage: {
    flex: 1,
    resizeMode: 'cover', // or 'stretch'
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%', // ensure the background covers the whole screen
    height: '65%', // ensure the background covers the whole screen
  },
  
});

export default App;
