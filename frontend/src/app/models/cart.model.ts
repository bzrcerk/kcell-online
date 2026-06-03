import {ProductModel} from './product.model';

export interface CartModel {
  id: number;
  userId : number;
}

export interface CartItemModel {
  id : number;
  cart : CartModel;
  product : ProductModel;
  quantity: number;
}
