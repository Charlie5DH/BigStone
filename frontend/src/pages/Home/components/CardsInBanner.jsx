/* eslint-disable react/prop-types */
import { Card } from "../../../components";

const CardsInBanner = ({
  transactions,
  computeDifferenceBetweenCurrentAndPast,
  computeNumeroDeVendasHoje,
  kg_price,
}) => {
  return (
    <div className="flex flex-wrap lg:flex-nowrap items-stretch w-full lg:w-[90%] gap-2">
      <Card
        title={`$R ${
          Number(
            transactions
              .filter((row) => row.timestamp.split("T")[0] === new Date().toISOString().split("T")[0])
              .reduce((acc, row) => acc + row.total, 0)
          ).toFixed(2) || 0
        }`}
        subtitle={"Total do dia"}
        titleCompare={
          // compare today and yesterday
          computeDifferenceBetweenCurrentAndPast("total") > 0
            ? `+${Number(computeDifferenceBetweenCurrentAndPast("total").toFixed(2))} comparado a ontem`
            : `${Number(computeDifferenceBetweenCurrentAndPast("total").toFixed(2))} comparado a ontem`
        }
        sign={"+"}
      />

      <Card
        title={
          computeDifferenceBetweenCurrentAndPast("meal_price") > 0
            ? `+$R ${Number(computeDifferenceBetweenCurrentAndPast("meal_price")).toFixed(2)}`
            : `+$R ${Number(computeDifferenceBetweenCurrentAndPast("meal_price")).toFixed(2)}`
        }
        subtitle={"Total do dia em refeições"}
        titleCompare={
          computeDifferenceBetweenCurrentAndPast("meal_price") > 0
            ? `+${Number(computeDifferenceBetweenCurrentAndPast("meal_price")).toFixed(2)} comparado a ontem`
            : `${Number(computeDifferenceBetweenCurrentAndPast("meal_price")).toFixed(2)} comparado a ontem`
        }
        sign={`${computeDifferenceBetweenCurrentAndPast("meal_price") > 0 ? "+" : ""}`}
      />
      <Card
        title={
          transactions.filter((row) => row.timestamp.split("T")[0] === new Date().toISOString().split("T")[0]).length ||
          0
        }
        subtitle={"# de vendas hoje"}
        titleCompare={
          computeNumeroDeVendasHoje() > 0
            ? `+${computeNumeroDeVendasHoje()} comparado a ontem`
            : `${computeNumeroDeVendasHoje()} comparado a ontem`
        }
        sign={"+"}
      />
      <Card title={`$R ${kg_price}`} subtitle={"Preço atual do KG"} />
    </div>
  );
};

export default CardsInBanner;
