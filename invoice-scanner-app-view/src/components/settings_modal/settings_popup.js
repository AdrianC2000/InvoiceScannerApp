import React from 'react';
import '../../css/Button.css';
import EndpointConfiguration from './endpoint_configuration';
import JsonFieldList from './json_field_list';

function SettingsPopup() {
  return (
    <div className="row no-gutters Data-container">
      <div className="col-md-6 data_column">
        <div className="col-md-11 big_inner_column">
          <div className="row justify-content-center no-gutters Header" id="uploadInvoice">
            <p><b>Endpoint configuration</b></p>
          </div>
          <div className="row justify-content-center no-gutters Data-container">
            <EndpointConfiguration />
          </div>
        </div>
      </div>
      <div className="col-md-6 data_column">
        <div className="col-md-11 big_inner_column">
          <div className="row d-flex justify-content-end Header">
            <div className="col-1">
            </div>
            <div className="col-10 d-flex justify-content-center">
              <p><b>Data format configuration</b></p>
            </div>
            <div className="col-1 d-flex justify-content-end">
              <i className="fa fa-info-circle fa-2x" data-toggle="tooltip" data-placement="top"
                 title="Leave the box unchecked if you don't want the key to be included in the final json"
                 aria-hidden="true"></i>
            </div>
          </div>
          <div className="row form-check">
            <input className="form-check-input" type="checkbox" value="" id="remove_nulls"/>
            <label className="form-check-label" htmlFor="removeNullsCheck">
              Remove nulls
            </label>
          </div>
          <div className="row justify-content-center overflow-auto sub-data-container">
            <JsonFieldList />
          </div>
        </div>
      </div>
    </div>
  );
}

export default SettingsPopup;
