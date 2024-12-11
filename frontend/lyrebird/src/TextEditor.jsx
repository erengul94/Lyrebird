import React from 'react';
import ReactQuill from 'react-quill'; // Import for a rich text editor
import 'react-quill/dist/quill.snow.css'; // Editor styles

function TextEditor() {
  const [content, setContent] = React.useState("");

  const handleChange = (value) => {
    setContent(value);
  };

  return (
    <div style={{ marginTop: '20px' }}>
    <ReactQuill
      value={content}
      onChange={handleChange}
      placeholder="Start typing here..."
      style={{
        height: '200px', 
        maxWidth: '100%',
        marginBottom: '20px',
      }}
    />
  </div>
  );
}


export default TextEditor;