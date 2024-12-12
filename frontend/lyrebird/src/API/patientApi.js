
import { axiosInstance } from "./utils";

const APIURL = 'http://localhost:8000';


async function getPatients() {
    const url = 'patients';
    const accessToken = JSON.parse(localStorage.getItem("user"))['access']

    try {
        const response = await axiosInstance.get(url, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
        if (response) {
            // process the response
            const patients = response.data
            console.log(response.data)
            console.log("Patients retreived")
            // // console.log(pages)
            return patients;
        } else {
            // application error (404, 500, ...)
            const text = await response.text();
            throw new TypeError(text);
        }
    } catch (ex) {
        // network error
        throw ex;
    }
}


async function getPatient(patientID) {

    const url =`patient/${patientID}`;
    console.log("Patient retreived")

    const accessToken = JSON.parse(localStorage.getItem("user"))['access']
    
    try {
        const response = await axiosInstance.get(url,
        {    
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
        // console.log(response);

        if (response) {
            // process the response
            const patient = await response.data;
            // console.log(patient)
            return patient;
        } else {
            // application error (404, 500, ...)
            const text = await response.text();
            throw new TypeError(text);
        }
    } catch (ex) {
        // network error
        throw ex;
    }
}


export {getPatients, getPatient};