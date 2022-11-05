import React from 'react';
import './css/App.css';
import List from './components/list';
import DragAndDrop from './components/drag_and_drop';
import GetDataButton from './components/get_data_button';
import TextArea from './components/text_area';

function App() {
  return (
    <body>
      <div className="container-fluid">
        <div className="row justify-content-center no-gutters Header">
          <h2><b>Invoice Scanner App</b></h2>
        </div>
        <div className="row no-gutters Data-container">
          <div className="col-md-5 data_column">
            <div className="col-md-11 big_inner_column">
              <div className="row justify-content-center no-gutters Header" id="uploadInvoice">
                <p><b>Upload your invoices</b></p>
              </div>
              <div className="row justify-content-center no-gutters" id="dropBox">
                <DragAndDrop />
              </div>
              <div className="row justify-content-center no-gutters overflow-auto" id="filesList">
                <List />
              </div>
            </div>
          </div>
          <div className="col-md-2 data_column">
            <div className="col-md-11 center-block inner_column" id="buttonDiv">
              <GetDataButton />
            </div>
          </div>
          <div className="col-md-5 data_column">
            <div className="col-md-11 big_inner_column">
              <div className="row justify-content-center no-gutters Header">
                <p><b>Invoice data</b></p>
              </div>
              <div className="row justify-content-center no-gutters Data-container">
                <TextArea />
              </div>
            </div>
          </div>
        </div>
      </div>
    </body>
  );
}

export default App;
