import { GET_KG_PRICE, LOADING_KG_PRICE, END_LOADING_KG_PRICE, UPDATE_KG_PRICE } from "../constants/weight";

const reducer = (state = { kg_price: 0, isLoadingKGPrice: true }, action) => {
  switch (action.type) {
    case GET_KG_PRICE:
      return { ...state, kg_price: action.payload.kg_price };
    case LOADING_KG_PRICE:
      return { ...state, isLoadingKGPrice: true };
    case END_LOADING_KG_PRICE:
      return { ...state, isLoadingKGPrice: false };
    case UPDATE_KG_PRICE:
      return { ...state, kg_price: action.payload };
    default:
      return state;
  }
};

export default reducer;
