import React, { useState } from 'react';

function JsonFieldListElement({field, value}) {
  const [message, setMessage] = useState(value);

  const handleChange = event => {
    setMessage(event.target.value);
  };
  return (
    <li className={"list-group-item"}>
      <div className="container">
        <div className="row no-gutters">
          <div className="col-4">
            <input type="text" className="form-control" placeholder="Key" value={field} disabled/>
          </div>
          <div className="col-7">
            <input id={message} type="text" className="form-control" placeholder="Value" defaultValue={message} onChange={handleChange}/>
          </div>
          <div className="form-check no-gutters" id="delete-header-button">
            <input className="form-check-input shouldIncludeCheckBox" type="checkbox" value="" id={"checkBox" + message}/>
          </div>
        </div>
      </div>
    </li>
  );
}

export default JsonFieldListElement;
