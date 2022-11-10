import React from 'react';
import { getFilesList, removeItemFromTheList } from './drag_and_drop';
import { EnableObject } from './common';

function List({id}) {
  return (
    <ul className="list-group" id={id}></ul>
  );
}

export default List;

export function addFileToList(file) {
    const ul = document.getElementById('invoices-list');
    const li = document.createElement('li');
    li.className = "list-group-item";
    li.appendChild(document.createTextNode(file.name));

    const deleteButton = document.createElement("i")
    deleteButton.className = "fa fa-trash fa-lg delete-button hvr-fade"
    deleteButton.id = file.path;
    li.append(deleteButton)

    deleteButton.addEventListener("click", function (e) {
      this.parentNode.parentNode.removeChild(this.parentNode);
      removeItemFromTheList(this.id)
      if (getFilesList().length === 0) {
        EnableObject("getDataButton", false)
      }
    });

    ul.appendChild(li);
}
