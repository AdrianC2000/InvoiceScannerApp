import React from 'react';
import './css/App.css';
import List from './components/list';
import DragAndDrop from './components/drag_and_drop';
import GetDataButton from './components/get_data_button';
import TextArea from './components/text_area';
import Spinner from './components/spinner';
import SettingsModal from './components/settings_modal/settings_modal.js';
import SendingModal from './components/sending_modal/sending_modal';

function App() {
  return (
    <body>
    <div className="container-fluid" id={'root'}>
      <div className="row d-flex justify-content-end Header">
        <div className="col-1">
        </div>
        <div className="col-10 d-flex justify-content-center">
          <h2><b>Invoice Scanner App</b></h2>
        </div>
        <div className="col-1 d-flex justify-content-end">
          <SettingsModal/>
        </div>
      </div>
      <div className="row no-gutters Data-container">
        <div className="col-md-5 data_column">
          <div className="col-md-11 big_inner_column">
            <div className="row justify-content-center no-gutters Header" id="uploadInvoice">
              <p><b>Upload your invoices</b></p>
            </div>
            <div className="row justify-content-center no-gutters" id="dropBox">
              <DragAndDrop/>
            </div>
            <div className="row justify-content-center no-gutters overflow-auto" id="filesList">
              <List id={'invoices-list'}/>
            </div>
          </div>
        </div>
        <div className="col-md-2 data_column d-flex align-items-center justify-content-center">
          <div className="col-md-11 center-block inner_column">
            <div className={'row no-gutters color'} id="buttonDiv">
              <GetDataButton/>
            </div>
            <div id={'spinnerDiv'} className={'hidden'}>
              <Spinner/>
            </div>
          </div>
        </div>
        <div className="col-md-5 data_column">
          <div className="col-md-11 big_inner_column">
            <div className="row justify-content-center no-gutters Header">
              <p><b>Invoice data</b></p>
            </div>
            <div className="row justify-content-center Data-container">
              <div className="col-md-11">
                <div className="row json-field-container">
                  <TextArea/>
                </div>
                <SendingModal/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </body>
  );
}

export default App;
