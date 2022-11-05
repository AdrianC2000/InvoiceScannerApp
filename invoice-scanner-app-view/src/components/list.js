import React from 'react';
import { removeItemFromTheList } from './drag_and_drop';

function List() {
  return (
    <ul className="list-group" id={'invoices-list'}></ul>
  );
}

export default List;

export function addFileToList(file) {
    const ul = document.getElementById('invoices-list');
    const li = document.createElement('li');
    li.className = "list-group-item";
    li.appendChild(document.createTextNode(file.name));

    const btn = document.createElement("Button");
    btn.id = file.path;
    btn.className = "delete-button"
    btn.innerHTML = 'Delete';
    li.append(btn)

    btn.addEventListener("click", function (e) {
      this.parentNode.parentNode.removeChild(this.parentNode);
      removeItemFromTheList(this.id)
    });

    ul.appendChild(li);
}
