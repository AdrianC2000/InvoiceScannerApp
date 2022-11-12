import { getData } from './get_data_button';

export function SwitchClasses(objectId, classToDelete, classToAdd) {
  const object = document.getElementById(objectId)
  object.classList.remove(classToDelete)
  object.classList.add(classToAdd)
}

export function EnableObject(objectId, enabled) {
  const object = document.getElementById(objectId)
  object.enabled = enabled
  object.disabled = !enabled
  if (enabled && objectId === "getDataButton") {
    object.onclick = getData;
  } else {
     // TODO
  }
}


