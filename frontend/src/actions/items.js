import * as api from "../apis/";
import {
  GET_ITEMS,
  GET_ITEMS_BY_ID,
  CREATE_ITEM,
  CREATE_MANY_ITEMS,
  UPDATE_ITEM,
  UPDATE_ITEM_QUANTITY,
  SUBTRACT_ITEM_QUANTITY,
  DELETE_ITEM,
  LOADING_ITEMS,
  END_LOADING_ITEMS,
  LOADING_ITEM,
  END_LOADING_ITEM,
  LOADING_ITEM_QUANTITY,
  END_LOADING_ITEM_QUANTITY,
  DELETE_MANY_ITEMS,
} from "../constants/items";

export const getItems = (add_daily_mean_sales, period) => async (dispatch) => {
  try {
    dispatch({ type: LOADING_ITEMS });
    const { data } = await api.getItems(add_daily_mean_sales, period);
    dispatch({ type: GET_ITEMS, payload: data });
    dispatch({ type: END_LOADING_ITEMS });
  } catch (error) {
    console.log(error);
  }
};

export const getItemById = (id) => async (dispatch) => {
  try {
    dispatch({ type: LOADING_ITEM });
    const { data } = await api.getItemById(id);
    dispatch({ type: GET_ITEMS_BY_ID, payload: data });
    dispatch({ type: END_LOADING_ITEM });
  } catch (error) {
    console.log(error);
  }
};

export const createItem = (newItem) => async (dispatch) => {
  try {
    dispatch({ type: LOADING_ITEMS });
    const { data } = await api.postItem(newItem);
    dispatch({ type: CREATE_ITEM, payload: data });
    dispatch({ type: END_LOADING_ITEMS });
  } catch (error) {
    console.log(error);
  }
};

export const createManyItems = (newItems) => async (dispatch) => {
  try {
    dispatch({ type: LOADING_ITEMS });
    const { data } = await api.createManyItems(newItems);
    dispatch({ type: CREATE_MANY_ITEMS, payload: data });
    dispatch({ type: END_LOADING_ITEMS });
  } catch (error) {
    console.log(error);
  }
};

export const updateItem = (id, updatedItem) => async (dispatch) => {
  try {
    dispatch({ type: LOADING_ITEMS });
    const { data } = await api.updateItem(id, updatedItem);
    dispatch({ type: UPDATE_ITEM, payload: data });
    dispatch({ type: END_LOADING_ITEMS });
  } catch (error) {
    console.log(error);
  }
};

export const updateItemQuantity = (id, quantity, user) => async (dispatch) => {
  try {
    dispatch({ type: LOADING_ITEM_QUANTITY });
    const { data } = await api.updateItemQuantity(id, quantity, user);
    dispatch({ type: UPDATE_ITEM_QUANTITY, payload: data });
    dispatch({ type: END_LOADING_ITEM_QUANTITY });
  } catch (error) {
    console.log(error);
  }
};

export const subtractItemQuantity = (id, quantity) => async (dispatch) => {
  try {
    dispatch({ type: LOADING_ITEM_QUANTITY });
    const { data } = await api.subtractItemQuantity(id, quantity);
    dispatch({ type: SUBTRACT_ITEM_QUANTITY, payload: data });
    dispatch({ type: END_LOADING_ITEM_QUANTITY });
  } catch (error) {
    console.log(error);
  }
};

export const deleteItem = (id) => async (dispatch) => {
  try {
    await api.deleteItem(id);
    dispatch({ type: DELETE_ITEM, payload: id });
  } catch (error) {
    console.log(error);
  }
};

export const deleteManyItems = (ids) => async (dispatch) => {
  try {
    await api.deleteManyItems(ids);
    dispatch({ type: DELETE_MANY_ITEMS, payload: ids });
  } catch (error) {
    console.log(error);
  }
};
