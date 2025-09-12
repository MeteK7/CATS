import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface DropdownOption {
  value: string;
  text: string;
}

interface SearchFormData {
  wo_types: DropdownOption[];
  wo_statuses: DropdownOption[];
  fg_statuses: DropdownOption[];
  countries: DropdownOption[];
  approval_statuses: DropdownOption[];
  ra_countries: DropdownOption[];
  strategies: DropdownOption[];
}

interface WorkOrderSearchRequest {
  i_lang: string;
  i_usercode: string;
  wo_type?: string;
  wo_type_multi?: string;
  wo_status?: string;
  wo_status_multi?: string;
  fg_status_multi?: string;
  country?: string;
  wonay?: string;
  ra_country?: string;
  vin?: string;
  ostrateji_td?: string;
  ostrateji_tg?: string;
  ostrateji_ti?: string;
  ostrateji_tf?: string;
  ostrateji_tx?: string;
  ostrateji_ty?: string;
  ostrateji_tz?: string;
  ostrateji_tu?: string;
  zcats_wo_conv?: string;
  creuser?: string;
  zgos?: string;
  demo?: string;
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