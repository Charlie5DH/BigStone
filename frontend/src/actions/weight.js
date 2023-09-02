import * as api from "../apis/";
import { GET_KG_PRICE, LOADING_KG_PRICE, END_LOADING_KG_PRICE, UPDATE_KG_PRICE } from "../constants/weight";

export const getKGPrice = () => async (dispatch) => {
  try {
    dispatch({ type: LOADING_KG_PRICE });
    const { data } = await api.getKGPrice();
    dispatch({ type: GET_KG_PRICE, payload: data });
    dispatch({ type: END_LOADING_KG_PRICE });
  } catch (error) {
    console.log(error);
  }
};

export const updateKGPrice = (newPrice) => async (dispatch) => {
  try {
    dispatch({ type: LOADING_KG_PRICE });
    const { data } = await api.updateKGPrice(newPrice);
    dispatch({ type: UPDATE_KG_PRICE, payload: data });
    dispatch({ type: END_LOADING_KG_PRICE });
  } catch (error) {
    console.log(error);
  }
};
