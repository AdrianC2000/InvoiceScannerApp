import React from 'react';
import '../css/Button.css';
import { getFilesList } from './drag_and_drop';
import { fillAreaWithResponse } from './text_area';

function GetDataButton() {
  return (
    <button className="button-4" onClick={getData}>Get data</button>
  );
}

export default GetDataButton;

async function getData() {
  const filesList = getFilesList()
  const first_file = filesList[0]
  const response = await getInvoiceData(first_file);
  let json_data = await response.json();
  console.log(json_data)
  fillAreaWithResponse(json_data)
}

function getInvoiceData(file) {
  console.log("Button clicked!")

  const url = 'http://localhost:5000/invoice'

  const fd = new FormData();
  fd.append('image', file)

  return fetch(url, {
    method: 'post',
    body: fd
  });
}
