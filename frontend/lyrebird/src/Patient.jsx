import React, { useEffect, useState } from 'react';

import {getPatient} from '../src/API/patientApi'

function Patient() {
    const [patientInfo, setPatientInfo] = useState(null);
    const [sessions, setSessions] = useState([]);
  
    useEffect(() => {
      // Fetch patient info and sessions from the API
      async function fetchPatientData() {
        const response = await getPatient(1); // Replace with the actual patient ID
        const data = response
        setPatientInfo(data.patient);
        setSessions(data.sessions);
      }
  
      fetchPatientData();
    }, []);
  
    return (
      <div style={{ padding: '30px', maxWidth: '900px', margin: '0 auto', fontFamily: 'Arial, sans-serif' }}>
        {patientInfo ? (
          <>
            {/* Patient Information Section */}
            <div style={{ marginBottom: '40px' }}>
              <h1 style={{ color: '#4CAF50' }}>Patient Information</h1>
              <div style={{ marginBottom: '20px' }}>
                <h2>{patientInfo.first_name} {patientInfo.last_name}</h2>
                <p><strong>Phone:</strong> {patientInfo.phone_number}</p>
                <p><strong>Email:</strong> {patientInfo.email}</p>
                <p><strong>Address:</strong> {patientInfo.address}</p>
              </div>
            </div>
  
            {/* Sessions Section */}
            <div>
              <h2 style={{ color: '#4CAF50' }}>Sessions</h2>
              {sessions.length > 0 ? (
                <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
                  <thead>
                    <tr>
                      <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'left' }}>Session ID</th>
                      <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'left' }}>Date</th>
                      <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'left' }}>Description</th>
                      <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'left' }}>Recording</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sessions.map((session) => (
                      <tr key={session.id}>
                        <td style={{ padding: '12px', border: '1px solid #ddd' }}>{session.id}</td>
                        <td style={{ padding: '12px', border: '1px solid #ddd' }}>{new Date(session.started_at).toLocaleString()}</td>
                        <td style={{ padding: '12px', border: '1px solid #ddd' }}>{session.description}</td>
                        <td style={{ padding: '12px', border: '1px solid #ddd' }}>
                        {session.record_url ? (
                          <audio controls>
                            <source src={session.record_url} type="audio/wav" />
                            Your browser does not support the audio element.
                          </audio>
                        ) : (
                          <span>No recording available</span>
                        )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <p style={{ marginTop: '20px', fontStyle: 'italic' }}>No sessions found for this patient.</p>
              )}
            </div>
          </>
        ) : (
          <p>Loading patient information...</p>
        )}
      </div>
    );
  }
    

export default Patient;
