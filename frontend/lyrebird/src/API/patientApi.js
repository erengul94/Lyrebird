const APIURL = 'http://localhost:8000';


async function getPatients() {
    const url = APIURL + '/patients';
    console.log("Patients retreived")

    try {
        const response = await fetch(url);
        if (response.ok) {
            // process the response
            const patients = await response.json();
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
    const url = APIURL + '/patient/' + patientID;
    console.log("Patient retreived")

    try {
        const response = await fetch(url);
        // console.log(response);

        if (response.ok) {
            // process the response
            const patient = await response.json();
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