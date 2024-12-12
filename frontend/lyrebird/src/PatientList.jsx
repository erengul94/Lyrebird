import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import {getPatients} from '../src/API/patientApi'
import { useNavigate } from 'react-router-dom';


function PatientList() {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [modalContent, setModalContent] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const _patients = async () => {
        console.log("patients fetch")
        const _patients = await getPatients(); 
        setPatients(_patients)
    };
    _patients();
}, []);

  const handleView = (patient) => {
    navigate(`/patientDetail?patientID=${patient.id}`)
  };

  const handleRecord = (patient) => {
    // setModalContent(`Recording data for patient: ${patient.name}`);
    // setShowModal(true);
    const url = `/createSession?patientID=${patient.id}`
    navigate(url)
  };

  const handleNotes = (patient) => {
    setModalContent(`Adding notes for patient: ${patient.name}`);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setModalContent("");
  };

  return (
    <div className="container mt-4">
      <h3>Patient List</h3>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Name</th>
            <th className="text-end">Actions</th>
          </tr>
        </thead>
        <tbody>
          {patients.map((patient) => (
            <tr key={patient.id} className={selectedPatient?.id === patient.id ? "table-primary" : ""}>
              <td>
                <button
                  className="btn btn-link text-decoration-none"
                  onClick={() => handleView(patient)}
                  aria-label={`View details of ${patient.name}`}
                >
                  {patient.first_name}
                </button>
              </td>
              <td className="text-end">
                <Button
                  variant="primary"
                  size="sm"
                  className="me-2"
                  onClick={() => handleRecord(patient)}
                >
                  Record
                </Button>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => handleNotes(patient)}
                >
                  Notes
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Modal for Actions */}
      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>Action</Modal.Title>
        </Modal.Header>
        <Modal.Body>{modalContent}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default PatientList;
