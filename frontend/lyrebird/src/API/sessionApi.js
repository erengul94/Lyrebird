const APIURL = 'http://localhost:8000';


async function recordSession(formData) {
    console.log("record session triggered");
    const url = APIURL + '/createSession/';
    console.log(url);

    try {
        const response = await fetch(url, {
          method: 'POST',
          body: formData,
        });
        
        if (response.ok) {
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