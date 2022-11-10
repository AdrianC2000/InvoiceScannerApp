import React from 'react';
import Modal from 'react-modal';
import SettingsPopup from './settings_popup';
import $ from 'jquery';
import { SetUrlConfiguration } from './url_options';
import { SetHeadersConfiguration } from './headers_options';
import { SetDataConfiguration } from './data_format';
import Spinner from '../spinner';

const customStyles = {
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)',
  },
};

Modal.setAppElement('#root');

function SettingsModal() {
  const [modalIsOpen, setIsOpen] = React.useState(false);

  function openModal() {
    InitModalValues()
    setIsOpen(true);
  }

  function closeModal() {
    setIsOpen(false);
  }

  return (
    <div>
      <i className="fa fa-cog fa-2x settings-button hvr-fade" id={"settings"} aria-hidden="true" onClick={openModal}></i>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        style={customStyles}
        contentLabel="Example Modal"
      >
        <div className="container-fluid" id={"modalBody"}>
          <div className="row d-flex justify-content-end Header">
            <div className="col-1" id={"settingsSpinner"}>
              <Spinner />
            </div>
            <div className="col-10 d-flex justify-content-center">
              <h2><b>Settings</b></h2>
            </div>
            <div className="col-1 d-flex justify-content-end">
              <i className="fa fa-arrow-left fa-2x settings-button hvr-fade" aria-hidden="true" onClick={closeModal}></i>
            </div>
          </div>
          <SettingsPopup />
        </div>
      </Modal>
    </div>
  );
}

export default SettingsModal;

export async function InitModalValues() {
  $(function () {
    $('[data-toggle="tooltip"]').tooltip() // Enabling tooltip in the whole modal
  })
  let jsonData = ""
  try {
    const response = await GetSettings();
    if (response.ok) {
      jsonData = await response.json()
    } else {
      jsonData =  "Error: " + response.status + " " + response.body
    }
  } catch (e) {
    jsonData =  "Service unavailable.";
  }
  FillFieldsWithResponse(jsonData)
  SetModalLoaded()
}

function GetSettings() {
  const url = 'http://localhost:5000/settings'
  return fetch(url, {
    method: 'get',
  });
}

function FillFieldsWithResponse(settings) {
  console.log(settings)
  let urlConfiguration = settings["url_configuration"]
  SetUrlConfiguration(urlConfiguration)
  let headersConfiguration = settings["headers_configuration"]
  SetHeadersConfiguration(headersConfiguration)
  let dataConfiguration = settings["data_configuration"]
  SetDataConfiguration(dataConfiguration)
}

function SetModalLoaded() {
  const endpointConfigurationDiv = document.getElementById("endpointConfigurationDiv");
  endpointConfigurationDiv.classList.remove("invisible");

  const removeNullsDiv = document.getElementById("removeNullsDiv");
  removeNullsDiv.classList.remove("invisible");

  const dataFormatDiv = document.getElementById("dataFormatDiv");
  dataFormatDiv.classList.remove("invisible");

  const settingsSpinnerDiv = document.getElementById("settingsSpinner")
  settingsSpinnerDiv.classList.add("invisible")
}
