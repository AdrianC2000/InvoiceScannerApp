import React, { useEffect } from 'react';
import $ from 'jquery';
import 'jquery-ui-bundle';
import 'jquery-ui-bundle/jquery-ui.css';
import UrlOptions from './url_options';
import HeadersOptions from './headers_options';

function EndpointConfiguration() {
  useEffect(() => {
    SetEndpointValues()
  });
  return (
    <div className={'endpoint-configuration container-fluid d-flex h-100 flex-column'}>
      <UrlOptions />
      <div className={'row spacing'}></div>
      <HeadersOptions />
    </div>
  );
}

export default EndpointConfiguration;

export function SetEndpointValues() {
  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })
}
