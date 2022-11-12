import React from 'react';
import Modal from 'react-modal';
import $ from 'jquery';
import '../../css/App.css';
import Spinner from '../spinner';
import SendingPopup from './sending_popup';
import { actualResponse } from '../text_area';
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

function SendingModal() {

  const [modalIsOpen, setIsOpen] = React.useState(false);

  function openModal() {
    SendRequest(actualResponse);
    setIsOpen(true);
  }

  async function closeModal() {
    setIsOpen(false);
  }

  return (
    <div className="row send-data-container">
      <button type="button" id={'sendData'}
              className="btn btn-outline-secondary btn-lg btn-block actionButton w-100"
              onClick={openModal}>
        Send data
      </button>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        style={customStyles}
        id={'sendingModal'}
      >
        <div className="container-fluid" id={'modalBody'}>
          <div className="row d-flex justify-content-end Header">
            <div className="col-1" id={'sendingSpinner'}>
              <Spinner/>
            </div>
            <div className="col-10 d-flex justify-content-center">
              <h2><b>Response</b></h2>
            </div>
            <div className="col-1 d-flex justify-content-end">
              <i className="fa fa-arrow-left fa-2x settings-button hvr-fade" aria-hidden="true"
                 onClick={closeModal}></i>
            </div>
          </div>
          <SendingPopup/>
        </div>
      </Modal>
    </div>
  );
}

export default SendingModal;

$(document)
  .ready(function () {
    const object = document.getElementById('sendData');
    object.enabled = false;
    object.disabled = true;
  });

async function SendRequest(body) {
  let invoicesData = JSON.parse(body);
  console.log(invoicesData);
  let allResponses = {}
  for (let i = 0; i < invoicesData.length; i++){
    let singleInvoiceData = invoicesData[i];
    let key = Object.keys(singleInvoiceData)[0];
    let endpointResponse = await SendData(JSON.stringify(singleInvoiceData));
    let responseJson = await endpointResponse.json();
    allResponses[key] = JSON.parse(responseJson)
  }
  const responseTextfield = document.getElementById('response-host-text-field');
  responseTextfield.value = JSON.stringify(allResponses, null, 4);
  SwitchClasses('sendingSpinner', 'visible', 'hidden');
}

function SendData(body) {
  const url = 'http://localhost:5000/send_request';
  return fetch(url, {
    headers: {
      'Content-Type': 'application/json'
    },
    method: 'post',
    body: body
  });
}
