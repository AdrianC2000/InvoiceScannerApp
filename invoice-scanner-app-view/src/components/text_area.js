import React from 'react';
import { EnableObject } from './common';

function TextArea() {
  return (
    <textarea className="scrollableTextBox" name="json_invoice" id={'response-text-field'} onChange={CheckContent}>
    </textarea>
  );
}

export default TextArea;

let actualResponse = ""
export { actualResponse };

export function FillAreaWithResponse(response) {
  const textarea = document.getElementById('response-text-field');
  textarea.value = JSON.stringify(response, null, 4);
  CheckContent()
}

function CheckContent() {
  const textarea = document.getElementById('response-text-field');
  actualResponse = textarea.value;
  if (textarea.value !== "") {
    EnableObject('sendData', true)
  } else {
    EnableObject('sendData', false)
  }
}
