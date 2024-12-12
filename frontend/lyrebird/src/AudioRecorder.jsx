import React, { useState, useRef } from 'react';
import './App.css'; // Import CSS for animation
import { recordSession } from '../src/API/sessionApi';

const VoiceRecorder = (props) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);  // State to track pause status
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
      setIsPaused(false);  // Reset the pause state
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

  const pauseRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.pause();
      setIsPaused(true);  // Set pause state to true
    }
  };

  const resumeRecording = () => {
    if (mediaRecorderRef.current && isPaused) {
      mediaRecorderRef.current.resume();
      setIsPaused(false);  // Set pause state to false
    }
  };

  const submitAudio = async () => {
    if (!audioBlob) {
      alert('No audio recorded to submit!');
      return;
    }
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');
    await recordSession(formData, props.patientID);
  };

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h2>Voice Recorder</h2>
      {isRecording ? (
        <div>
          {isPaused ? (
            <button
              onClick={resumeRecording}
              className="pulsing-button"
            >
              Resume Recording
            </button>
          ) : (
            <button
              onClick={pauseRecording}
              className="pulsing-button"
            >
              Pause Recording
            </button>
          )}
          <button
            onClick={stopRecording}
            className="pulsing-button"
          >
            Stop Recording
          </button>
        </div>
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
