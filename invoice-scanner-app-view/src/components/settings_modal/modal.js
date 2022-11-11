import React from 'react';
import Modal from 'react-modal';
import { originalResponse } from '../get_data_button'
import SettingsPopup from './settings_popup';
import $ from 'jquery';
import { GetUrlConfiguration, SetUrlConfiguration } from './url_options';
import { GetHeadersConfiguration, SetHeadersConfiguration } from './headers_options';
import { GetDataConfiguration, SetDataConfiguration } from './data_format';
import Spinner from '../spinner';
import { FillAreaWithResponse } from '../text_area';
import { SwitchClasses } from '../common';

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
    InitModalValues();
    setIsOpen(true);
  }

  async function closeModal() {
    setIsOpen(false);
    let response = await SaveSettings();
    switch (response) {
      case 200:
        if (originalResponse !== "") {
          SwitchClasses('spinnerDiv', 'hidden', 'visible');
          const updatedJson = await GetUpdatedJson(originalResponse)
          FillAreaWithResponse(updatedJson);
          SwitchClasses('spinnerDiv', 'visible', 'hidden');
        }
        break;
      case 304:
        console.log(`Settings unchanged`); //
        break;
      default:
        console.log(`Something went wrong...`); // Display error info here
    }
  }

  return (
    <div>
      <i className="fa fa-cog fa-2x settings-button hvr-fade" id={'settings'} aria-hidden="true"
         onClick={openModal}></i>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        style={customStyles}
        contentLabel="Example Modal"
      >
        <div className="container-fluid" id={'modalBody'}>
          <div className="row d-flex justify-content-end Header">
            <div className="col-1" id={'settingsSpinner'}>
              <Spinner/>
            </div>
            <div className="col-10 d-flex justify-content-center">
              <h2><b>Settings</b></h2>
            </div>
            <div className="col-1 d-flex justify-content-end">
              <i className="fa fa-arrow-left fa-2x settings-button hvr-fade" aria-hidden="true"
                 onClick={closeModal}></i>
            </div>
          </div>
          <SettingsPopup/>
        </div>
      </Modal>
    </div>
  );
}

export default SettingsModal;

export async function InitModalValues() {
  $(function () {
    $('[data-toggle="tooltip"]')
      .tooltip(); // Enabling tooltip in the whole modal
  });
  let jsonData = '';
  try {
    const response = await GetSettings();
    if (response.ok) {
      jsonData = await response.json();
    } else {
      jsonData = 'Error: ' + response.status + ' ' + response.body;
    }
  } catch (e) {
    jsonData = 'Service unavailable.';
  }
  FillFieldsWithResponse(jsonData);
  SetModalLoaded();
}

function GetSettings() {
  const url = 'http://localhost:5000/settings';
  return fetch(url, {
    method: 'get',
  });
}

function FillFieldsWithResponse(settings) {
  console.log('Settings: ' + settings);
  let urlConfiguration = settings['url_configuration'];
  SetUrlConfiguration(urlConfiguration);
  let headersConfiguration = settings['headers_configuration'];
  SetHeadersConfiguration(headersConfiguration);
  let dataConfiguration = settings['data_configuration'];
  SetDataConfiguration(dataConfiguration);
}

function SetModalLoaded() {
  const endpointConfigurationDiv = document.getElementById('endpointConfigurationDiv');
  endpointConfigurationDiv.classList.remove('invisible');

  const removeNullsDiv = document.getElementById('removeNullsDiv');
  removeNullsDiv.classList.remove('invisible');

  const dataFormatDiv = document.getElementById('dataFormatDiv');
  dataFormatDiv.classList.remove('invisible');

  const settingsSpinnerDiv = document.getElementById('settingsSpinner');
  settingsSpinnerDiv.classList.add('invisible');
}

async function SaveSettings() {
  const configuration = {};
  configuration['url_configuration'] = GetUrlConfiguration();
  configuration['headers_configuration'] = GetHeadersConfiguration();
  configuration['data_configuration'] = GetDataConfiguration();
  let response = await SetSettings(JSON.stringify(configuration));
  try {
    if (response.status === 200 || response.status === 304) {
      return response.status
    } else {
      return 'Error: ' + response.status + ' ' + response.body;
    }
  } catch (e) {
    return "Service unavailable.";
  }
}

function SetSettings(settings) {
  const url = 'http://localhost:5000/settings';
  return fetch(url, {
    headers: {
      'Content-Type': 'application/json'
    },
    method: 'post',
    body: settings
  });
}

export async function GetUpdatedJson(json) {
  let jsonData = '';
  try {
    const response = await GetCustomizedJson(json);
    if (response.ok) {
      jsonData = await response.json();
    } else {
      jsonData = 'Error: ' + response.status + ' ' + response.body;
    }
  } catch (e) {
    jsonData = 'Service unavailable.';
  }
  return jsonData
}

function GetCustomizedJson(json) {
  const url = 'http://localhost:5000/customize_json';
  return fetch(url, {
    headers: {
      'Content-Type': 'application/json'
    },
    method: 'post',
    body: json
  });
}
