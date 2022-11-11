import React from 'react';
import JsonFieldListElement from './json_field_list_element';

function DataFormat() {
  return (
    <ul className="list-group" id={"keysList"}>
        <JsonFieldListElement field={"parsed_table"} value={"parsed_table"}/>
        <JsonFieldListElement field={"ordinal_number"} value={"ordinal_number"}/>
      <JsonFieldListElement field={"name"} value={"name"}/>
      <JsonFieldListElement field={"pkwiu"} value={"pkwiu"}/>
      <JsonFieldListElement field={"quantity"} value={"quantity"}/>
      <JsonFieldListElement field={"unit_of_measure"} value={"unit_of_measure"}/>
      <JsonFieldListElement field={"gross_price"} value={"gross_price"}/>
      <JsonFieldListElement field={"net_price"} value={"net_price"}/>
      <JsonFieldListElement field={"net_value"} value={"net_value"}/>
      <JsonFieldListElement field={"vat"} value={"vat"}/>
      <JsonFieldListElement field={"vat_value"} value={"vat_value"}/>
      <JsonFieldListElement field={"gross_value"} value={"gross_value"}/>
      <JsonFieldListElement field={"seller"} value={"seller"}/>
      <JsonFieldListElement field={"buyer"} value={"buyer"}/>
      <JsonFieldListElement field={"invoice_number"} value={"invoice_number"}/>
      <JsonFieldListElement field={"currency"} value={"currency"}/>
      <JsonFieldListElement field={"listing_date"} value={"listing_date"}/>
    </ul>
  );
}

export default DataFormat;

export function SetDataConfiguration(dataConfiguration) {
    for (const key in dataConfiguration) {
        if (key === "remove_nulls") {
            document.getElementById(key).checked = dataConfiguration[key];
        } else {
            document.getElementById(key).value = dataConfiguration[key]["value"];
            document.getElementById("checkBox" + key).checked = dataConfiguration[key]["included"];
        }
    }
}

export function GetDataConfiguration() {
    const data_configuration = {};
    data_configuration['remove_nulls'] = document.getElementById('remove_nulls').checked

    const ul = document.getElementById('keysList');
    const items = ul.getElementsByTagName('li');

    for (let i = 0; i < items.length; ++i) {
        const li = items[i];
        const key = li.querySelector('.keyInput').value;
        const value = li.querySelector('.valueInput').value;
        const shouldInclude = li.querySelector('.shouldIncludeCheckBox').checked;
        const key_configuration = {};
        key_configuration["value"] = value;
        key_configuration["included"] = shouldInclude;
        data_configuration[key] = key_configuration
    }
    return data_configuration;
}
