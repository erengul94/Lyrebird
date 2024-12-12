import { axiosInstance } from "./utils";

const APIURL = 'http://localhost:8000';


async function recordSession(formData, patientID) {
    console.log("record session triggered");
    const url = APIURL + `/createSession/`;
    console.log(url);
    const accessToken = JSON.parse(localStorage.getItem("user"))['access']
    formData.append("patientID", patientID);
    try {

        console.log(formData)
        const response = await axiosInstance.post(url, formData, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
            body: formData
          });
        
        if (response) {
          alert('Audio successfully uploaded!');
        } else {
          const error = await response.text();
          alert(`Error uploading audio: ${error}`);
        }
      } catch (error) {
        console.error('Error uploading audio:', error);
      }
    };    




export {recordSession}