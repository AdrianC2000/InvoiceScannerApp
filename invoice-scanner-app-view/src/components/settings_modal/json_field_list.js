import React from 'react';
import JsonFieldListElement from './json_field_list_element';

function JsonFieldList() {
  return (
    <ul className="list-group">
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

export default JsonFieldList;
