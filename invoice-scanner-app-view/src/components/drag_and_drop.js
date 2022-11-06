import React from 'react';
import { FileUploader } from 'react-drag-drop-files';
import { addFileToList } from './list';
import { EnableObject } from './common';

let fileTypes = ['JPEG', 'PNG', 'GIF'];

let filesList = [];

export default function DragAndDrop() {
  const handleChange = (files) => {
    for (const new_file of files) {
      if (filesList.filter(file => file.path === new_file.path).length > 0) {
        console.log("File with path: " + new_file.path + " has already been updated.")
      } else {
        filesList.push(new_file);
        addFileToList(new_file);
      }
      if (filesList.length > 0) {
        EnableObject("getDataButton", true)
      }
    }
  };
  return (
    <div id="dragAndDrop">
      <FileUploader
        multiple
        handleChange={handleChange}
        name="file"
        types={fileTypes}
      />
    </div>
  );
}

export function removeItemFromTheList(id) {
  filesList = filesList.filter(function( file ) {
    return file.path !== id;
  });
}

export function getFilesList() {
  return filesList;
}
