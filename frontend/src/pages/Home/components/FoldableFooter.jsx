/* eslint-disable react/prop-types */

const FoldableFooter = ({ activeDropdown, index, record, produtos }) => {
  return (
    activeDropdown[index] && (
      <div className="flex flex-col gap-y-1 px-3 py-2 duration-200 mt-2">
        {record.items.length == 0 ? (
          <div className="flex flex-col items-center justify-center w-full my-1">
            <span className="text-14 font-medium text-slate-600">Sem produtos vendidos</span>
          </div>
        ) : (
          <div className="flex flex-col items-center border rounded-md w-full my-1">
            <div
              className="grid grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 w-full items-center
   justify-between p-3 bg-slate-100"
            >
              <div className="flex items-start col-span-2 lg:col-span-3 xl:col-span-3">
                <span className="text-14 font-medium text-slate-600">Produtos vendidos</span>
              </div>

              <div
                className="lg:flex hidden items-center justify-center gap-1 text-slate-500
     hover:text-slate-400 duration-200 cursor-pointer border-l"
              >
                <span className="text-[13px] font-normal">Preço</span>
              </div>

              <div className="flex items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
                <span className="text-[13px] font-normal">Vendidos</span>
              </div>
            </div>

            {record.items.length > 0 &&
              record.items.map((produto, index) => (
                <div
                  key={index}
                  className="grid grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 w-full items-center justify-between p-3 bg-slate-100 border-t"
                >
                  <div className="flex items-start col-span-2 lg:col-span-3 xl:col-span-3">
                    <div className="flex items-center">
                      <img
                        src={`http://localhost:8003/api/get_image/${
                          produtos.find((e) => e._id === produto.item_id).image
                        }`} //"https://placehold.co/600x400" ||
                        alt="produto"
                        className="rounded-md shadow-sm w-16 h-16 object-cover"
                      />
                      <div className="flex flex-col gap-y-1 ml-4">
                        <span className="text-14 font-medium text-slate-700">{produto.name}</span>
                        <span className="text-12 font-normal text-slate-500">
                          {produtos.find((e) => e._id === produto.item_id).description}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div
                    className="lg:flex hidden items-center justify-center gap-1 text-slate-500
     hover:text-slate-400 duration-200 border-l"
                  >
                    <span className="text-12 font-normal text-slate-500">
                      {produtos.find((e) => e._id === produto.item_id).price}
                    </span>
                  </div>
                  <div
                    className="lg:flex hidden items-center justify-center gap-1 text-slate-500
     hover:text-slate-400 duration-200 border-l"
                  >
                    <span className="text-12 font-normal text-slate-500">{produto.quantity}</span>
                  </div>
                </div>
              ))}
          </div>
        )}
      </div>
    )
  );
};

export default FoldableFooter;
