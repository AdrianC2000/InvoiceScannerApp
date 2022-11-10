import React from 'react';
import List from '../list';

function HeadersOptions() {
  return (
    <div className={'container headers'}>
      <div className="row d-flex justify-content-end sub-header">
        <div className="col-1">
        </div>
        <div className="col-10 d-flex justify-content-center">
          <h4><b>Headers</b></h4>
        </div>
        <div className="col-1 d-flex justify-content-end">
          <i className="fa fa-plus settings-button hvr-fade" aria-hidden="true"
             onClick={AddEmptyElement}></i>
        </div>
      </div>
      <div className="row justify-content-center overflow-auto sub-data-container">
        <List id={'headers-list'}/>
      </div>
    </div>
  );
}

export default HeadersOptions;

function AddEmptyElement() {
  AddElement("", "")
}

function AddElement(key, value) {
  const ul = document.getElementById('headers-list');
  const li = document.createElement('li');
  li.id = ul.getElementsByTagName("li").length
  li.className = 'list-group-item d-flex align-items-center';

  const outerDiv = document.createElement("div")
  outerDiv.className = "container"

  const row = document.createElement("row")
  row.className = "row no-gutters"

  const keyColumn = document.createElement("div")
  keyColumn.className = "col-5"

  const inputKeyColumn = document.createElement("input")
  inputKeyColumn.className = "form-control";
  inputKeyColumn.placeholder = "Key";
  inputKeyColumn.value = key;

  keyColumn.appendChild(inputKeyColumn);

  const valueColumn = document.createElement("div")
  valueColumn.className = "col-5"

  const inputValueColumn = document.createElement("input")
  inputValueColumn.className = "form-control";
  inputValueColumn.placeholder = "Value";
  inputValueColumn.value = value;

  valueColumn.appendChild(inputValueColumn);

  const buttonColumn = document.createElement("div")
  buttonColumn.className = "col-2"

  const deleteButton = document.createElement("i")
  deleteButton.className = "fa fa-trash fa-lg delete-header-button hvr-fade"
  deleteButton.id = "header" + li.id;
  deleteButton.addEventListener("click", function (e) {
    this.parentNode.parentNode.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode.parentNode.parentNode);
  });

  buttonColumn.appendChild(deleteButton);
  row.append(keyColumn)
  row.append(valueColumn)
  row.append(buttonColumn)

  outerDiv.append(row)
  li.append(outerDiv)
  ul.append(li);
}

export function SetHeadersConfiguration(headersConfiguration) {
  for (const key in headersConfiguration) {
    AddElement(key, headersConfiguration[key])
  }
}
