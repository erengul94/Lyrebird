import React from "react";
import { Container, Navbar, Nav, Button } from "react-bootstrap";
import { BrowserRouter, Routes, Route } from 'react-router-dom'

import PatientList from "./PatientList";
import MainLayout from "./MainLayout";
import CreateSession from "./SessionPage/CreateSession";

import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import Patient from "./Patient";
import LoginPage from "./Login";

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route element={<LoginPage />} >
            <Route path="/" >
              <Route index element={<PatientList />} />
              <Route path="createSession" element={<CreateSession />} />
              <Route path="patientDetail" element={<Patient />} />

            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
