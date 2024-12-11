import React, { useState, useRef } from 'react';
import './App.css'; // Import CSS for animation
import {recordSession} from '../src/API/sessionApi';
 
const VoiceRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunks = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(audioChunks.current, { type: 'audio/wav' });
        const url = URL.createObjectURL(blob);
        setAudioURL(url);
        setAudioBlob(blob);
        audioChunks.current = [];
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const submitAudio = async () => {
    if (!audioBlob) {
      alert('No audio recorded to submit!');
      return;
    }
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');
    await recordSession(formData);
    
  };

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h2>Voice Recorder</h2>
      {isRecording ? (
        <button
          onClick={stopRecording}
          className="pulsing-button"
        >
          Stop Recording
        </button>
      ) : (
        <button
          onClick={startRecording}
          style={{
            backgroundColor: 'green',
            color: 'white',
            padding: '10px 20px',
          }}
        >
          Start Recording
        </button>
      )}
      {audioURL && (
        <div style={{ marginTop: '20px' }}>
          <h3>Recorded Audio:</h3>
          <audio controls src={audioURL}></audio>
          <a href={audioURL} download="recording.wav" style={{ display: 'block', marginTop: '10px' }}>
            Download Audio
          </a>
          <button
            onClick={submitAudio}
            style={{
              marginTop: '20px',
              backgroundColor: '#007bff',
              color: 'white',
              padding: '10px 20px',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
            }}
          >
            Submit Audio
          </button>
        </div>
      )}
    </div>
  );
};

export default VoiceRecorder;
