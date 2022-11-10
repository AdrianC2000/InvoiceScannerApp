import React from 'react';
import Modal from 'react-modal';
import SettingsPopup from './settings_popup';

const customStyles = {
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)',
  },
};

Modal.setAppElement('#root');

function SettingsModal() {
  const [modalIsOpen, setIsOpen] = React.useState(false);

  function openModal() {
    setIsOpen(true);
  }

  function closeModal() {
    setIsOpen(false);
  }

  return (
    <div>
      <i className="fa fa-cog fa-2x settings-button hvr-fade" id={"settings"} aria-hidden="true" onClick={openModal}></i>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        style={customStyles}
        contentLabel="Example Modal"
      >
        <div className="container-fluid" id={"modalBody"}>
          <div className="row d-flex justify-content-end Header">
            <div className="col-4 d-flex justify-content-center">
              <h2><b>Settings</b></h2>
            </div>
            <div className="col-4 d-flex justify-content-end">
              <i className="fa fa-arrow-left fa-2x settings-button hvr-fade" aria-hidden="true" onClick={closeModal}></i>
            </div>
          </div>
          <SettingsPopup />
        </div>
      </Modal>
    </div>
  );
}

export default SettingsModal;

