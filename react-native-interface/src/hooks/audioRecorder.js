// npm install react-native-audio-recorder-player
import { useState } from 'react';
import AudioRecorderPlayer from 'react-native-audio-recorder-player';

const audioRecorderPlayer = new AudioRecorderPlayer();

const useAudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);

  const onStartRecord = async (path, audioSet) => {
    try {
      const result = await audioRecorderPlayer.startRecorder(path, audioSet);
      audioRecorderPlayer.addRecordBackListener((e) => {
        console.log('Recording progress:', e);
        return;
      });
      setIsRecording(true);
      console.log(result);
    } catch (error) {
      console.log('Failed to start recording:', error);
    }
  };

  const onStopRecord = async () => {
    try {
      const result = await audioRecorderPlayer.stopRecorder();
      audioRecorderPlayer.removeRecordBackListener();
      setIsRecording(false);
      console.log(result);
    } catch (error) {
      console.log('Failed to stop recording:', error);
    }
  };

  return {
    isRecording,
    onStartRecord,
    onStopRecord,
  };
};

export default useAudioRecorder;