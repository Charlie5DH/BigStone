import Toolbar from "./components/Toolbar";
import { useDispatch, useSelector } from "react-redux";
import { ProductsList } from "../../components";
import { getItems } from "../../actions/items";
import { ProgressSpinner } from "primereact/progressspinner";
import React from "react";

const Products = () => {
  const { items, isLoadingItems } = useSelector((state) => state.items);
  const [selectedCategory, setSelectedCategory] = React.useState(null);
  const [inputTextFilter, setInputTextFilter] = React.useState("");
  const [filteredItems, setFilteredItems] = React.useState([]);
  const dispatch = useDispatch();

  React.useEffect(() => {
    dispatch(getItems(true));
  }, []);

  React.useEffect(() => {
    if (items.length > 0) {
      setFilteredItems(items);
    }
  }, [items]);

  const handleFilterItemsByName = (e) => {
    setInputTextFilter(e.target.value);
    if (e.target.value === "") {
      setFilteredItems(items);
    } else {
      setFilteredItems(items.filter((item) => item.name.toLowerCase().includes(e.target.value.toLowerCase())));
    }
  };

  /**implementar pagination */

  return (
    <div className="flex flex-col">
      <Toolbar
        inputTextFilter={inputTextFilter}
        setInputTextFilter={setInputTextFilter}
        selectedCategory={selectedCategory}
        setSelectedCategory={setSelectedCategory}
        handleFilterItemsByName={handleFilterItemsByName}
      />

      {isLoadingItems ? (
        <div className="flex items-center justify-center mt-10">
          <ProgressSpinner
            style={{ width: "80px", height: "80px" }}
            strokeWidth="4"
            fill="var(--surface-ground)"
            animationDuration="1.2s"
          />
        </div>
      ) : (
        <div
          className="flex flex-wrap items-center mt-2 border 
          bg-white shadow-indigo-100 shadow-md rounded-md p-3 max-w-full
          overflow-x-auto mx-1 mb-3 max-h-[82vh] justify-center overflow-y-scroll"
        >
          <ProductsList products={filteredItems} />
        </div>
      )}
    </div>
  );
};

export default Products;

/*
<div className="flex flex-wrap items-stretch lg:grid lg:grid-cols-3 lg:gap-2 mt-3 mx-2">
  {items.map((item, index) => (
    <ProductCarHor product={item} key={index} />
  ))}
</div>
 */
