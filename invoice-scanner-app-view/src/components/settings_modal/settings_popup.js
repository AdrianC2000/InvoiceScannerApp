import React from 'react';
import 'jquery-ui-bundle';
import 'jquery-ui-bundle/jquery-ui.css';
import '../../css/Button.css';
import EndpointConfiguration from './endpoint_configuration';
import DataFormat from './data_format';

function SettingsPopup() {
  return (
    <div className="row no-gutters Data-container">
      <div className="col-md-6 data_column">
        <div className="col-md-11 big_inner_column">
          <div className="row justify-content-center no-gutters Header" id="uploadInvoice">
            <p><b>Endpoint configuration</b></p>
          </div>
          <div className="row justify-content-center no-gutters Data-container invisible" id={"endpointConfigurationDiv"}>
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
                 title="Check box next to the attribute if you want it to be included in the final json."
                 aria-hidden="true"></i>
            </div>
          </div>
          <div className="row form-check invisible" id={"removeNullsDiv"}>
            <div className={"row"}>
              <div className={"col-6"}>
                <input className="form-check-input cursor-on-hover" type="checkbox" value="" id="remove_nulls"/>
                <label className="form-check-label cursor-on-hover" htmlFor="remove_nulls">
                  Remove nulls
                </label>
              </div>
              <div className={"col-6"}>
                <input className="form-check-input cursor-on-hover" type="checkbox" value="" id="convert_to_cents"/>
                <label className="form-check-label cursor-on-hover" htmlFor="convert_to_cents" data-toggle="tooltip" data-placement="top"
                       title="Check this box if you want to change every amount value into smaller unit, e.g. dollars into cents.">
                  Convert to cents
                </label>
              </div>
            </div>
            <div className={"row"}>
              <div className={"col-6"}>
                <input className="form-check-input cursor-on-hover" type="checkbox" value="" id="remove_percentage"/>
                <label className="form-check-label cursor-on-hover" htmlFor="remove_percentage" data-toggle="tooltip" data-placement="top"
                       title='Check this box if you want to remove the "%" sign from the VAT attribute.' >
                  Remove <q>%</q> sign
                </label>
              </div>
              <div className={"col-6"}>
                <input className="form-check-input cursor-on-hover" type="checkbox" value="" id="convert_currency"/>
                <label className="form-check-label cursor-on-hover" htmlFor="convert_currency" data-toggle="tooltip" data-placement="top"
                       title="Check this box if you want to change the currency for the one defined in ISO 4217, e.g. zł -> PLN. If conversion fails the value will not be changed.">
                  Convert currency
                </label>
              </div>
            </div>
          </div>
          <div className="row justify-content-center overflow-auto sub-data-container invisible" id={"dataFormatDiv"}>
            <DataFormat />
          </div>
        </div>
      </div>
    </div>
  );
}

export default SettingsPopup;
