/* eslint-disable react/prop-types */
import { Dialog } from "primereact/dialog";

const AddProductToSaleDialog = ({
  filterQuery,
  filteredItems,
  transactionForm,
  handleFilterItems,
  setTransactionForm,
  viewInsertProductDialog,
  setViewInsertProductDialog,
  handleAddItemToTransactionForm,
  handleRemoveItemFromTransactionForm,
}) => {
  return (
    <Dialog
      header="Adicionar produtos ao pedido"
      visible={viewInsertProductDialog}
      style={{ width: "50vw" }}
      onHide={() => setViewInsertProductDialog(false)}
    >
      <div className="flex items-center justify-between w-full mb-2 gap-1">
        <input
          className="relative w-1/2 h-10 cursor-text text-left font-light sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
          name="filter_object"
          type="text"
          value={filterQuery}
          onChange={(e) => handleFilterItems(e)}
          placeholder={`filtrar produtos por nome`}
          autoComplete="off"
        ></input>

        <button
          onClick={() => {
            // clean transaction form items
            setTransactionForm({
              ...transactionForm,
              items: [],
            });
          }}
          className="bg-white hover:bg-indigo-400 hover:text-white text-slate-500 text-14 font-normal
              py-2 px-3 rounded-md border duration-200 shadow-sm shadow-indigo-200 active:scale-95"
        >
          Limpar produtos adicionados
        </button>
      </div>

      {transactionForm.items.length > 0 ? (
        <div className="flex flex-wrap items-center w-full mb-2 gap-1 border rounded-md p-3">
          {transactionForm.items.map((item) => (
            <div key={item.name} className="flex items-center px-3 py-1 border rounded-md bg-slate-50">
              <span className="flex items-center gap-2 text-[13px] font-normal text-slate-500">{item.name}:</span>
              <span className="flex items-center gap-2 text-[13px] font-semibold text-slate-600 ml-4">
                {item.quantity}
              </span>
            </div>
          ))}
        </div>
      ) : (
        <div className="flex flex-wrap items-center w-full mb-2 gap-1 border rounded-md p-3">
          <span className="flex items-center gap-2 px-3 py-1 text-[13px] font-normal text-slate-500">
            Nenhum produto adicionado
          </span>
        </div>
      )}

      <div className="flex flex-col w-full gap-y-1 max-h-[620px] overflow-y-scroll">
        <div className="flex flex-col items-center border rounded-md w-full my-1">
          <div className="grid grid-cols-6 w-full items-center justify-between p-3 bg-slate-100">
            <div className="flex items-start col-span-2 lg:col-span-3 xl:col-span-3">
              <span className="flex items-center gap-2 text-[13px] font-normal text-slate-500">Nome</span>
            </div>

            <div
              className="lg:flex hidden items-center justify-center gap-1 text-slate-500
           hover:text-slate-400 duration-200 cursor-pointer border-l"
            >
              <span className="text-[13px] font-normal">Preço</span>
            </div>

            <div className="flex items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
              <span className="text-[13px] font-normal">Disponível</span>
            </div>

            <div className="flex items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
              <span className="text-[13px] font-normal">Ações</span>
            </div>
          </div>
          {filteredItems.map((produto, index) => (
            <div key={index} className="grid grid-cols-6 w-full items-center justify-between p-2 border-t">
              <div className="flex items-start col-span-3 p-1">
                <div className="flex flex-nowrap items-center">
                  <img
                    src={`http://localhost:8003/api/get_image/${produto.image}`} //"https://placehold.co/600x400" ||
                    alt="produto"
                    className="rounded-md shadow-sm w-12 h-12 object-cover"
                  />
                  <div className="flex flex-col gap-y-1 ml-4">
                    <span className="text-14 font-medium text-slate-700">{produto.name}</span>
                    <span className="text-12 font-normal text-slate-500">{produto.description}</span>
                  </div>
                </div>
              </div>
              <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l">
                <span className="text-14 font-normal text-slate-500">$R {produto.price}</span>
              </div>
              <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l">
                <span className="text-14 font-normal text-slate-500">{produto.quantity}</span>
              </div>
              <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500hover:text-slate-400 duration-200 border-l">
                <button
                  onClick={() => handleAddItemToTransactionForm(produto)}
                  className="text-slate-100 font-display font-semibold text-14 w-7 h-7 rounded-md hover:scale-105 duration-150 border bg-emerald-500 active:scale-95"
                >
                  +
                </button>
                <button
                  onClick={() => handleRemoveItemFromTransactionForm(produto)}
                  className="text-slate-100 font-display font-semibold text-14 w-7 h-7 rounded-md hover:scale-105 duration-150 border bg-slate-500 active:scale-95"
                >
                  -
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </Dialog>
  );
};

export default AddProductToSaleDialog;
