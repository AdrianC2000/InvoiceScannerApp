import React from 'react';
import UrlOptions from './url_options';
import HeadersOptions from './headers_options';

function EndpointConfiguration() {
  return (
    <div className={'endpoint-configuration container-fluid d-flex h-100 flex-column'}>
      <UrlOptions />
      <div className={'row spacing'}></div>
      <HeadersOptions />
    </div>
  );
}

export default EndpointConfiguration;
