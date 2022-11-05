import React from 'react';

function TextArea() {
  return (
    <textarea className="scrollableTextBox" name="json_invoice" id={'response-text-field'}>
    </textarea>
  );
}

export default TextArea;

export function fillAreaWithResponse(response) {
  const textarea = document.getElementById('response-text-field');
  textarea.value = JSON.stringify(response, null, 4);
}
