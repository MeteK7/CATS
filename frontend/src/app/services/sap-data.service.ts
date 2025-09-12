import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { SAPRecord, SAPResponse } from '../models/sap-record.model';

@Injectable({
  providedIn: 'root'
})
export class SapDataService {
  private apiUrl = '/api/sap'; // Use relative path with Angular proxy

  constructor(private http: HttpClient) {
    // API calls will be proxied through Angular dev server to backend
  }

  getAllRecords(): Observable<SAPRecord[]> {
    return this.http.get<SAPRecord[]>(`${this.apiUrl}/records`);
  }

  getRecord(id: string): Observable<SAPRecord> {
    return this.http.get<SAPRecord>(`${this.apiUrl}/records/${id}`);
  }

  createRecord(record: SAPRecord): Observable<SAPResponse> {
    return this.http.post<SAPResponse>(`${this.apiUrl}/records`, record);
  }

  updateRecord(id: string, record: SAPRecord): Observable<SAPResponse> {
    return this.http.put<SAPResponse>(`${this.apiUrl}/records/${id}`, record);
  }

  deleteRecord(id: string): Observable<SAPResponse> {
    return this.http.delete<SAPResponse>(`${this.apiUrl}/records/${id}`);
  }
}