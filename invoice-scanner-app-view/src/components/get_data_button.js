import React from 'react';
import '../css/Button.css';
import { getFilesList } from './drag_and_drop';
import { FillAreaWithResponse } from './text_area';
import { SwitchClasses } from './common';
import { GetUpdatedJson } from './settings_modal/modal';

function GetDataButton() {
  return (
    <button className="button-4" id={"getDataButton"} disabled onClick={GetData}>Get data</button>
  );
}

export default GetDataButton;

let originalResponse = ""
export { originalResponse };

export async function GetData() {
  SwitchClasses('spinnerDiv', 'hidden', 'visible');
  const filesList = getFilesList();
  let json_data = "";
  try {
    const response = await getInvoiceData(filesList);
    if (response.ok) {
      json_data = await response.json();
    } else {
      json_data =  "Error: " + response.status + " " + response.body;
    }
  } catch (e) {
    json_data =  "Service unavailable.";
  }
  originalResponse = JSON.stringify(JSON.stringify(json_data));
  let updated_json = await GetUpdatedJson(originalResponse)
  FillAreaWithResponse(updated_json);
  SwitchClasses('spinnerDiv', 'visible', 'hidden');
}

function getInvoiceData(files) {
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
