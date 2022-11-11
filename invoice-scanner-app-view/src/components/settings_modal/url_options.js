import React from 'react';

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
            <label className="form-check-label" htmlFor="separately">
              Send invoices separately
            </label>
          </div>
        </div>
        <div className="col-md-auto">
          <i className="fa fa-info-circle fa-2x" data-toggle="tooltip" data-placement="top"
             title="If you leave this box unchecked, request body will include all invoices at once.
             Otherwise, every invoice will be sent separately, which results in multiple requests." aria-hidden="true" id={"urlInfo"}></i>
        </div>
      </div>
    </div>
  );
}

export default UrlOptions;

export function SetUrlConfiguration(urlConfiguration) {
  document.getElementById("url").value = urlConfiguration["url"];
  document.getElementById("separately").checked = urlConfiguration["separately"];
}

export function GetUrlConfiguration() {
  const url = document.getElementById("url").value
  const separately = document.getElementById("separately").checked
  const url_configuration = {};
  url_configuration.url = url;
  url_configuration.separately  = separately;
  return url_configuration;
}
