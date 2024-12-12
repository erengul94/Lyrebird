import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';


import {getPatient} from '../src/API/patientApi'

function Patient() {
    const [patientInfo, setPatientInfo] = useState(null);
    const [sessions, setSessions] = useState([]);

    const [params, setParams] = useSearchParams();


    const patientID = params.size ? params.get('patientID') : null; // in the edit mode

  
    useEffect(() => {
      // Fetch patient info and sessions from the API
      async function fetchPatientData() {
        const response = await getPatient(patientID); 
        const data = response
        setPatientInfo(data.patient);
        setSessions(data.sessions);
      }
  
      fetchPatientData();
    }, []);
  
    return (
        <div
          style={{
            padding: '30px',
            maxWidth: '900px',
            margin: '0 auto',
            fontFamily: 'Arial, sans-serif',
          }}
        >
          {patientInfo ? (
            <>
              {/* Patient Information Section */}
              <div style={{ marginBottom: '40px' }}>
                <h1 style={{ color: '#4CAF50' }}>Patient Information</h1>
                <div style={{ marginBottom: '20px' }}>
                  <h2>
                    {patientInfo.first_name} {patientInfo.last_name}
                  </h2>
                  <p>
                    <strong>Phone:</strong> {patientInfo.phone_number}
                  </p>
                  <p>
                    <strong>Email:</strong> {patientInfo.email}
                  </p>
                  <p>
                    <strong>Address:</strong> {patientInfo.address}
                  </p>
                </div>
              </div>
    
              {/* Sessions Section */}
              <div>
                <h2 style={{ color: '#4CAF50' }}>Sessions</h2>
                {console.log("Sessions")}
                {console.log(sessions)}

                {sessions.length > 0 ? (
                  <table
                    style={{
                      width: '100%',
                      borderCollapse: 'collapse',
                      marginTop: '20px',
                    }}
                  >
                    <thead>
                      <tr>
                        <th
                          style={{
                            padding: '12px',
                            border: '1px solid #ddd',
                            textAlign: 'left',
                          }}
                        >
                          Session ID
                        </th>
                        <th
                          style={{
                            padding: '12px',
                            border: '1px solid #ddd',
                            textAlign: 'left',
                          }}
                        >
                          Date
                        </th>
                        <th
                          style={{
                            padding: '12px',
                            border: '1px solid #ddd',
                            textAlign: 'left',
                          }}
                        >
                          Description
                        </th>
                        <th
                          style={{
                            padding: '12px',
                            border: '1px solid #ddd',
                            textAlign: 'left',
                          }}
                        >
                          Recording
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {sessions.map((session) => (
                        <React.Fragment key={session.session_id}>
                          <tr>
                            <td
                              style={{
                                padding: '12px',
                                border: '1px solid #ddd',
                              }}
                            >
                              {session.id}
                            </td>
                            <td
                              style={{
                                padding: '12px',
                                border: '1px solid #ddd',
                              }}
                            >
                              {new Date(session.started_at).toLocaleString()}
                            </td>
                            <td
                              style={{
                                padding: '12px',
                                border: '1px solid #ddd',
                              }}
                            >
                              {session.description}
                            </td>
                            <td
                              style={{
                                padding: '12px',
                                border: '1px solid #ddd',
                              }}
                            >
                              {session.record_url ? (
                                <audio controls>
                                  <source
                                    src={session.record_url}
                                    type="audio/wav"
                                  />
                                  Your browser does not support the audio element.
                                </audio>
                              ) : (
                                <span>No recording available</span>
                              )}
                            </td>
                          </tr>
                          {/* Additional Notes */}
                          <tr>
                            <td
                              colSpan={4}
                              style={{
                                padding: '12px',
                                border: '1px solid #ddd',
                                backgroundColor: '#f9f9f9',
                              }}
                            >
                              <strong>Doctor's Notes:</strong>{' '}
                              {session.note || 'No notes available'}
                              <br />
                              <strong>Recording Notes:</strong>{' '}
                              {session.recording_notes || 'No notes available'}
                            </td>
                          </tr>
                        </React.Fragment>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <p
                    style={{
                      marginTop: '20px',
                      fontStyle: 'italic',
                    }}
                  >
                    No sessions found for this patient.
                  </p>
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

