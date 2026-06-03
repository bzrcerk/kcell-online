export interface OrderModel {
  id: number;
  user_id: number;
  full_name: string;
  email: string;
  phone_number: string;
  address: string;
  total_price: number;
  status: string;
  created_at: string;
}

export interface OrderItemModel {
  id: number;
  order_id: number;
  product_id: number;
  product_name: string;
  price: number;
  created_at: string;
}
