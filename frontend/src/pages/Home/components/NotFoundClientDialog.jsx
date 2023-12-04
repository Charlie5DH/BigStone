/* eslint-disable react/prop-types */
import { Dialog } from "primereact/dialog";

const NotFoundClientDialog = ({ clientError, setClientError }) => {
  return (
    <Dialog
      header="Cliente não encontrado"
      visible={clientError}
      style={{ width: "50vw" }}
      onHide={() => setClientError(false)}
    >
      <div className="flex flex-col items-center justify-center w-full mb-2 gap-1">
        <span className="text-slate-500 text-14 font-normal text-center">
          O cliente não foi encontrado no sistema. Por favor, verifique se o código RFID está correto.
        </span>
      </div>
    </Dialog>
  );
};

export default NotFoundClientDialog;
