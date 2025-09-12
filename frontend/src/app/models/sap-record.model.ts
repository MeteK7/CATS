export interface SAPRecord {
  id?: string;
  data: { [key: string]: any };
}

export interface SAPResponse {
  success: boolean;
  message: string;
  data?: any;
}