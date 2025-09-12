import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface DropdownOption {
  value: string;
  text: string;
}

interface SearchFormData {
  // No dropdown data needed for simplified search
}

interface WorkOrderSearchRequest {
  i_lang: string;
  i_usercode: string;
  vin?: string;
  dealer_code?: string;
  wo_no?: string;
  date_from?: string;
  date_to?: string;
  temsa_global?: boolean;
  temsa_global_gwk?: boolean;
  germany?: boolean;
  france?: boolean;
  north_america?: boolean;
}

interface WorkOrderItem {
  credate?: string;
  dealer_code?: string;
  vin?: string;
  wo_status?: string;
  wo_status_text?: string;
  wo_type?: string;
  wo_type_text?: string;
  fg_status_text?: string;
  pds?: string;
  demo?: string;
  wono?: string;
  creuser?: string;
  ra_country_text?: string;
  wo_onay_text?: string;
  reject_note?: string;
  enability_button?: boolean;
}

interface WorkOrderSearchResponse {
  success: boolean;
  message: string;
  work_orders: WorkOrderItem[];
  error_type?: string;
  error_message?: string;
}

@Injectable({
  providedIn: 'root'
})
export class WorkOrderService {
  private apiUrl = '/api/sap/work-orders';

  constructor(private http: HttpClient) {}

  getFormData(): Observable<SearchFormData> {
    return this.http.get<SearchFormData>(`${this.apiUrl}/form-data`);
  }

  searchWorkOrders(searchRequest: WorkOrderSearchRequest): Observable<WorkOrderSearchResponse> {
    return this.http.post<WorkOrderSearchResponse>(`${this.apiUrl}/search`, searchRequest);
  }
}