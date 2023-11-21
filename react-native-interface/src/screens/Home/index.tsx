import React from 'react';
import { Text, View, TouchableOpacity, Image } from 'react-native';
import { styles } from './styles';
import useAudioRecorder from '../hooks/AudioRecorder'; // Certifique-se de que o caminho esteja correto

export function Home() {
  const { isRecording, onStartRecord, onStopRecord } = useAudioRecorder();

  // Define o caminho para salvar o arquivo de áudio e a configuração do áudio
  const audioPath = 'hello.m4a';
  const audioSet = {
    // Sua configuração de áudio vai aqui
  };

  const handlePress = () => {
    if (isRecording) {
      onStopRecord();
    } else {
      onStartRecord(audioPath, audioSet);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.eventName}>
        MATCH
      </Text>

      <Text style={styles.eventDate}>
        Shazam diretamente da Shopee
      </Text>

      <Text style={styles.pressText}>
        Tap to Match
      </Text>

      <TouchableOpacity onPress={handlePress}>
        <View style={styles.shadowContainer}>
          <Image source={require('./../../foto.jpeg')} style={styles.image}/>
          {isRecording && <View style={styles.recordingOverlay}>
            <Text style={styles.recordingText}>Gravando...</Text>
          </View>}
        </View>
      </TouchableOpacity>
      
      <Text style={styles.joke}>
        Não é tinder, mas sempre temos um match para você!
      </Text>  
    </View>
  );