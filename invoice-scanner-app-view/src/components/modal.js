import React from 'react';
import Modal from 'react-modal';
import TextArea from './text_area';

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

function Modal123() {
  const [modalIsOpen, setIsOpen] = React.useState(false);

  function openModal() {
    setIsOpen(true);
  }

  function closeModal() {
    setIsOpen(false);
  }

  return (
    <div>
      <i className="fa fa-cog fa-2x settings-button hvr-fade" aria-hidden="true" onClick={openModal}></i>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        style={customStyles}
        contentLabel="Example Modal"
      >
        <div className="container-fluid">
          <div className="row d-flex justify-content-end Header">
            <div className="col-4 d-flex justify-content-center">
              <h2><b>Settings</b></h2>
            </div>
            <div className="col-4 d-flex justify-content-end">
              <i className="fa fa-arrow-left fa-2x settings-button hvr-fade" aria-hidden="true" onClick={closeModal}></i>
            </div>
          </div>
          <div className="row no-gutters Data-container">
            <div className="col-md-6 data_column">
              <div className="col-md-11 big_inner_column">
                <div className="row justify-content-center no-gutters Header" id="uploadInvoice">
                  <p><b>Endpoint configuration</b></p>
                </div>
                <div className="row justify-content-center no-gutters Data-container">
                  <TextArea />
                </div>
              </div>
            </div>
            <div className="col-md-6 data_column">
              <div className="col-md-11 big_inner_column">
                <div className="row justify-content-center no-gutters Header">
                  <p><b>Data format configuration</b></p>
                </div>
                <div className="row justify-content-center no-gutters Data-container">
                  <TextArea />
                </div>
              </div>
            </div>
          </div>
        </div>
      </Modal>
    </div>
  );
}

export default Modal123;
