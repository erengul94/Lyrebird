import React from 'react';
import ReactQuill from 'react-quill'; // Import for a rich text editor
import 'react-quill/dist/quill.snow.css'; // Editor styles

function TextEditor() {
  const [content, setContent] = React.useState("");

  const handleChange = (value) => {
    setContent(value);
  };

  const handleSubmit = () => {
    if (content.trim() === "") {
      alert("Please enter some content before submitting.");
    } else {
      // Submit the content, for example, send it to a server or process it
      console.log("Note submitted:", content);
      alert("Note submitted successfully!");
      setContent(""); // Clear the editor after submission (optional)
    }
  };

  return (
    <div style={{ marginTop: '20px', textAlign: 'center' }}>
      <ReactQuill
        value={content}
        onChange={handleChange}
        placeholder="Start typing here..."
        style={{
          height: '200px',
          maxWidth: '100%',
          marginBottom: '20px', // Adds a gap between the editor and the button
          marginLeft: 'auto',
          marginRight: 'auto', // Centers the editor
        }}
      />
      <button
        onClick={handleSubmit}
        style={{
          backgroundColor: '#007bff',
          color: 'white',
          padding: '10px 20px',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          display: 'inline-block',
          marginTop: '20px', // Adds some gap between the editor and the button
        }}
      >
        Submit Note
      </button>
    </div>
  );
}

export default TextEditor;
