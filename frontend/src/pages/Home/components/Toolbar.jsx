/* eslint-disable react/prop-types */
import { AiOutlineSearch } from "react-icons/ai";
import { GenericButton, Input } from "../../../components";

const Toolbar = ({ setVisible }) => {
  return (
    <div className="flex items-center bg-white h-full max-h-40 w-full rounded-b-md border p-3 shadow-sm">
      <div className="flex flex-wrap gap-2 items-center justify-between w-full">
        <div className="flex flex-wrap items-str gap-3">
          <Input
            icon={<AiOutlineSearch className="text-slate-500 text-20 mr-2" />}
            onChange={undefined}
            placeholder="Procurar por cliente"
          />
        </div>
        <div className="flex items-center gap-2">
          <GenericButton
            text="Atualizar Preço do Kg"
            color={"white"}
            bgColor={"bg-emerald-500"}
            onClick={() => setVisible(true)}
            icon={undefined}
          />
        </div>
      </div>
    </div>
  );
};

export default Toolbar;
