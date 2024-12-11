import React from 'react';
import TextEditor from '../TextEditor';
import VoiceRecorder from '../AudioRecorder';
import '../App.css'; // Move styles here for cleaner code

function CreateSession() {
  return (
    <div className="page-container">
      <div className="content-container">
        <header className="header">
          <p>Record audio and take notes efficiently.</p>
        </header>

        <section className="section">
          <VoiceRecorder />
        </section>

        <section className="section">
          <h2>Text Editor</h2>
          <TextEditor />
        </section>
      </div>
    </div>
  );
}

export default CreateSession;
