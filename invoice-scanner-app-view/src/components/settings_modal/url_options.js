import React from 'react';
import { EnableObject } from '../common';

function UrlOptions() {
  return (
    <div className={'container url-options'}>
      <div className="row d-flex justify-content-end sub-header">
        <div className="col-12 d-flex justify-content-center">
          <h4><b>URL</b></h4>
        </div>
      </div>
      <div className="row input-group">
        <span className="input-group-text" id="inputGroup-sizing-default">URL</span>
        <input id="url" type="text" className="form-control" aria-label="Sizing example input"
               aria-describedby="inputGroup-sizing-default"/>
      </div>
      <div className={'row justify-content-center'}>
        <div className="col-md-auto">
          <div className="form-check">
            <input id="separately" className="form-check-input" type="checkbox" value=""/>
            <label className="form-check-label cursor-on-hover" htmlFor="separately" data-toggle="tooltip" data-placement="top"
                   title="Check this box if you want to send each invoice separately. This results in sending multiple requests, one per invoice." aria-hidden="true">
              Send invoices separately
            </label>
          </div>
        </div>
      </div>
      <div className="row input-group" id={"send-separately-key-div"}>
        <span className="input-group-text cursor-on-hover" id="key-label" data-toggle="tooltip" data-placement="top"
              title="Leave it empty if you want to send each invoice with the file name as its key. Otherwise, type in a key that will be used to mark the invoice data.
              This change will not be seen in the json data preview (json keys has to be unique), but will be processed during request sending process." aria-hidden="true">Key</span>
        <input id="invoice_key" type="text" className="form-control" aria-label="Sizing example input"
               aria-describedby="inputGroup-sizing-default"/>
      </div>
    </div>
  );
}

export default UrlOptions;

export function SetUrlConfiguration(urlConfiguration) {
  document.getElementById("url").value = urlConfiguration["url"];
  document.getElementById("separately").checked = urlConfiguration["separately"];
  document.getElementById("invoice_key").value = urlConfiguration["invoice_key"];

  let keyFieldId = "key-label";
  let invoiceKeyId = "invoice_key";

  if (document.getElementById("separately").checked) {
    EnableObject(keyFieldId, true);
    EnableObject(invoiceKeyId, true);
  } else {
    EnableObject(keyFieldId, false);
    EnableObject(invoiceKeyId, false);
    document.getElementById("invoice_key").value = ""
  }

  const separatelySendCheckBox = document.getElementById('separately');

  separatelySendCheckBox.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
      EnableObject(keyFieldId, true);
      EnableObject(invoiceKeyId, true);
    } else {
      EnableObject(keyFieldId, false);
      EnableObject(invoiceKeyId, false);
      document.getElementById("invoice_key").value = ""
    }
  })

}

export function GetUrlConfiguration() {
  const url = document.getElementById("url").value
  const separately = document.getElementById("separately").checked
  const invoice_key = document.getElementById("invoice_key").value
  const url_configuration = {};
  url_configuration.url = url;
  url_configuration.separately  = separately;
  url_configuration.invoice_key  = invoice_key;
  return url_configuration;
}
