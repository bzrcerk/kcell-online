export interface CategoryModel {
  id: number;
  title: string;
}


export interface ProductModel {
  id: number;
  categoryId: number;
  title : string;
  description : string;
  price : number;
  imageUrl : string;
}
