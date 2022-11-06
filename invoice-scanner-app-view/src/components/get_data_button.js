import React from 'react';
import '../css/Button.css';
import { getFilesList } from './drag_and_drop';
import { fillAreaWithResponse } from './text_area';
import { SwitchClasses } from './common';

function GetDataButton() {
  return (
    <button className="button-4" id={"getDataButton"} disabled onClick={getData}>Get data</button>
  );
}

export default GetDataButton;

export async function getData() {
  SwitchClasses('spinnerDiv', 'hidden', 'visible')
  const filesList = getFilesList()
  let json_data = ""
  try {
    const response = await getInvoiceData(filesList);
    if (response.ok) {
      json_data = await response.json()
    } else {
      json_data =  "Error: " + response.status + " " + response.body
    }
  } catch (e) {
    json_data =  "Service unavailable.";
  }

  fillAreaWithResponse(json_data)
  SwitchClasses('spinnerDiv', 'visible', 'hidden')

}

function getInvoiceData(files) {
  console.log("Button clicked!")

  const url = 'http://localhost:5000/invoice'

  const fd = new FormData();
  for (const file of files) {
    fd.append('image', file)
  }

  return fetch(url, {
    method: 'post',
    body: fd
  });
}
