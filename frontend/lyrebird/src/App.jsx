import { Container, Navbar, Nav, Button } from "react-bootstrap";
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import React, { useState, useEffect } from "react";


import PatientList from "./PatientList";
import MainLayout from "./MainLayout";
import CreateSession from "./SessionPage/CreateSession";

import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import Patient from "./Patient";
import LoginPage from "./Login";
import { getUserInfo } from "./API/userApi";

function App() {
  // const [user, setUser] = useState("");
  const [authenticated, setAuthenticated] = useState(false);

  // useEffect(() => {
  //   const checkAuth = async () => {
  //     try {
  //       const user = await getUserInfo(); // current authenticated user
  //       setUser(user)
  //       setAuthenticated(true);
  //     }
  //     catch (err) {
  //       console.log("Dont worry just you logged out")
  //       setUser("");
  //       setAuthenticated(false);
  //     }
  //   };
  //   checkAuth();
  // }, []);

  return (
      <BrowserRouter>
        <Routes>
          <Route element={ <MainLayout />} >
            <Route path="/" >
              <Route index element={<LoginPage setAuthenticated={setAuthenticated} /> } />
              <Route path="createSession" element={ authenticated ? <CreateSession /> : <LoginPage setAuthenticated={setAuthenticated} /> } />
              <Route path="patientDetail" element={authenticated ? <Patient /> : <LoginPage setAuthenticated={setAuthenticated} />} />
              <Route path="patients" element={authenticated ? <PatientList /> : <LoginPage setAuthenticated={setAuthenticated} />} />

            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
  );
}

export default App;
