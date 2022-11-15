import React from 'react';
import JsonFieldListElement from './json_field_list_element';

function DataFormat() {
  return (
    <ul className="list-group" id={'keysList'}>
      <JsonFieldListElement field={'parsed_table'} value={'parsed_table'}/>
      <JsonFieldListElement field={'ordinal_number'} value={'ordinal_number'}/>
      <JsonFieldListElement field={'name'} value={'name'}/>
      <JsonFieldListElement field={'pkwiu'} value={'pkwiu'}/>
      <JsonFieldListElement field={'quantity'} value={'quantity'}/>
      <JsonFieldListElement field={'unit_of_measure'} value={'unit_of_measure'}/>
      <JsonFieldListElement field={'gross_price'} value={'gross_price'}/>
      <JsonFieldListElement field={'net_price'} value={'net_price'}/>
      <JsonFieldListElement field={'net_value'} value={'net_value'}/>
      <JsonFieldListElement field={'vat'} value={'vat'}/>
      <JsonFieldListElement field={'vat_value'} value={'vat_value'}/>
      <JsonFieldListElement field={'gross_value'} value={'gross_value'}/>
      <JsonFieldListElement field={'invoice_number'} value={'invoice_number'}/>
      <JsonFieldListElement field={'currency'} value={'currency'}/>
      <JsonFieldListElement field={'listing_date'} value={'listing_date'}/>
      <JsonFieldListElement field={'seller_name'} value={'seller_name'}/>
      <JsonFieldListElement field={'seller_address'} value={'seller_address'}/>
      <JsonFieldListElement field={'seller_nip'} value={'seller_nip'}/>
      <JsonFieldListElement field={'buyer_name'} value={'buyer_name'}/>
      <JsonFieldListElement field={'buyer_address'} value={'buyer_address'}/>
      <JsonFieldListElement field={'buyer_nip'} value={'buyer_nip'}/>
    </ul>
  );
}

export default DataFormat;

export function SetDataConfiguration(dataConfiguration) {
  for (const key in dataConfiguration) {
    if ((['remove_nulls', 'convert_to_cents', 'remove_percentage', 'convert_currency'].includes(key))) {
      document.getElementById(key).checked = dataConfiguration[key];
    } else {
      document.getElementById(key).value = dataConfiguration[key]['value'];
      document.getElementById('checkBox' + key).checked = dataConfiguration[key]['included'];
    }
  }
}

export function GetDataConfiguration() {
  const data_configuration = {};
  data_configuration['remove_nulls'] = document.getElementById('remove_nulls').checked;
  data_configuration['convert_to_cents'] = document.getElementById('convert_to_cents').checked;
  data_configuration['remove_percentage'] = document.getElementById('remove_percentage').checked;
  data_configuration['convert_currency'] = document.getElementById('convert_currency').checked;

  const ul = document.getElementById('keysList');
  const items = ul.getElementsByTagName('li');

  for (let i = 0; i < items.length; ++i) {
    const li = items[i];
    const key = li.querySelector('.keyInput').value;
    const value = li.querySelector('.valueInput').value;
    const shouldInclude = li.querySelector('.shouldIncludeCheckBox').checked;
    const key_configuration = {};
    key_configuration['value'] = value;
    key_configuration['included'] = shouldInclude;
    data_configuration[key] = key_configuration;
  }
  return data_configuration;
}
